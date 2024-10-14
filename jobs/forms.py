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
            'requirements',
            'salary',
            'contact_email',
            'location',
            'description',
            'employment_type',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок вакансии'}),
            'industry': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Выберите отрасль'}),
            'requirements': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Ваши требования'}),
            'salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заработная плата'}),
            'contact_email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Контактный адрес почты'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Место поиска'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Описание для вакансии'}),
            'employerment_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тип занятости'}),
        }

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
         # Добавляем пустую опцию для поля industry
        self.fields['industry'].empty_label = "Выберите категорию"
        self.fields['industry'].widget.attrs['class'] += ' select-placeholder'
        
        self.fields['employment_type'].empty_label = "Выберите тип занятости"
        self.fields['employment_type'].widget.attrs['class'] += ' select-placeholder'