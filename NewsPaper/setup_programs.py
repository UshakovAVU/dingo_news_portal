# setup_programs.py - название файла
# Скрипт для создания тестовых данных в Django проекте
# python setup_programs.py
# Импортируем необходимые модули
import os
import django
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')
django.setup()

from django.contrib.auth.models import User
from news.models import Author, Category, Post, Comment


def create_test_data():
    # Начало транзакции
    try:
        with transaction.atomic():
            # Создание пользователей
            print("Создание пользователей...")
            u1 = User.objects.create_user(username='User1')
            u2 = User.objects.create_user(username='User2')

            # Создание авторов
            print("Создание авторов...")
            author1 = Author.objects.create(user=u1)
            author2 = Author.objects.create(user=u2)

            # Создание категорий
            print("Создание категорий...")
            categories = ['Politics', 'Economy', 'Incidents', 'Culture']
            for cat in categories:
                Category.objects.get_or_create(name=cat)  # Обработка создания категорий

            # Создание постов
            print("Создание постов...")
            post1 = Post.objects.create(
                author=author1,
                category_type='AR',  # Исправлено на category_type или другое актуальное поле
                title='The article of the first author',
                text='here is the first text of the first author about incidents and politics'
            )

            post2 = Post.objects.create(
                author=author2,
                category_type='AR',  # Исправлено на category_type или другое актуальное поле
                title='The article of the second author',
                text='here is the first text of the second author about culture'
            )

            # Назначение категорий постам
            print("Назначение категорий...")
            try:
                politics_category = Category.objects.get(name='Politics')
                incidents_category = Category.objects.get(name='Incidents')
                culture_category = Category.objects.get(name='Culture')

                post1.post_category.add(politics_category, incidents_category)  # Измените на правильное поле
                post2.post_category.add(culture_category)  # Измените на правильное поле
            except ObjectDoesNotExist as e:
                print(f"Ошибка при получении категорий: {e}")

            # Создание комментариев
            print("Создание комментариев...")
            Comment.objects.create(
                commentPost=post1,
                userPost=u1,
                text='comment on the policy in the first article from author 1'
            )

            Comment.objects.create(
                commentPost=post1,
                userPost=u2,
                text='comment on the policy in the first article from author 2'
            )

            Comment.objects.create(
                commentPost=post2,
                userPost=u1,
                text='comment on the Culture in the second article from author 1'
            )

            Comment.objects.create(
                commentPost=post2,
                userPost=u2,
                text='comment on the Culture in the second article from author 2'
            )

            # Работа с рейтингами
            print("Работа с рейтингами...")
            post1.like()
            post1.dislike()
            post2.like()
            post2.dislike()

            # Обновление рейтингов комментариев
            first_comment = Comment.objects.first()
            first_comment.like()
            first_comment.dislike()

            best_author = Author.objects.order_by('-ratingAuthor').first()
            print(f"Лучший пользователь: {best_author.user.username}, Рейтинг: {best_author.ratingAuthor}")

            best_post = Post.objects.order_by('-rating').first()
            print(f"Лучшая статья: {best_post.title}")

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


# Запуск скрипта
if __name__ == "__main__":
    create_test_data()