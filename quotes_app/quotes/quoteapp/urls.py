from django.urls import path
from . import views

app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('add_tag/', views.add_tag, name='add_tag'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('author/<str:author_fullname>', views.author, name='author'),
    path('tag/<str:tag_name>/', views.quotes_by_tag, name='quotes_by_tag'),
    path('my_quotes/', views.my_quotes, name='my_quotes'),
    path('authors/', views.authors, name='authors'),
    path('delete_author/<str:author_fullname>', views.delete_author, name='delete_author'),
    path('delete_quote/<int:quote_id>', views.delete_quote, name='delete_quote'),
    # path('authors/delete_duplicate', views.delete_duplicate, name='delete_duplicate'),
]
