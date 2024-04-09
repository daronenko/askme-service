from app.models import Question, Answer, Tag, Profile, User

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, InvalidPage

try:
    CURRENT_USER = User.objects.get(pk=1)
except:
    CURRENT_USER = None


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
        'user': CURRENT_USER,
        'questions': page_obj,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'index.html', context)


def hot_questions(request):
    questions = list(Question.objects.hot_questions())
    page_obj = paginate(questions, request)

    context = {
        'user': CURRENT_USER,
        'questions': page_obj,
        'authorized': True,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'hot-questions.html', context)


def question(request, question_id):
    question = Question.objects.get_question(question_id)
    answers = list(Answer.objects.get_answers(question_id))
    page_obj = paginate(answers, request)

    context = {
        'user': CURRENT_USER,
        'question': question,
        'answers': page_obj,
        'authorized': True,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'question-details.html', context)


def ask(request):
    context = {
        'user': CURRENT_USER,
        'authorized': True,
        'error': None,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'ask.html', context)


def login(request):
    context = {
        'user': CURRENT_USER,
        'authorized': True,
        'error': None,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'login.html', context)


def signup(request):
    context = {
        'user': CURRENT_USER,
        'authorized': True,
        'error': None,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'signup.html', context)


def questions_by_tag(request, tag_name):
    questions = list(Question.objects.questions_by_tag(tag_name))
    page_obj = paginate(questions, request)

    context = {
        'user': CURRENT_USER,
        'questions': page_obj,
        'authorized': True,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
        'tag_name': tag_name,
    }

    return render(request, 'tag.html', context)


def settings(request):
    context = {
        'user': CURRENT_USER,
        'authorized': True,
        'error': None,
        'popular_tags': Tag.objects.get_popular_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'settings.html', context)
