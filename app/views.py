from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, InvalidPage


POPULAR_TAGS = [f'Tag-{i}' for i in range(10)]
BEST_MEMBERS = [f'Member-{i}' for i in range(5)]

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'text': f'This is question number {i}.',
        'tags': {f'Tag-{i}' for i in range(5)},
        'answers': [f'Comment {j}' for j in range(30)],
    } for i in range(100)
]


def paginate(items, request, *, per_page=5):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(items, per_page)

    try:
        page_obj = paginator.page(page_number)
    except (EmptyPage, InvalidPage):
        page_obj = paginator.page(1)

    return page_obj


def index(request):
    page_obj = paginate(QUESTIONS, request)

    return render(request, 'index.html', {
        'questions': page_obj,
        'authorized': True,
        'popular_tags': POPULAR_TAGS,
        'best_members': BEST_MEMBERS,
    })


def hot_questions(request):
    questions = QUESTIONS[:10]
    page_obj = paginate(questions, request)

    return render(request, 'hot-questions.html', {
        'questions': page_obj,
        'authorized': True,
        'popular_tags': POPULAR_TAGS,
        'best_members': BEST_MEMBERS,
    })


def question(request, question_id):
    question = QUESTIONS[question_id]
    page_obj = paginate(question['answers'], request)

    return render(request, 'question-details.html', {
        'question': question,
        'answers': page_obj,
        'authorized': True,
        'popular_tags': POPULAR_TAGS,
        'best_members': BEST_MEMBERS,
    })


def ask(request):
    return render(request, 'ask.html', {
        'authorized': True,
        'error': None,
        'popular_tags': POPULAR_TAGS,
        'best_members': BEST_MEMBERS,
    })


def login(request):
    return render(request, 'login.html', {
        'authorized': True,
        'error': None,
        'popular_tags': POPULAR_TAGS,
        'best_members': BEST_MEMBERS,
    })


def signup(request):
    return render(request, 'signup.html', {
        'authorized': True,
        'error': None,
        'popular_tags': POPULAR_TAGS,
        'best_members': BEST_MEMBERS,
    })


def questions_by_tag(request, tag_name):
    questions = [question for question in QUESTIONS if tag_name in question['tags']]
    page_obj = paginate(questions, request)

    return render(request, 'tag.html', {
        'questions': page_obj,
        'authorized': True,
        'popular_tags': POPULAR_TAGS,
        'best_members': BEST_MEMBERS,
        'tag_name': tag_name,
    })


def settings(request):
    return render(request, 'settings.html', {
        'authorized': True,
        'error': None,
        'popular_tags': POPULAR_TAGS,
        'best_members': BEST_MEMBERS,
    })
