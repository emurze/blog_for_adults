from django.db import models

from .porno_star import PornoStar


class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Comment.Status.PUBLISHED)


class CommentUser(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField()

    def __str__(self) -> str:
        return f"{self.name}"


class Comment(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DR', 'Draft'
        FIXING = 'FX', 'Fixing'
        PUBLISHED = 'PB', 'Publish'

    pornostar = models.ForeignKey(PornoStar, on_delete=models.CASCADE,
                                  related_name="comments")
    comment_user = models.OneToOneField(CommentUser, on_delete=models.CASCADE,
                                        related_name='comment')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices,
                              default=Status.PUBLISHED)

    objects = models.Manager()
    published = CustomManager()

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self) -> str:
        return f"Comment written by {self.comment_user.name} " \
               f"on {self.pornostar.name}"
