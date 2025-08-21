from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from core.models import Project, Tag, ProjectMedia, Achievement, Skill


# Register your models here.
@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ['title', 'project_type', 'category', 'updated_at', 'is_published']
    search_fields = ['title', 'description', 'client_name']
    list_filter = ['project_type', 'category', 'is_published', 'created_at', 'updated_at']
    ordering = ['-created_at']

    readonly_fields = ['slug']

    formfield_overrides = {
        models.TextField: {'widget': WysiwygWidget},
    }


@admin.register(ProjectMedia)
class ProjectMediaAdmin(ModelAdmin):
    list_display = ['project', 'caption']
    search_fields = ['project__title', 'caption']
    list_filter = ['project']
    ordering = ['project__title']


@admin.register(Tag)
class ProjectTagAdmin(ModelAdmin):
    list_display = ['name', 'get_project_count', 'get_projects']
    search_fields = ['name']
    list_filter = ['projects']
    ordering = ['name']

    def get_projects(self, obj):
        projects = obj.projects.all()
        if projects:
            project_titles = ', '.join([project.title for project in projects])
            return project_titles
        return 'No projects'

    def get_project_count(self, obj):
        return obj.projects.count()

    get_projects.short_description = 'Associated Projects'
    get_project_count.short_description = 'Project Count'


@admin.register(Achievement)
class AchievementAdmin(ModelAdmin):
    list_display = ['title', 'event_date', 'is_published', 'created_at']
    search_fields = ['title', 'content']
    list_filter = ['is_published', 'event_date', 'created_at']
    ordering = ['-created_at', '-event_date']

    readonly_fields = ['slug']

    formfield_overrides = {
        models.TextField: {'widget': WysiwygWidget},
    }


@admin.register(Skill)
class SkillAdmin(ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at', 'is_published']
    ordering = ['name', '-created_at']


    formfield_overrides = {
        models.TextField: {'widget': WysiwygWidget},
    }
