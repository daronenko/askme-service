from django.shortcuts import render

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'text': f'This is question number {i}.',
        'tags': ['python', 'vk-education', 'postgresql', 'django', 'duckduckgo', 'mail-ru'],
    } for i in range(5)
]


def index(request):
    return render(request, 'index.html', {'questions': QUESTIONS, 'authorized': True})
