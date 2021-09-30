from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from authapp.forms import XabrUserLoginForm
from django.contrib import auth
from django.urls import reverse
from authapp.forms import XabrUserRegisterForm, XabrUserEditForm
from authapp.models import XabrUser
from mainapp.models import Category, Post


def login(request):
    """контроллер для выводв страницы авторизации/регистрации пользователя"""

    title = 'вход'
    next = request.GET['next'] if 'next' in request.GET.keys() else ''
    login_form = XabrUserLoginForm(data=request.POST)

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main:index'))

    content = {'title': title, 'login_form': login_form, 'next': next, }
    return render(request, 'authapp/login.html', content)


def logout(request):
    """контроллер выхода пользователя из личного кабинета"""

    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def register(request):
    """контроллер для вывода формы регистрации (ввода данных) пользователя"""

    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST':
        register_form = XabrUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if user.send_verify_mail():
                print('сообщение подтверждения отправлено')
                return HttpResponseRedirect(reverse('auth:send_confirm'))
            else:
                print('ошибка отправки сообщения')
            return HttpResponseRedirect(reverse('mainapp:index'))
    else:
        register_form = XabrUserRegisterForm()
    content = {
        'title': 'регистрация пользователя',
        'register_form': register_form,
        'next': next,
    }
    return render(request, 'authapp/register.html', content)


@login_required
def read_profile(request):
    """контроллер для вывода профиля пользователя"""

    categories = Category.objects.all()
    posts = Post.objects.filter(user=request.user).order_by('-create_datetime')
    user = request.user

    content = {
        'title': 'Профиль пользователя',
        'user': user,
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'authapp/read_profile.html', content)


@login_required
def edit(request):
    """функция для редактирования профиля пользователя"""

    title = 'редактирование'

    if request.method == 'POST':
        edit_form = XabrUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:read_profile'))
    else:
        edit_form = XabrUserEditForm(instance=request.user)

    content = {
        'title': title,
        'edit_form': edit_form,
    }

    return render(request, 'authapp/edit.html', content)


def verify(request, email, activation_key):
    """контроллер для вывода подтверждения/не подтверждения регистрации"""

    try:
        user = XabrUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user,
                       backend='django.contrib.auth.backends.ModelBackend')
        else:
            print(f'error activation user: {user}')
        return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('mainapp:index'))
