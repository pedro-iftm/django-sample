from django.contrib import admin
from .models import Course, Lesson, Material, Enrollment


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'start_date', 'created_at']
    search_fields = ['name', 'slug']


class MaterialInlineAdmin(admin.TabularInline):
    model = Material


class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'course', 'release_date']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    inlines = [MaterialInlineAdmin]


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register([Material, Enrollment])