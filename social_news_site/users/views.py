from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import LoginForm, RegisterForm, ProfileEditForm
from django.views.generic import UpdateView
from django.contrib.auth import get_user_model
from social_news_site.settings import DEFAULT_USER_IMAGE
from articles.models import Articles
from django.db.models import Count
from django.core.paginator import Paginator
from articles.views import forbidden_page

class LoginView(View):
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({}, status=201)
            return JsonResponse(data={'detail': 'Не верный логин или пароль'}, status=400)
        return JsonResponse(data={'detail': 'Введите логин пароль'}, status=400)


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('index')


class RegisterView(View):
    
    def post(self, request):
        form = RegisterForm(request.POST)
        print(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            return JsonResponse(data={}, status=201)
        return JsonResponse(data=form.errors, status=400)


class RegisterDoneView(View):
    
    def get(self, request):
        
        context = {
            'LoginForm': LoginForm(),
            'RegisterForm': RegisterForm(),
        }
        
        return render(request, 'users/register_done.html', context)    


class ProfileView(UpdateView):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return forbidden_page(request)
        return super(ProfileView, self).dispatch(request, *args, **kwargs)
    
    model = get_user_model()
    template_name = 'users/profile.html'
    form_class = ProfileEditForm
    extra_context = {
        'title': 'Профиль',
        'default_photo': DEFAULT_USER_IMAGE,
    }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        themes = Articles.objects.filter(author=self.request.user).annotate(count=Count("articlescontent__pk")-1)
        paginator = Paginator(themes, 4)
        page_number = self.request.GET.get('page', 1)
        themes = paginator.get_page(page_number)
        context['themes'] = themes
        return context

    
    def get_success_url(self):
        return reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return self.request.user