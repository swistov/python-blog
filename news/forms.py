import re

from django import forms
from django.core.exceptions import ValidationError

from .models import News


class NewsForm(forms.ModelForm):
    """
    :param fields - поля для отображения
    :param widgets - дополнительные параметры
    """
    class Meta:
        model = News
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        """
        Дополнительная проверка
        Проверяем что-бы title не начинался с цифры
        :return: title или ошибку
        """
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title
