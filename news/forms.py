from django import forms

from .models import Categories


class NewsForm(forms.Form):
    title = forms.CharField(max_length=150, label='Название', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(required=False, label='Текст',
                              widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    is_published = forms.BooleanField(required=False, initial=True, label='Опубликовать?')
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), label='Категория',
                                      empty_label='Выберите категорию',
                                      widget=forms.Select(attrs={'class': 'form-control'}))
