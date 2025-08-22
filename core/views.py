from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Project, Achievement, Skill


# Create your views here.

class HomeView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_project = Project.objects.filter(is_published=True).order_by('-created_at').first()
        context['latest_project'] = latest_project

        # Exclude the latest project from featured projects
        featured_projects_queryset = Project.objects.filter(is_published=True).order_by('-created_at')
        if latest_project:
            featured_projects_queryset = featured_projects_queryset.exclude(id=latest_project.id)
        context['featured_projects'] = featured_projects_queryset[:4]
        context['skills'] = Skill.objects.all().filter(is_published=True).order_by('name')

        return context


class ProjectsView(ListView):
    template_name = 'core/projects/projects.html'
    model = Project
    context_object_name = 'projects'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_published=True)


class ProjectDetailView(DetailView):
    template_name = 'core/projects/project_details.html'
    model = Project
    context_object_name = 'project'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('media', 'tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        # Use the related_name from your models
        context['media'] = project.media.all()
        context['tags'] = project.tags.all()
        context['related_projects'] = Project.objects.filter(tags__in=project.tags.all(),
                                                             category=project.category).exclude(
            id=project.id).distinct()[:4]
        return context


class AchievementsView(ListView):
    template_name = 'core/achievements.html'
    model = Achievement
    context_object_name = 'achievements'
    paginate_by = 10
    ordering = ['-created_at', '-event_date']

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('tags')
        return queryset.filter(is_published=True)


# State views
def handler404(request, exception=None):
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    return render(request, 'errors/500.html', status=500)
