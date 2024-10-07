from django.contrib import admin

# Register your models here.

from jobs.models import Job

class JobAdmin(admin.ModelAdmin):
    list_display = [
        'employer',
        'title',
        'description',
        'location',
        'salary',
    ]

admin.site.register(Job, JobAdmin)
