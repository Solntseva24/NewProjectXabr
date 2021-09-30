import mainapp.views as mainapp
from django.urls import path

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('post/<slug:slug>/', mainapp.post, name='post'),
    path('help/', mainapp.help, name='help'),
    path('category/<slug:slug>/', mainapp.category_page, name='category_page'),
    path('changelike/<slug:slug>/', mainapp.change_like, name='change_like'),
    path('search/', mainapp.SearchResultsView.as_view(), name='search_results'),
    path('delete/comment/', mainapp.delete_comment, name='delete_comment'),
    path('to/banish/', mainapp.to_banish, name='to_banish'),
]
