from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NewsForm
from .models import News, Categories
from .utils import MyMixin


class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    # extra_context = {'title': 'Главная'}
    queryset = News.objects.select_related('category')
    mixin_prop = 'hello world'

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


# def index(request):
#     news = News.objects.all()
#     context = {
#         "news": news,
#         "title": "Список новостей",
#     }
#     return render(request=request, template_name="news/index.html", context=context)


# def get_category(request, category_id: int):
#     news = News.objects.filter(category_id=category_id)
#     categories = Categories.objects.all()
#     category = Categories.objects.get(pk=category_id)
#     context = {
#         "news": news,
#         'categories': categories,
#         'category': category,
#     }
#     return render(request, "news/category.html", context)


# def view_news(request, news_id: int):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})
