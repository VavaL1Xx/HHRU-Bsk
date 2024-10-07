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
        'creation',
    ]

    def creation(self, obj):
        if isinstance(obj.date_of_creation, str):
            return obj.date_of_creation
        elif obj.date_of_creation:
            return obj.date_of_creation.strftime('%Y-%m-%d %H:%M')
        return 'Не указана'
    creation.short_description = 'Дата создания'

admin.site.register(Job, JobAdmin)
