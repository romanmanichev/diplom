from urllib.parse import urlencode
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from users.forms import LoginForm, RegisterForm
from .models import Category, Articles, ArticlesContent, get_user_model
from django.http import JsonResponse
from django.db.models import Count, Value, F
from django.core.paginator import Paginator
from social_news_site.settings import DEFAULT_USER_IMAGE


def page_not_found(request, exception):
    
    context = {
        'title': 'Страница не найдена',
        'error': 'Страница не найдена',
        'LoginForm': LoginForm(),
        'RegisterForm': RegisterForm(),
    }
    
    return render(request, 'articles/error.html', context)


def forbidden_page(request):
    
    context = {
        'title': 'Доступ запрещен',
        'error': 'У вас нет доступа к данной странице',
        'LoginForm': LoginForm(),
        'RegisterForm': RegisterForm(),
    }
    
    return render(request, 'articles/error.html', context)

class IndexView(View):
    
    def get(self, request):
        
        categories = Category.objects.all()
        
        context = {
            'title': 'Главная страница',
            'LoginForm': LoginForm(),
            'RegisterForm': RegisterForm(),
            'categories': categories,
        }   
        return render(request, 'users/index.html', context)
    
    def post(self, request):
        search = request.POST.get('search', '')
        
        if search:
           return redirect(f'{reverse('search')}?{urlencode({'search': search})}')
        else:
            return redirect('index')


class SearchView(View):
    
    def get(self, request):
        
        cat_id = request.GET.get('cat', 0)
        search = request.GET.get('search', '')
        date = request.GET.get('date', '')
        
        results = Articles.objects.all()
        
        if cat_id:
            results = Articles.objects.filter(cat_id=cat_id)
        if search:
            results = results.filter(title__contains=search)
        if date:
            if date == 'recent':
                results = results.order_by('-time_create')
            elif date == 'old':
                results = results.order_by('time_create')
        
        results = results.annotate(count=Count("articlescontent__pk")-1)
        
        paginator = Paginator(results, 10)
        page_number = request.GET.get('page', 1)
        page_object = paginator.get_page(page_number)
        
        categories = Category.objects.all()
        context = {
            'title': 'Поиск по статьям',
            
            'LoginForm': LoginForm(),
            'RegisterForm': RegisterForm(),
            
            'categories': categories,
            'results': page_object,
            'selected_cat': int(cat_id),
            'search': search,
            'selected_date': date,
            'date_of_list': {'не выбрано': '', 'Свежие': 'recent', 'Старые': 'old'},
        }
        
        return render(request, 'articles/search.html', context)
    
    
    def post(self, request):
        
        cat_id = request.POST.get('cat', 0)
        search = request.POST.get('search', '')
        date = request.POST.get('date', '')
        
        query_dict = dict()
        
        if int(cat_id) != 0:
            query_dict.update(cat=cat_id)
            
        if search != '':
            query_dict.update(search=search)
        
        if date != '':
            query_dict.update(date=date)
            
        return redirect(f'{reverse('search')}?{urlencode(query_dict)}')
            
            
class CreateView(View):
    
    def get(self, request):
        
        if not self.request.user.is_authenticated:
            return forbidden_page(request)
        
        categories = Category.objects.all()
        context = {
            'title': 'Создание темы',
            'categories': categories,
        }
        
        return render(request, 'articles/create.html', context)
    
    def post(self, request):
    
        
        cat_id = request.POST.get('category', 0)
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        code = request.POST.get('code', '')
        errors = {}
        
        if int(cat_id) == 0:
            errors['category'] = 'Не выбрана категория'
        if title == '':
            errors['title'] = 'Поле заголовок не заполнено'
        if content == '':
            errors['content'] = 'После содержание не заполнено'
        
        if errors:
            return JsonResponse(data=errors, status=401) 
        
        article = Articles.objects.create(cat_id=cat_id, title=title, author=request.user)
        ArticlesContent.objects.create(text=content, code=code, article=article, user=request.user)
        
        return JsonResponse(data={'theme': article.get_absolute_url()}, status=201)


class ThemeView(View):
    
    def get(self, request):
        
        id_theme = request.GET.get('id', 0)
        
        if int(id_theme) < 1:
            return redirect('index')
        
        article = Articles.objects.get(pk=id_theme)
        articlesContent = ArticlesContent.objects.filter(article=article)
        
        paginator = Paginator(articlesContent, 6)
        page_number = request.GET.get('page', 1)
        page_object = paginator.get_page(page_number)
        
        context = {
            'LoginForm': LoginForm(),
            'RegisterForm': RegisterForm(),
            
            'article': article,
            'articlesContent': page_object,
            'sum_of_articles': articlesContent.aggregate(count=Count("pk")),
            
            'default_photo': DEFAULT_USER_IMAGE
        }
        
        return render(request, 'articles/theme.html', context)
    
    def post(self, request):
        
        id_theme = request.GET.get('id', 0)
        
        content = request.POST.get('content', '')
        code = request.POST.get('code', '')
                
        if content == '':
            return redirect(f'{reverse('theme')}?{urlencode({'id': id_theme})}')
        
        article = Articles.objects.get(pk=id_theme)
        
        ArticlesContent.objects.create(text=content, code=code, user=request.user, article=article)
        get_user_model().objects.update(message_count=F("message_count")+1)
        
        return redirect(f'{reverse('theme')}?{urlencode({'id': id_theme})}')