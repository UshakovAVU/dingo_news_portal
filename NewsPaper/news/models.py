from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

CATEGORY_CHOISES = [
    ('ARTICLE', 'Article'),
    ('NEWS', 'News'),
]


class Author(models.Model):
    """
    Модель Author
    имеет следующие поля:
    - <authorUser> связь «один к одному» с встроенной моделью пользователей User;
    - <ratingAuthor> рейтинг пользователя.
    """
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        """
        update_rating() обновляет рейтинг пользователя.
        Рейтинг состоит из:
        - суммарный рейтинг каждой статьи автора умножается на 3;
        - суммарный рейтинг всех комментариев автора;
        - суммарный рейтинг всех комментариев к статьям автора.
        """
        # Суммируем рейтинг постов автора, умноженное на 3
        postR = self.post_set.aggregate(postRating=Sum('rating'))
        post_rating = (postR.get('postRating') or 0) * 3

        # Суммируем рейтинг комментариев самого автора
        commentR = self.authorUser.comment_set.all().aggregate(commentRating=Sum('rating'))

        # Суммируем рейтинг комментариев к статьям автора
        comments_from_posts = Comment.objects.filter(commentPost__author=self).aggregate(
            postCommentRating=Sum('rating'))

        # Итоговый рейтинг комментариев
        comment_rating = (commentR.get('commentRating') or 0) + (comments_from_posts.get('postCommentRating') or 0)

        # Обновляем рейтинг автора
        self.ratingAuthor = post_rating + comment_rating
        self.save()

    def __str__(self):
        return f"{self.authorUser}"


class Category(models.Model):
    """
    Модель Category
    Темы, которые они отражают (спорт, политика, образование и т. д.).
    Имеет единственное поле: название категории.
    - <name> Поле должно быть уникальным (в определении поля необходимо написать параметр unique = True).
    """
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name}"


class Post(models.Model):
    """
    Модель Post
    Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
    Каждый объект может иметь одну или несколько категорий.
    """
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categoryType = models.CharField(max_length=20, choices=CATEGORY_CHOISES, default='ARTICLE')
    created_at = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        """Увеличивает рейтинг на единицу."""
        self.rating += 1
        self.save()

    def dislike(self):
        """Уменьшает рейтинг на единицу."""
        if self.rating > 0:
            self.rating -= 1
        self.save()

    def preview(self):
        """Возвращает предварительный просмотр статьи длиной 124 символа и добавляет многоточие в конце."""
        return self.text[:124] + '...'

    def __str__(self):
        dataf = f'Post from {self.created_at.strftime("%d.%m.%Y %H:%M")}'
        return f"{dataf}, {self.author}, {self.title}"


class PostCategory(models.Model):
    """
    Модель PostCategory
    Промежуточная модель для связи «многие ко многим».
    """
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.postThrough}, from the category: {self.categoryThrough}"


class Comment(models.Model):
    """
    Модель Comment
    Хранит комментарии под статьями/новостями.
    """
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    userPost = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dataCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        """Увеличивает рейтинг комментария на единицу."""
        self.rating += 1
        self.save()

    def dislike(self):
        """Уменьшает рейтинг комментария на единицу."""
        if self.rating > 0:
            self.rating -= 1
        self.save()

    def __str__(self):
        return f"{self.dataCreation}, {self.userPost}"