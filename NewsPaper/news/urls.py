from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', news_page_list),
    path('authors/', AuthorsPage.as_view()),
    path('post/<int:pk>/', PostDetail.as_view()),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
]
