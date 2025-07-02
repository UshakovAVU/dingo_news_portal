from django.urls import path
from .views import *
from . import views
from django.urls import path
from .views import NewsListView
from .views import NewsCreate, NewsUpdate, NewsDelete
from .views import ArticleCreate, ArticleUpdate, ArticleDelete

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
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]
