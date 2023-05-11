from typing import cast

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

from lorem import get_word
from taggit.managers import TaggableManager

User = get_user_model()


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=PornoStar.Status.PUBLISHED)


class PornoStar(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    name = models.CharField(max_length=64)
    slug = models.SlugField(unique_for_date='publish')
    content = models.TextField(default=get_word(count=100).capitalize())
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, related_name='pornostars',
                               on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='star/%Y/%m/%d/', null=True)
    status = models.CharField(max_length=2, choices=Status.choices,
                              default=Status.DRAFT)
    tags = TaggableManager()

    objects = models.Manager()
    published = PublishManager()

    class Meta:
        verbose_name = 'Pornostar'
        verbose_name_plural = 'Pornostars'
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['publish'])
        ]

    def __str__(self) -> str:
        return f"{self.name}"

    def get_absolute_url(self):
        pb = cast(timezone.now, self.publish)
        return reverse('blog:star_detail',
                       args=[pb.year, pb.month, pb.day, self.slug])
