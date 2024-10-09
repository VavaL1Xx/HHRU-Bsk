from django.contrib import admin
from django.utils.safestring import mark_safe
# Register your models here.

from users.models import Employer, JobSeeker

class EmployerAdmin(admin.ModelAdmin):
    list_display = [
        'prof_image',
        'company_name',
        'inn',
        'user_username',
        'website',
        'date',
        'lst_log',
    ]
    
    def prof_image(self, obj):
        if obj.user.profile_picture:
            return mark_safe(f'<img src="{obj.user.profile_picture.url}" width="128"/>')
        return 'отсутствует'
    prof_image.short_description = "Фотография"

    def date(self, obj):
        if isinstance(obj.user.date_of_registration, str):
            return obj.user.date_of_registration
        elif obj.user.date_of_registration:
            return obj.user.date_of_registration.strftime('%Y-%m-%d %H:%M')
        return 'Не указана'
    date.short_description = 'Дата регистрации'

    def lst_log(self, obj):
        return obj.user.last_login
    lst_log.short_description = 'Последний вход'

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Логин'
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Электронная почта'


class JobSeekerAdmin(admin.ModelAdmin):
    list_display = [
        'prof_image',
        'user_username',
        'phone',
        'user_email',
        'portfolio_link',
        'date',
        'lst_log',
    ]

    def prof_image(self, obj):
        if obj.user.profile_picture:
            return mark_safe(f'<img src="{obj.user.profile_picture.url}" width="128"/>')
        return 'отсутствует'
    prof_image.short_description = "Фотография"

    def date(self, obj):
        if isinstance(obj.user.date_of_registration, str):
            return obj.user.date_of_registration
        elif obj.user.date_of_registration:
            return obj.user.date_of_registration.strftime('%Y-%m-%d %H:%M')
        return 'Не указана'
    date.short_description = 'Дата регистрации'

    def phone(self, obj):
        return obj.user.phone_number if not None else ""
    phone.short_description = 'Телефон'

    def lst_log(self, obj):
        return obj.user.last_login
    lst_log.short_description = 'Последний вход'

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Логин'

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Электронная почта'


admin.site.register(JobSeeker, JobSeekerAdmin)
admin.site.register(Employer, EmployerAdmin)
