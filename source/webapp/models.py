from django.db import models

from django.db import models

ACCESS_CHOICES = (
    ('common', 'Обычный'),
    ('hidden', 'Скрытый'),
    ('private', 'Приватный'),
)


class File(models.Model):
    file = models.FileField(upload_to='user_file', verbose_name='Файл')
    name = models.CharField(max_length=50, verbose_name='Подпись к файлу')
    author = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='author_file', verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    general_access = models.CharField(max_length=50, choices=ACCESS_CHOICES, default=ACCESS_CHOICES[0][0],
                                      verbose_name='Общий доступ')
    users_private = models.ManyToManyField('auth.User', related_name='file_private', verbose_name='Приват')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'