from django.shortcuts import render, redirect
from django.core.paginator import Paginator


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


def index(request):
    page_num = request.GET.get('page', '1')
    paginator = Paginator(QUESTIONS, 5)

    if (not all(ch.isdigit() for ch in page_num)
            or not (1 <= int(page_num) <= paginator.num_pages)):
        return redirect('index')

    page_obj = paginator.page(page_num)
    return render(request, 'index.html', {
        'questions': page_obj,
        'authorized': True,
        'popular_tags': POPULAR_TAGS,
        'best_members': BEST_MEMBERS,
    })


def hot_questions(request):
    questions = QUESTIONS[:10]

    page_num = request.GET.get('page', '1')
    paginator = Paginator(questions, 5)

    if (not all(ch.isdigit() for ch in page_num)
            or not (1 <= int(page_num) <= paginator.num_pages)):
        return redirect('hot_questions')

    page_obj = paginator.page(page_num)

    return render(request, 'hot-questions.html', {
        'questions': page_obj,
        'authorized': True,
        'popular_tags': POPULAR_TAGS,
        'best_members': BEST_MEMBERS,
    })


def question(request, question_id):
    question = QUESTIONS[question_id]

    page_num = request.GET.get('page', '1')
    paginator = Paginator(question['answers'], 5)

    if (not all(ch.isdigit() for ch in page_num)
            or not (1 <= int(page_num) <= paginator.num_pages)):
        return redirect('question', question_id)

    page_obj = paginator.page(page_num)

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

    page_num = request.GET.get('page', '1')
    paginator = Paginator(questions, 5)

    if (not all(ch.isdigit() for ch in page_num)
            or not (1 <= int(page_num) <= paginator.num_pages)):
        return redirect('tag', tag_name)

    page_obj = paginator.page(page_num)

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
