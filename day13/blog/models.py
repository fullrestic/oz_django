from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Manager, Q
from django.utils import timezone

from utils.models import TimestampModel

User = get_user_model()

class PublishedManager(Manager):
    def get_queryset(self):
        now = timezone.now()

        return super().get_queryset().filter(
            Q(published_at__isnull=True) |
            Q(published_at__lte=now)
        )   # publish 된 것만


class Blog(TimestampModel):
    title = models.CharField('제목', max_length=100)
    content = models.TextField('본문')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_at = models.DateTimeField('배포 일시', null=True, blank=True)

    objects = PublishedManager()
    all_objects = Manager() # all_objects는 원래 objects처럼 사용

    @property
    def is_active(self):
        now = timezone.now()

        if not self.published_at:
            return True

        return self.published_at <= now


    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'
        ordering = ('-created_at', '-id')


class Comment(TimestampModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField('본문')

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ('blog', '-created_at', '-id')