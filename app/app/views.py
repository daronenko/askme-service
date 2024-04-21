from app.models import Question, Answer, Tag, Profile, User
from app.forms import LoginForm, SignupForm, SettingsForm

from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.urls import reverse
from django.forms import model_to_dict


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
    page_obj = paginate(new_questions, request)

    context = {
        'questions': page_obj,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'index.html', context)


def hot_questions(request):
    questions = list(Question.objects.hot_questions())
    page_obj = paginate(questions, request)

    context = {
        'questions': page_obj,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'hot-questions.html', context)


def question(request, question_id):
    question = Question.objects.get_question(question_id)
    answers = list(Answer.objects.get_answers(question_id))
    page_obj = paginate(answers, request)

    context = {
        'question': question,
        'answers': page_obj,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'question-details.html', context)


@login_required(login_url='login')
def ask(request):
    context = {
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'ask.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                redirect_to = request.GET.get('next', reverse('index'))
                return redirect(redirect_to)

    context = {
        'form': login_form,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'login.html', context)


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER', 'index'))


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
    page_obj = paginate(questions, request)

    context = {
        'questions': page_obj,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
        'tag_name': tag_name,
    }

    return render(request, 'tag.html', context)


@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def settings(request):
    settings_form = SettingsForm(initial=model_to_dict(request.user))
    if request.method == 'POST':
        settings_form = SettingsForm(request.POST, files=request.FILES, instance=request.user)
        if settings_form.is_valid():
            settings_form.save()
            return redirect(reverse('settings'))

    context = {
        'form': settings_form,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'settings.html', context)
