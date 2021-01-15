from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView

from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from .models import News, Categories
from .utils import MyMixin


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрированы')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'blog@green-call.ru',
                             ['swip88@bk.ru'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка при отправке')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = ContactForm()
    return render(request, 'news/test.html', {'form': form})


class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    # extra_context = {'title': 'Главная'}
    queryset = News.objects.select_related('category').filter(is_published=True)
    mixin_prop = 'hello world'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавление кастомных полей"""
        context = super(HomeNews, self).get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    # def get_queryset(self):
    #     """Выводить только опубликованные новости"""
    #     return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    """Запрет на показ пустых списков"""
    allow_empty = False
    paginate_by = 5

    def get_queryset(self):
        """Выводить новости категории"""
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsByCategory, self).get_context_data(**kwargs)
        context['title'] = self.get_upper(Categories.objects.get(pk=self.kwargs['category_id']))
        return context


class ViewNews(DetailView):
    model = News
    """Если в url используется название отличное от pk"""
    # pk_url_kwarg = 'news_id'
    # template_name = 'news/news_detail.html'
    """В стандарте используется наименование object"""
    context_object_name = 'news_item'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    """Адрес для пересылки, если не используется get_absolute_url"""
    login_url = '/admin/'
    """Вместо перенаправления возвращает 403"""
    # raise_exception = True
    # success_url = reverse_lazy('home')
