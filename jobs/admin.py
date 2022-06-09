from django.contrib import admin
from .models import Job, JobType, CarrerLevel, Category, Applies

class JobAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    fields =  [
            'owner',
            'title',
            'description',
            'country',
            'city',
            'categories',
            'image',
            ('min_salary',
            'max_salary',),
            'vacancy',
            ('min_experience',
            'max_experience',),
            'career_level',
            'job_type',
            'published_at',
            'created_at',
            'slug',
            'status',
            'active',
            ]
    search_fields = [
            'owner',
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
            'status',
            'active',
            ]

admin.site.register(Job, JobAdmin)
admin.site.register(CarrerLevel)
admin.site.register(JobType)
admin.site.register(Category)
admin.site.register(Applies)