from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(verbose_name="Название категории", max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default="Без категории")
    title = models.CharField(verbose_name="Название поста", max_length=100)
    expert = models.TextField(verbose_name="Рецензия", null=True)
    content = models.TextField(verbose_name="Текст поста")
    slug = models.SlugField(max_length=250, unique_for_date='published')
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    options = (('draft', 'draft'),
               ('published', 'published'),
               )
    status = models.CharField(max_length=10, choices=options, default='published')
    objects = models.Manager()
    postobjects = PostObjects()

    class Meta:
        ordering = ('-published',)
