from .models import Job
from django import forms


# ---------------------------
# Форма для создания вакансии
# ---------------------------


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title',
            'industry',
            'skills',
            'salary',
            'contact_email',
            'location',
            'description',
            'employment_type',
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок вакансии'}),
            'industry': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Выберите отрасль'}),
            'skills': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Выберите навыки'}),
            'salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заработная плата'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Контактный адрес почты'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Место поиска'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Описание для вакансии'}),
            'employment_type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Тип занятости'}),
        }

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['industry'].empty_label = "Выберите категорию"
        self.fields['industry'].widget.attrs['class'] += ' select-placeholder'
        
        self.fields['employment_type'].empty_label = "Выберите тип занятости"
        self.fields['employment_type'].widget.attrs['class'] += ' select-placeholder'