from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin  # Импортируем миксин для проверки аутентификации
from .models import Author, Post, News
from .filters import NewsFilter  # Импортируем свой фильтр
from django.urls import reverse_lazy

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
        ps = get_object_or_404(Post, id=pk)
        return render(request, "news/posts.html", {'ps': ps})

class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10  # Количество новостей на странице

    def get_queryset(self):
        self.filterset = NewsFilter(self.request.GET, queryset=super().get_queryset())
        return self.filterset.qs

class NewsCreate(LoginRequiredMixin, CreateView):
    model = News
    fields = ['title', 'text']  # Укажите поля, которые нужно заполнить
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = 'news'  # Установка типа
        return super().form_valid(news)

class NewsUpdate(LoginRequiredMixin, UpdateView):
    model = News
    fields = ['title', 'text']  # Укажите поля для редактирования
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')

class NewsDelete(LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news_list')

# Новые классы для создания, редактирования и удаления статей
class ArticleCreate(LoginRequiredMixin, CreateView):
    model = News  # Используем ту же модель, что и для новостей
    fields = ['title', 'text']
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        article = form.save(commit=False)
        article.type = 'article'  # Устанавливаем тип как 'статья'
        return super().form_valid(article)

class ArticleUpdate(LoginRequiredMixin, UpdateView):
    model = News
    fields = ['title', 'text']
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')

class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news_list')

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
        news.text = censor(news.text[:20])  # Показываем только 20 символов
    return render(request, 'news/news_list.html', {'news_list': news_list})

def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    news.title = censor(news.title)
    news.text = censor(news.text)  # Цензурируем полный текст
    return render(request, 'news/news_detail.html', {'news': news})