import django_filters
from .models import Job

class JobFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = [
            'title',
            'description',
            'categories',
            'min_salary',
            'max_salary',
            'vacancy',
            'min_experience',
            'max_experience',
            'career_level',
            'job_type',
            'published_at',
            ]