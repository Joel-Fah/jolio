import re

from django.db import models
from slugify import slugify
from django.utils.html import strip_tags

from core.utils import time_since


# Create your models here.

class Project(models.Model):
    """
    Represents a project with various attributes like title, description, type, category, etc.
    Provides methods for calculating read time, time since creation/update, and auto-generating slugs.
    Attributes:
        title (str): The title of the project.
        slug (str): A unique URL-friendly identifier for the project, auto-generated from the title.
        description (str): A brief description of the project.
        project_type (str): The type of project, e.g., personal, contract, community, open source.
        category (str): The category of the project, e.g., design, development, mixed.
        client_name (str): Name of the client for contract projects; optional for personal projects.
        cover_image (ImageField): An optional cover image for the project.
        created_at (date): The date when the project was created.
        updated_at (date): The date when the project was last updated.
        is_published (bool): Whether the project is visible on the site.
        live_url (str): Optional URL to view the live project.
        repo_url (str): Optional URL to view the project's repository.
    Methods:
        get_read_time(): Calculates the estimated read time for the project description.
        time_since_created(): Returns a human-readable string of time since the project was created.
        time_since_updated(): Returns a human-readable string of time since the project was last updated.
        save(): Auto-generates the slug from the title before saving.
    """

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
    tags = models.ManyToManyField('Tag', blank=True, related_name="projects")
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
    """
    Represents media associated with a project, such as images or videos.
    Attributes:
        project (ForeignKey): The project this media belongs to.
        image (ImageField): The media file, typically an image.
        caption (str): Optional caption for the media.
    Provides a string representation of the media in the format "Project Title - Caption".
    """
    project = models.ForeignKey(Project, related_name="media", on_delete=models.CASCADE, help_text="Associated project")
    image = models.ImageField(upload_to="projects/media/")
    caption = models.CharField(max_length=255, blank=True, null=True, help_text="Optional caption for the media")

    class Meta:
        verbose_name = "Project Media"
        verbose_name_plural = "Project Media"
        ordering = ["project__title"]

    def __str__(self):
        return f"{self.project.title} - {self.caption or 'Media'}"


class Tag(models.Model):
    """
    Represents a tag that can be associated with projects or achievements.
    Attributes:
        name (str): The name of the tag, must be unique.
    Provides a string representation of the tag name.
    Provides ordering by name.
    """
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Achievement(models.Model):
    """
    Represents an achievement with various attributes like title, content, image, tags, and event date.
    Provides methods for calculating time since creation, update, and event date.
    Attributes:
        title (str): The title of the achievement.
        slug (str): A unique URL-friendly identifier for the achievement, auto-generated from the title.
        content (str): A description of the achievement.
        image (ImageField): An optional image associated with the achievement.
        tags (ManyToManyField): Tags associated with the achievement.
        link (URLField): Optional link for more information about the achievement.
        event_date (DateField): Date of the event related to the achievement, if applicable.
        created_at (DateTimeField): The date and time when the achievement was created.
        updated_at (DateField): The date when the achievement was last updated.
        is_published (bool): Whether the achievement is visible on the site.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField(help_text="Achievement description")
    image = models.ImageField(upload_to="achievements/", blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="achievements")
    link = models.URLField(blank=True, null=True)
    event_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True, help_text="Achievement last update date")
    is_published = models.BooleanField(default=True, help_text="Is the achievement visible on the site?")

    class Meta:
        ordering = ["-created_at", "-event_date"]

    def time_since_created(self):
        """Return human-readable time since project was created."""
        return time_since(self.created_at)

    def time_since_updated(self):
        """Return human-readable time since project was last updated."""
        return time_since(self.updated_at)

    def time_since_event(self):
        """Return human-readable time since the event date."""
        if self.event_date:
            return time_since(self.event_date)
        return "N/A"

    def save(self, *args, **kwargs):
        if not self.slug:  # auto-generate slug if missing
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Skill(models.Model):
    """
    Represents a skill with a name and optional description.
    Attributes:
        name (str): The name of the skill, must be unique.
        description (str): Optional description of the skill.
    Provides a string representation of the skill name.
    Provides ordering by name.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True, help_text="Skill last update date")
    is_published = models.BooleanField(default=True, help_text="Is the skill visible on the site?")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name