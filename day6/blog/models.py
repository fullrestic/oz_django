from django.contrib.auth import get_user_model
from django.db import models

from utils.models import TimestampModel

User = get_user_model()

class Blog(TimestampModel):
    CATEGORY_CHOICES = (
    ('free', '자유'),
    ('travel', '여행'),
    ('cat', '고양이'),
    ('dog', '강아지'),
    )

    category = models.CharField('카테고리', max_length=10, choices=CATEGORY_CHOICES, default='free')
    title = models.CharField('제목', max_length=100)
    content = models.TextField('본문')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # models.CASCADE => 같이 삭제
    # models.PROTECT => 삭제 불가능 (유저를 삭제하려고 할 때 블로그가 있으면 삭제 불가능)
    # models.SET_NULL => 블로그의 author가 NULL이 됨

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title[:10]}"

    def get_absolute_url(self):
        from django.urls.base import reverse
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'


class Comment(TimestampModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.CharField('본문', max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.blog.title} 댓글'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ['-created_at', '-id']


