from django.urls import path
from .views import (
    NewsListView,
    NewsCreate,
    NewsUpdate,
    NewsDelete,
    ArticleCreate,
    ArticleUpdate,
    ArticleDelete,
    AuthorsPage,
    PostDetail,
    news_page_list,
    news_list,
    news_detail,
)

urlpatterns = [
    path('', news_page_list, name='homepage'),  # Главная страница с новостями
    path('authors/', AuthorsPage.as_view(), name='authors_page'),  # Страница авторов
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),  # Детали поста
    path('news/', NewsListView.as_view(), name='news_list'),  # Список новостей
    path('news/create/', NewsCreate.as_view(), name='news_create'),  # Создание новости
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),  # Редактирование новости
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),  # Удаление новости
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),  # Создание статьи
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),  # Редактирование статьи
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),  # Удаление статьи
    path('list/', news_list, name='news_page_list'),  # Дополнительная страница со списком новостей
    path('news/detail/<int:news_id>/', news_detail, name='news_detail'),  # Детали новости
]