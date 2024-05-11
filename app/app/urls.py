from app import views

from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot_questions, name='hot_questions'),
    path('question/<int:question_id>', views.question, name='question'),
    path('question/<int:question_id>/answer', views.answer, name='answer'),
    path('answer/correct', views.correct, name='correct'),
    path('vote/', views.vote, name='vote'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('tag/<tag_name>/', views.questions_by_tag, name='tag'),
    path('profile/edit', views.profile, name='profile'),
]
