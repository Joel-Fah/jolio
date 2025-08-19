import re

from django.db import models
from slugify import slugify
from django.utils.html import strip_tags

from core.utils import time_since


# Create your models here.

class Project(models.Model):
    class ProjectType(models.TextChoices):
        PERSONAL = "personal", "Personal"
        CONTRACT = "contract", "Contract"
        COMMUNITY = "community", "Community"
        OPEN_SOURCE = "open_source", "Open Source"

    class Category(models.TextChoices):
        DESIGN = "design", "Design"
        DEVELOPMENT = "development", "Development"
        MIXED = "mixed", "Mixed"

    title = models.CharField(max_length=255, help_text="Project title")
    slug = models.SlugField(unique=True, help_text="Unique URL-friendly identifier <i>(auto-generated)</i>")
    description = models.TextField(blank=True, null=True, help_text="Brief project description")
    project_type = models.CharField(
        max_length=20, choices=ProjectType.choices, default=ProjectType.PERSONAL, help_text="Project type"
    )
    category = models.CharField(
        max_length=20, choices=Category.choices, default=Category.MIXED, help_text="Project category"
    )
    client_name = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="Leave empty for personal projects"
    )
    cover_image = models.ImageField(
        upload_to="projects/covers/", blank=True, null=True
    )
    created_at = models.DateField(auto_now_add=True, help_text="Project creation date")
    updated_at = models.DateField(auto_now=True, help_text="Project last update date")
    is_published = models.BooleanField(default=True, help_text="Is the project visible on the site?")

    # optional extras
    live_url = models.URLField(blank=True, null=True, help_text="Project live URL")
    repo_url = models.URLField(blank=True, null=True, help_text="Project repository URL")

    def get_read_time(self):
        """
        Calculate estimated read time for the project description.
        Handles HTML content by stripping tags and calculating based on plain text.
        """
        # Return early if no description
        if not self.description:
            return 1

        # Strip HTML tags to get plain text
        plain_text = strip_tags(self.description)

        # Remove extra whitespace and newlines
        clean_text = re.sub(r'\s+', ' ', plain_text).strip()

        # Split into words (more accurate than simple split)
        words = re.findall(r'\b\w+\b', clean_text)
        total_words = len(words)

        # Average reading speed (words per minute)
        # 200-250 is typical for adults, using 200 for conservative estimate
        wpm = 200

        # Calculate minutes, rounding up using ceiling division
        if total_words == 0:
            return 1

        minutes = (total_words + wpm - 1) // wpm

        # Ensure minimum 1 minute read time
        return max(minutes, 1)

    def time_since_created(self):
        """Return human-readable time since project was created."""
        return time_since(self.created_at)

    def time_since_updated(self):
        """Return human-readable time since project was last updated."""
        return time_since(self.updated_at)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProjectMedia(models.Model):
    project = models.ForeignKey(Project, related_name="media", on_delete=models.CASCADE, help_text="Associated project")
    image = models.ImageField(upload_to="projects/media/")
    caption = models.CharField(max_length=255, blank=True, null=True, help_text="Optional caption for the media")

    def __str__(self):
        return f"{self.project.title} - {self.caption or 'Media'}"


class ProjectTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    projects = models.ManyToManyField(Project, related_name="tags")

    def __str__(self):
        return self.name
