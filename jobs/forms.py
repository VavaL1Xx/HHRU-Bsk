from .models import Job
from django import forms


# ---------------------------
# Форма для создания вакансии
# ---------------------------


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('title', 'description', 'location', 'salary')