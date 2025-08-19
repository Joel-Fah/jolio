from datetime import datetime, timedelta
from django.utils import timezone


def date_formatter(date: datetime) -> str:
    """
    This function takes a date object and returns a string representation of the date in the format 'Thursday 19 August 2021'.

    Args:
        date (datetime): The date to format.

    Returns:
        str: The formatted date string.
    """
    return date.strftime('%A %d %B %Y')


def short_date_formatter(date: datetime) -> str:
    """
        This function takes a date object and returns a string representation of the date in the format 'Mon. 19 Aug. 2021'.

        Args:
            date (datetime): The date to format.

        Returns:
            str: The formatted date string.
        """
    return date.strftime('%a. %d %b. %Y')


def time_formatter(time: datetime) -> str:
    """
    This function takes a time object and returns a string representation of the time in the format '12:00 PM'.

    Args:
        time (datetime): The time to format.

    Returns:
        str: The formatted time string.
    """
    return time.strftime('%I:%M %p')


def datetime_formatter(date_time: datetime) -> str:
    """
    This function takes a datetime object and returns a string representation of the datetime in the format 'Thursday 19 August 2021, 12:00 PM'.

    Args:
        date_time (datetime): The datetime to format.

    Returns:
        str: The formatted datetime string.
    """
    return f"{date_formatter(date_time)} at {time_formatter(date_time)}"


def time_since(date):
    """
    Calculate human-readable time since a given date.
    Returns a string like "2 days ago", "1 hour ago", etc.
    """
    if not date:
        return "Unknown"

    # Ensure we're working with timezone-aware datetime
    if isinstance(date, datetime):
        now = timezone.now()
        if timezone.is_naive(date):
            date = timezone.make_aware(date)
    else:
        # If it's a date object, convert to datetime at start of day
        now = timezone.now().date()
        date = date

    # Calculate the difference
    if isinstance(date, datetime):
        diff = now - date
    else:
        diff = now - date
        # Convert to timedelta for consistent handling
        diff = timedelta(days=diff.days)

    # Handle future dates
    if diff.total_seconds() < 0:
        return "In the future"

    # Calculate time units
    seconds = int(diff.total_seconds())
    minutes = seconds // 60
    hours = minutes // 60
    days = diff.days
    weeks = days // 7
    months = days // 30
    years = days // 365

    # Return appropriate time string with pluralization
    if years > 0:
        return f"{years} year{'s' if years != 1 else ''} ago"
    elif months > 0:
        return f"{months} month{'s' if months != 1 else ''} ago"
    elif weeks > 0:
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    elif days > 0:
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif hours > 0:
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif minutes > 0:
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    else:
        return "Just now"
