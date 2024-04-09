from app import views

from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot_questions, name='hot_questions'),
    path('question/<int:question_id>', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('tag/<tag_name>/', views.questions_by_tag, name='tag'),
    path('settings/', views.settings, name='settings'),
]
