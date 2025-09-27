from datetime import datetime

from django.views.generic.base import ContextMixin

from core.models import Update


# Create your mixins here.

class CommonContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_available_for_work'] = Update.objects.last().is_available_for_work if Update.objects.exists() else False
        context['copyright_year'] = datetime.now().year
        context['resume_url'] = Update.objects.last().resume.url if Update.objects.exists() and Update.objects.last().resume else None
        return context
