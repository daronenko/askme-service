from app.models import Question, Answer, Tag, Profile, User
from app.forms import LoginForm, SignupForm, ProfileForm, AskForm, AnswerForm

from core.settings import QUESTIONS_PER_PAGE, ANSWERS_PER_PAGE

from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.urls import reverse
from django.forms import model_to_dict

import math


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
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'index.html', context)


def hot_questions(request):
    questions = list(Question.objects.hot_questions())
    page_obj = paginate(questions, request, per_page=QUESTIONS_PER_PAGE)

    context = {
        'questions': page_obj,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'hot-questions.html', context)


def question(request, question_id):
    question = Question.objects.get_question(question_id)
    answers = list(Answer.objects.get_answers(question_id))
    page_obj = paginate(answers, request, per_page=ANSWERS_PER_PAGE)

    answer_form = AnswerForm(request.user, question)

    context = {
        'form': answer_form,
        'question': question,
        'answers': page_obj,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'question-details.html', context)


@login_required(login_url='login', redirect_field_name='continue')
@require_POST
@csrf_protect
def answer(request, question_id):
    question = Question.objects.get_question(question_id)
    answer_form = AnswerForm(request.user, question, request.POST)
    if answer_form.is_valid():
        answer = answer_form.save()
        answers_count = Answer.objects.get_answers(question_id).count()
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
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
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
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
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
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'signup.html', context)


def questions_by_tag(request, tag_name):
    questions = list(Question.objects.questions_by_tag(tag_name))
    page_obj = paginate(questions, request, per_page=QUESTIONS_PER_PAGE)

    context = {
        'questions': page_obj,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
        'tag_name': tag_name,
    }

    return render(request, 'tag.html', context)


@login_required(login_url='login', redirect_field_name='continue')
@require_http_methods(['GET', 'POST'])
@csrf_protect
def profile(request):
    profile_form = ProfileForm(initial=model_to_dict(request.user))
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, files=request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse('profile'))

    context = {
        'form': profile_form,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'profile.html', context)
