# news/views.py
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import Author, Post, News

# Список плохих слов для цензурирования
bad_names = ['incidents', 'Дурак', 'Гад']

def censor(text):
    if not isinstance(text, str):
        raise ValueError("Фильтр может применяться только к строковым переменным.")
    for word in bad_names:
        text = text.replace(word, '*' * len(word))  # Цензурируем слова
    return text

class AuthorsPage(ListView):
    model = Author
    context_object_name = "Authors"
    template_name = 'news/authors.html'

class PostDetail(View):
    def get(self, request, pk):
        ps = Post.objects.get(id=pk)
        return render(request, "news/posts.html", {'ps': ps})

def news_page_list(request):
    """ Представление для вывода страницы с новостями по заданию 6.1 """
    newslist = Post.objects.all().order_by('-rating')[:6]
    return render(request, 'news/news.html', {'newslist': newslist})

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def news_list(request):
    news_list = News.objects.all().order_by('-date')
    for news in news_list:
        news.title = censor(news.title)  # Цензурируем заголовок
        news.content = censor(news.content[:20])  # Показываем только 20 символов
    return render(request, 'news/news_list.html', {'news_list': news_list})

def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    news.title = censor(news.title)
    news.content = censor(news.content)  # Цензурируем полный текст
    return render(request, 'news/news_detail.html', {'news': news})