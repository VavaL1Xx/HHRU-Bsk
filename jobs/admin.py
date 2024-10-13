from django.contrib import admin

# Register your models here.

from jobs.models import Job, Response


class JobAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'employer',
        'industry',
        'resps',
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


class ResponseAdmin(admin.ModelAdmin):
    list_display =[
        'status',
        'job',
        'job_seeker',
        'creation',
    ]

    def creation(self, obj):
        if isinstance(obj.date_of_response, str):
            return obj.date_of_response
        elif obj.date_of_response:
            return obj.date_of_response.strftime('%Y-%m-%d %H:%M')
        return 'Не указана'
    creation.short_description = 'Дата создания'


admin.site.register(Job, JobAdmin)
admin.site.register(Response, ResponseAdmin)
