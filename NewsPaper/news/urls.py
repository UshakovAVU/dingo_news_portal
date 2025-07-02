from django.urls import path
from .views import *
from . import views
from django.urls import path
from .views import NewsListView
from .views import NewsCreate, NewsUpdate, NewsDelete

urlpatterns = [
    path('', news_page_list),
    path('authors/', AuthorsPage.as_view()),
    path('post/<int:pk>/', PostDetail.as_view()),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
]
