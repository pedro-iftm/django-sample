from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

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
    start_date = models.DateField('Data de Início', blank=True, null=True)
    thumbnail = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    objects = CourseManager()

    def release_lessons(self):
        today = timezone.now().date()
        return self.lessons.filter(release_date__gte=today)

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
    
    def is_approved(self):
        return self.status == 1

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        unique_together = (('user', 'course'),)

class Lesson(models.Model):
    name = models.CharField('Nome', max_length=100)
    description = models.TextField('Descrição', blank=True)
    number = models.IntegerField('Número(ordem)', blank=True, default=0)
    release_date = models.DateField('Data de liberação', blank=True, null=True)
    course = models.ForeignKey(Course, verbose_name='Curso', related_name='lessons', on_delete=None)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    def is_available(self):
        if self.release_date:
            today = timezone.now().date()
            return self.release_date >= today
        return False

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['number']


class Material(models.Model):
    name = models.CharField('Nome', max_length=100)
    embedded = models.TextField('Vídeo embedded', blank=True, null=True)
    file = models.FileField(upload_to='lessons/materials', null=True, blank=True)
    lesson = models.ForeignKey(Lesson, verbose_name='Aula', related_name='materials', on_delete=None)

    def is_embedded(self):
        return bool(self.embedded)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'

