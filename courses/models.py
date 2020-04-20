from django.conf import settings
from django.db import models
from django.urls import reverse

class CourseManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query)
        )

class Course(models.Model):
    name = models.CharField('Nome', max_length=255)
    slug = models.SlugField('Url')
    description = models.TextField('Descrição', blank=True)
    about = models.TextField('Sobre o Curso', blank=True)
    startDate = models.DateField('Data de Início', blank=True, null=True)
    thumbnail = models.ImageField(null=True, blank=True)
    createdAt = models.DateTimeField('Criado em', auto_now_add=True)
    updatedAt = models.DateTimeField('Atualizado em', auto_now=True)

    objects = CourseManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['name']


class Enrollment(models.Model):
    STATUS_CHOICE = ((0, 'Pendente'),
                     (1, 'Aprovado'),
                     (2, 'Cancelado'))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', related_name='enrollments', on_delete=None)
    course = models.ForeignKey(Course, verbose_name='Curso', related_name='enrollments',on_delete=None)
    status = models.IntegerField('Situação', choices=STATUS_CHOICE, default=0, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def active(self):
        self.status = 1
        self.save()

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('user', 'course'),)
