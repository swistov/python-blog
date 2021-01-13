from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView

from .forms import NewsForm, UserRegisterForm
from .models import News, Categories
from .utils import MyMixin


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрированы')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def login(request):
    return render(request, 'news/login.html')


def test(request):
    object = ['john', 'paul', 'george', 'ringo']
    paginator = Paginator(object, 2)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    return render(request, 'news/test.html', {'page_obj': page_obj})


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
