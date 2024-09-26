from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .forms import TagForm, AuthorForm, QuoteForm
from .models import Tag, Author, Quote
from django.db.models import Count
from django.db import models


# Create your views here.
def main(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 10)  # Разбиваем на страницы по 10 цитат

    page_number = request.GET.get('page')  # Получаем текущий номер страницы из запроса
    page_obj = paginator.get_page(page_number)  # Получаем объекты для текущей страницы

    top_tags = Tag.objects.annotate(num_quotes=Count('quotes')).order_by('-num_quotes')[:10]

    context = {
        'page_obj': page_obj,
        'top_tags': top_tags
    }
    return render(request, 'quoteapp/index.html', context)


    # Пагинация: отображаем 10 цитат на странице



@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/add_tag.html', {'form': form})

    return render(request, 'quoteapp/add_tag.html', {'form': TagForm()})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save(commit=False)
            new_author.user = request.user
            new_author.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/add_author.html', {'form': form})

    return render(request, 'quoteapp/add_author.html', {'form': AuthorForm()})

@login_required
def add_quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            author_id = request.POST.get('author')
            new_quote.author = Author.objects.get(id=author_id)
            new_quote.user = request.user
            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/add_quote.html', {'tags': tags, 'authors': authors, 'form': form})

    return render(request, 'quoteapp/add_quote.html', {"tags": tags, 'authors': authors, 'form': QuoteForm()})


def author(request, author_fullname):
    author = get_object_or_404(Author, fullname=author_fullname)
    return render(request, 'quoteapp/author.html', {"author": author})


# def quotes_by_tag(request, tag_name):
#     tag = get_object_or_404(Tag, name=tag_name)
#     quotes = Quote.objects.filter(tags=tag)
#     return render(request, 'quoteapp/index.html', {'quotes': quotes, 'tag': tag})


def quotes_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    quotes = Quote.objects.filter(tags=tag) 

    paginator = Paginator(quotes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    top_tags = Tag.objects.annotate(num_quotes=Count('quotes')).order_by('-num_quotes')[:10]


    context = {
        'tag': tag,
        'page_obj': page_obj,
        'top_tags': top_tags
    }

    return render(request, 'quoteapp/index.html', context)


@login_required
def my_quotes(request):
    quotes = Quote.objects.filter(user=request.user)
    return render(request, 'quoteapp/index.html', {'quotes': quotes})



def authors(request):
    authors = Author.objects.filter(user=request.user)
    return render(request, 'quoteapp/authors.html', {'authors': authors})


@login_required
def delete_author(request, author_fullname):
    Author.objects.get(fullname=author_fullname, user=request.user).delete()
    authors(request)
    return redirect(to='quoteapp:main')

@login_required
def delete_quote(request, quote_id):
    Quote.objects.get(pk=quote_id, user=request.user).delete()
    return redirect(to='quoteapp:main')


# def delete_duplicate(request):
#     duplicate_authors = Author.objects.values('fullname').annotate(name_count=models.Count('fullname')).filter(name_count__gt=1)
#     for author in duplicate_authors:
#         Author.objects.filter(fullname=author['fullname']).exclude(pk=Author.objects.filter(fullname=author['fullname']).first().pk).delete()
#     return redirect(to='quoteapp/authors.html')