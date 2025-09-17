from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.db import models
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.contrib.forms.widgets import WysiwygWidget

from core.models import Project, Tag, ProjectMedia, Achievement, Skill, Update, Story

# Register your models here.
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(Update)
class UpdateAdmin(ModelAdmin):
    list_display = ['is_available_for_work', 'updated_at']
    readonly_fields = ['updated_at']


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ['title', 'project_type', 'category', 'updated_at', 'is_published']
    search_fields = ['title', 'description', 'client_name']
    list_filter = ['project_type', 'category', 'is_published', 'created_at', 'updated_at']
    ordering = ['-created_at']

    readonly_fields = ['slug', 'created_at', 'updated_at']

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

    readonly_fields = ['slug', 'created_at', 'updated_at']

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


class SubStoryInline(StackedInline):  # or StackedInline if you want bigger forms
    model = Story
    fk_name = "parent"  # important: tell Django which FK to use
    extra = 1  # how many empty forms to show by default


@admin.register(Story)
class StoryAdmin(ModelAdmin):
    list_display = ['title', 'created_at', 'is_published', 'is_parent_node']
    search_fields = ['title', 'content']
    list_filter = ['is_published', 'created_at']
    ordering = ['-created_at']

    # Only show inline for root stories
    inlines = [SubStoryInline]

    readonly_fields = ['created_at', 'updated_at']

    formfield_overrides = {
        models.TextField: {'widget': WysiwygWidget},
    }

    def is_parent_node(self, obj):
        return "Parent" if obj.parent is None else ""

    def get_inlines(self, request, obj=None):
        if obj and obj.parent is None:  # only top-level stories get inline editing
            return [SubStoryInline]
        return []
