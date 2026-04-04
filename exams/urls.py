from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    path('', views.exam_list, name='list'),
    path('listening/', views.listening_list, name='listening_list'),
    path('reading/', views.reading_list, name='reading_list'),
    path('writing/', views.writing_list, name='writing_list'),
    path('speaking/', views.speaking_list, name='speaking_list'),
    path('practice/reading/', views.practice_reading, name='practice_reading'),
    path('practice/writing/', views.practice_writing, name='practice_writing'),
    path('practice/listening/', views.practice_listening, name='practice_listening'),
    path('ai-assistant/', views.ai_assistant, name='ai_assistant'),
    path('api/ai-chat/', views.ai_chat, name='ai_chat'),
    path('api/ai-check-writing/', views.ai_check_writing, name='ai_check_writing'),
    path('articles/', views.articles_list, name='articles'),
    path('article/<str:slug>/', views.article_view, name='article'),
    path('start/<int:exam_id>/', views.start_exam, name='start'),
    path('<int:attempt_id>/<str:section_type>/', views.exam_section, name='section'),
    path('<int:attempt_id>/auto-save/', views.auto_save, name='auto_save'),
    path('<int:attempt_id>/submit/<str:section_type>/', views.submit_section, name='submit_section'),
    path('<int:attempt_id>/upload-speaking/<int:question_id>/', views.upload_speaking, name='upload_speaking'),
]
