from django.urls import path

from app import views


urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot_questions, name='hot_questions'),
    path('question/<int:question_id>', views.question, name='question'),
]
