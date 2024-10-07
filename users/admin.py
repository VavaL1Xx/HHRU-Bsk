from django.contrib import admin

# Register your models here.

from users.models import Employer, JobSeeker

class EmployerAdmin(admin.ModelAdmin):
    list_display = [
        'company_name',
        'user_username',
        'user_email',
        'date',
    ]
    
    def date(self, obj):
        if isinstance(obj.user.date_of_registration, str):
            return obj.user.date_of_registration
        elif obj.user.date_of_registration:
            return obj.user.date_of_registration.strftime('%Y-%m-%d %H:%M')
        return 'Не указана'
    date.short_description = 'Дата регистрации'

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Логин'

    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Электронная почта'


class JobSeekerAdmin(admin.ModelAdmin):
    list_display = [
        'user_username',
        'user_email',
        'resume',
        'date',
    ]

    def date(self, obj):
        if isinstance(obj.user.date_of_registration, str):
            return obj.user.date_of_registration
        elif obj.user.date_of_registration:
            return obj.user.date_of_registration.strftime('%Y-%m-%d %H:%M')
        return 'Не указана'
    date.short_description = 'Дата регистрации'

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Логин'

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Электронная почта'


admin.site.register(JobSeeker, JobSeekerAdmin)
admin.site.register(Employer, EmployerAdmin)
