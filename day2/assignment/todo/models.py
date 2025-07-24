from django.db import models

class Todo(models.Model):
    title = models.CharField('제목',max_length=50)
    description = models.TextField('설명')
    start_date = models.DateField('시작일')
    end_date = models.DateField('마감일')
    is_completed = models.BooleanField('완료 여부',default=False)
    created_at = models.DateTimeField('생성 시간',auto_now_add=True)
    updated_at = models.DateTimeField('수정 시간',auto_now=True)

    def __str__(self):
        return self.title

    class Meta :
        verbose_name = 'Todo'
        verbose_name_plural = 'Todo 목록'

