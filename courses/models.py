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