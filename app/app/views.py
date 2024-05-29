from app.models import Question, Answer, Tag, Profile, User, QuestionVote, AnswerVote
from app.forms import LoginForm, SignupForm, ProfileForm, AskForm, AnswerForm, CorrectForm, VoteForm
from app.context_processors import get_centrifugo_data, get_top_lists

from core.settings import QUESTIONS_PER_PAGE, ANSWERS_PER_PAGE

from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.urls import reverse
from django.forms import model_to_dict
from django.http import JsonResponse
from django.conf import settings
from django.contrib.postgres.search import SearchQuery
from django.db.models import Q

import requests

import math
import json
import operator
import functools


def paginate(items, request, *, per_page=5):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(items, per_page)

    try:
        page_obj = paginator.page(page_number)
    except (EmptyPage, InvalidPage):
        page_obj = paginator.page(1)

    return page_obj


def index(request):
    new_questions = list(Question.objects.new_questions())
    page_obj = paginate(new_questions, request, per_page=QUESTIONS_PER_PAGE)

    context = {
        'questions': page_obj,
        **get_top_lists(),
    }

    return render(request, 'index.html', context)


@require_GET
def search(request):
    query = request.GET.get('q')
    if not query:
        return redirect(reverse('index'))

    queries = query.split()
    query_set = functools.reduce(operator.__or__, [Q(search_vector__icontains=query) for query in queries])
    matched_questions = Question.objects.filter(query_set).distinct()

    page_obj = paginate(matched_questions, request, per_page=QUESTIONS_PER_PAGE)

    context = {
        'questions': page_obj,
        **get_top_lists(),
    }

    return render(request, 'search.html', context)


@require_GET
def search_hints(request):
    query = request.GET.get('q')
    if not query:
        return JsonResponse({'error': 'Query can not be empty!'}, status=422)

    queries = query.split()
    query_set = functools.reduce(operator.__or__, [Q(search_vector__icontains=query) for query in queries])
    matched_questions = Question.objects.filter(query_set).distinct()[:settings.HINTS_COUNT]

    hints = set()
    for question in matched_questions:
        if query in question.title:
            content = question.title
        else:
            content = question.content

        match_start = content.find(queries[0])
        match_idx = match_start
        query_idx = 0
        while (query_idx < len(query) and query[query_idx] == content[match_idx]) \
                or (match_idx < len(content) and content[match_idx].isalpha()):
            match_idx += 1
            query_idx += 1
        else:
            hints.add(content[match_start:match_idx])

    return JsonResponse(sorted(filter(len, hints), key=len, reverse=True), safe=False)


def hot_questions(request):
    questions = list(Question.objects.hot_questions())
    page_obj = paginate(questions, request, per_page=QUESTIONS_PER_PAGE)

    context = {
        'questions': page_obj,
        **get_top_lists(),
    }

    return render(request, 'hot-questions.html', context)


def question(request, question_id):
    question = Question.objects.get_question(question_id)
    answers = Answer.objects.get_answers(question_id)

    answer_form = AnswerForm(request.user, question)

    context = {
        'form': answer_form,
        'question': question,
        'answers': answers,
        'example_answer': Answer(
            user_id=1,
            question_id=1,
            content='content',
        ),
        **get_top_lists(),
        **get_centrifugo_data(request),
        'ws_channel_name': f'question_{question_id}',
    }

    return render(request, 'question-details.html', context)


@login_required(login_url='login', redirect_field_name='continue')
@require_POST
@csrf_protect
def answer(request, question_id):
    ws_channel_name = f'question_{question_id}'

    question = Question.objects.get_question(question_id)
    answer_form = AnswerForm(request.user, question, request.POST)
    if answer_form.is_valid():
        answer = answer_form.save()
        answers_count = Answer.objects.get_answers(question_id).count()

        api_url = settings.CENTRIFUGO_API_URL
        api_key = settings.CENTRIFUGO_API_KEY

        body = model_to_dict(answer)
        body |= {'avatar_url': request.user.profile.avatar.url}

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'apikey {api_key}'
        }
        data = {
            'method': 'publish',
            'params': {
                'channel': ws_channel_name,
                'data': body,
            }
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            return redirect(
                reverse('question', kwargs={'question_id': question_id})
                + f'?page={math.ceil(answers_count / ANSWERS_PER_PAGE)}'
                + f'#{answer.id}'
            )


@login_required(login_url='login', redirect_field_name='continue')
@require_http_methods(['GET', 'POST'])
@csrf_protect
def ask(request):
    ask_form = AskForm(request.user)
    if request.method == 'POST':
        ask_form = AskForm(request.user, request.POST)
        if ask_form.is_valid():
            question = ask_form.save()
            if question:
                return redirect('question', question_id=question.id)

    context = {
        'form': ask_form,
        **get_top_lists(),
    }

    return render(request, 'ask.html', context)


@require_http_methods(['GET', 'POST'])
@csrf_protect
def login(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                redirect_to = request.GET.get('continue', reverse('index'))
                return redirect(redirect_to)

    context = {
        'form': login_form,
        **get_top_lists(),
    }

    return render(request, 'login.html', context)


@login_required(login_url='login', redirect_field_name='continue')
def logout(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER', reverse('index')))


@csrf_protect
def signup(request):
    signup_form = SignupForm()
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))

    context = {
        'form': signup_form,
        **get_top_lists(),
    }

    return render(request, 'signup.html', context)


def questions_by_tag(request, tag_name):
    questions = list(Question.objects.questions_by_tag(tag_name))
    page_obj = paginate(questions, request, per_page=QUESTIONS_PER_PAGE)

    context = {
        'questions': page_obj,
        **get_top_lists(),
        'tag_name': tag_name,
    }

    return render(request, 'tag.html', context)


@login_required(login_url='login', redirect_field_name='continue')
@require_http_methods(['GET', 'POST'])
@csrf_protect
def profile(request):
    profile_form = ProfileForm(request.user, initial={
        'username': request.user.username,
        'email': request.user.email,
    })
    if request.method == 'POST':
        profile_form = ProfileForm(
            request.user,
            request.POST,
            files=request.FILES,
            instance=request.user
        )
        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse('profile'))

    context = {
        'form': profile_form,
        **get_top_lists(),
    }

    return render(request, 'profile.html', context)


@login_required(login_url='login', redirect_field_name='continue')
@require_POST
@csrf_protect
def correct(request):
    body = json.loads(request.body)

    correct_form = CorrectForm(request.user, body)
    if correct_form.is_valid():
        answer = correct_form.save()
        body['is_correct'] = answer.is_correct
        return JsonResponse(body)

    errors = correct_form.errors
    return JsonResponse({'errors': errors}, status=422)


@login_required(login_url='login', redirect_field_name='continue')
@require_POST
@csrf_protect
def vote(request):
    body = json.loads(request.body)

    vote_form = VoteForm(request.user, body)
    if vote_form.is_valid():
        rating = vote_form.save()
        body['rating'] = rating
        return JsonResponse(body)

    errors = vote_form.errors
    return JsonResponse({'errors': errors}, status=422)
