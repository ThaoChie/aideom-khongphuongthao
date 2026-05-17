from django.urls import path
from . import views
urlpatterns = [
    path('health/', views.health),
    path('lessons/', views.lessons_list),
    path('lessons/<str:lesson_id>/', views.lesson_detail),
    path('lessons/<str:lesson_id>/run/', views.lesson_run),
    path('pipeline/run/', views.pipeline_run),
]
