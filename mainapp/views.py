from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from authapp.models import XabrUser
from .forms import CommentForm
from .models import Category, Post, Comments, Like


class SearchResultsView(ListView):
    """контроллер, возврящающий страницу с результатами поиска"""

    model = Post
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        object_list = Post.objects.filter(
            Q(
                is_active__icontains=True) & Q(
                name__icontains=query) | Q(
                is_active__icontains=True) & Q(
                posts_text__icontains=query)).order_by(
            '-like_quantity',
            '-create_datetime')
        return object_list



def index(request):
    """контроллер, возврящающий главную страницу со списком всех статей сайта"""

    posts = Post.objects.filter(is_active=True).order_by('-create_datetime')
    categories = Category.objects.filter(is_active=True)

    context = {
        'page_title': 'главная',
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'mainapp/index.html', context)


def post(request, slug):
    """контроллер вывода полной статьи"""

    post = Post.objects.filter(slug=slug, is_active=True)
    categories = Category.objects.all()
    comment = Comments.objects.filter(post=post.first())

    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.post = post.first()
            form.save()

    else:
        form = CommentForm()

    context = {
        'page_title': 'хабр',
        'posts': post,
        'categories': categories,
        'comments': comment,
        'form': form,
    }
    return render(request, 'mainapp/post.html', context)


def help(request):
    """контроллер вывода страницы "Помощь" """

    categories = Category.objects.filter(is_active=True)

    context = {
        'page_title': 'помощь',
        'categories': categories
    }
    return render(request, 'mainapp/help.html', context)


def category_page(request, slug):
    """контроллер вывода страниц статей, относящихся к конкретной категории """

    categories = Category.objects.filter(is_active=True)

    if request.user.is_authenticated:
        new_like, created = Like.objects.get_or_create(
            user=request.user, slug=slug)
    else:
        new_like = Like.objects.all()
    if slug == '':
        category = {'slug': '', 'name': 'все'}
        posts = Post.objects.filter(
            is_active=True).order_by('-create_datetime')
    else:
        category = get_object_or_404(Category, slug=slug)
        posts = category.post_set.filter(
            is_active=True).order_by('-create_datetime')

    context = {
        'page_title': 'главная',
        'categories': categories,
        'category': category,
        'posts': posts,
        'new_like': new_like,
    }
    return render(request, 'mainapp/category_page.html', context)


def change_like(request, slug):
    """функция проставления лайка/дизлайка"""

    post = get_object_or_404(Post, slug=slug)
    new_like, created = Like.objects.get_or_create(
        user=request.user, slug=slug)

    if request.method == 'POST':
        new_like.is_active = not new_like.is_active
        if not new_like.is_active:
            post.like_quantity += 1
            post.save()
            new_like.save()
        else:
            post.like_quantity -= 1
            post.save()
            new_like.save()
        context = {
            'new_like': new_like,
        }

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'), context)


def delete_comment(request):
    """функция удаления комментария к статье"""

    id = request.POST['comment_id']
    if request.method == 'POST':
        comment = get_object_or_404(Comments, id=id)
        comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def to_banish(request):
    """функция, позволяющая забанить пользователя администратору/модератору"""

    user_com = request.POST['user_id']
    if request.method == 'POST':
        block_user = XabrUser.objects.get(username=user_com)
        block_user.is_active = False
        block_user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def doc(request):
    """контроллер вывода страницы "Документация" """

    return render(request, 'doc/index.html')
