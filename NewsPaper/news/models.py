from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Исправлено на CATEGORY_CHOICES
CATEGORY_CHOICES = [
    ('ARTICLE', 'Article'),
    ('NEWS', 'News'),
]

class Author(models.Model):
    """ Модель Author, имеет связь с пользователем. """
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        """ Обновляет рейтинг автора на основе рейтинга его постов и комментариев. """
        postR = self.post_set.aggregate(postRating=Sum('rating'))
        post_rating = (postR.get('postRating') or 0) * 3

        commentR = self.authorUser.comment_set.all().aggregate(commentRating=Sum('rating'))
        comments_from_posts = Comment.objects.filter(commentPost__author=self).aggregate(
            postCommentRating=Sum('rating'))

        comment_rating = (commentR.get('commentRating') or 0) + (comments_from_posts.get('postCommentRating') or 0)
        self.ratingAuthor = post_rating + comment_rating
        self.save()

    def __str__(self):
        return f"{self.authorUser}"

class Category(models.Model):
    """ Модель Category для указания категорий постов. """
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name}"

class Post(models.Model):
    """ Модель Post для статей и новостей, создаваемых пользователями. """
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categoryType = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='ARTICLE')
    created_at = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.author.authorUser.username}"

class News(models.Model):
    """ Модель News для новостных статей. """
    title = models.CharField(max_length=255)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ['-date']  # Сортировка по дате

    def like(self):
        """ Увеличивает рейтинг на единицу. """
        self.rating += 1
        self.save()

    def dislike(self):
        """ Уменьшает рейтинг на единицу. """
        if self.rating > 0:
            self.rating -= 1
        self.save()

    def preview(self):
        """ Возвращает предварительный просмотр текста. """
        return self.text[:124] + '...'

    def __str__(self):
        return f"{self.title} (Date: {self.date.strftime('%d.%m.%Y')})"

class PostCategory(models.Model):
    """ Модель для связи постов и категорий. """
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.postThrough.title} from category: {self.categoryThrough.name}"

class Comment(models.Model):
    """ Модель Comment для комментариев под постами. """
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    userPost = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dataCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        """ Увеличивает рейтинг комментария. """
        self.rating += 1
        self.save()

    def dislike(self):
        """ Уменьшает рейтинг комментария. """
        if self.rating > 0:
            self.rating -= 1
        self.save()

    def __str__(self):
        return f"{self.userPost.username} on {self.dataCreation}: {self.text[:20]}"