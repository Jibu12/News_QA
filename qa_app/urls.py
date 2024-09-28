# urls.py
from django.urls import path
from .views import question_answer_view

urlpatterns = [
    path('q_and_a/', question_answer_view, name='q_and_a')
]
