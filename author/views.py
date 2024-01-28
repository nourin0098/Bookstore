from django.shortcuts import render,redirect, get_object_or_404

from book.models import Book
from .models import Author
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import AuthorSerializer
from rest_framework import generics
from rest_framework.filters import SearchFilter
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def author_list(request):
    authors = Author.objects.all() 

    #searching
    keyword = request.GET.get('q','')
    if keyword:
        authors = authors.filter(
            Q(authorname__icontains=keyword) | 
            Q(username__icontains=keyword) | 
            Q(email__icontains=keyword)         
        )
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(authors, 10)
    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        authors = paginator.page(1)
    except EmptyPage:
        authors = paginator.page(paginator.num_pages)

    total_authors = Author.objects.count()
    total_books = Book.objects.count()

    context = {
        'authors': authors,
        'search_query': keyword,
        'total_authors': total_authors,
        'total_books': total_books,
    }
    return render(request, 'author.html', context)

@login_required
def author_details(request,pk):
    author = get_object_or_404(Author, pk=pk)
    books = Book.objects.filter(author=author)
    #searching
    keyword = request.GET.get('q','')
    if keyword:
        books = books.filter(
            Q(bookid__icontains=keyword) | 
            Q(bookname__icontains=keyword)  
        )
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(books, 10) 
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    context = {'author': author,}
    

    context = {
        'search_query':keyword,
        'author': author,
        'books': books,
    }
    return render(request, 'auth_details.html',context)
    
@login_required
def add_author(request):
    if request.method == 'POST':
        authorname = request.POST.get('authorname')
        username = request.POST.get('username')
        email = request.POST.get('email')

        existing_author = Author.objects.filter(
            authorname__iexact=authorname,
            username__iexact=username,
            email__iexact=email
        ).first()

        if existing_author:
            messages.error(request, 'Author with the same details already exists!')
        else:
            Author.objects.create(authorname=authorname, username=username, email=email)
            messages.success(request, 'Author created successfully!')
            return redirect('author')

    total_authors = Author.objects.count()
    total_books = Book.objects.count()
    context = {
        'total_authors': total_authors,
        'total_books': total_books,
    }

    return render(request, 'auth_add.html', context)


@login_required
def edit_author(request, pk):
    author = get_object_or_404(Author, pk=pk)

    if request.method == 'POST':
        new_authorname = request.POST.get('authorname')
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        existing_author = Author.objects.filter(
            authorname__iexact=new_authorname,
            username__iexact=new_username,
            email__iexact=new_email
        ).exclude(pk=pk)

        if existing_author.exists():
            messages.error(request, 'Author with the same details already exists!')
        else:
            author.authorname = new_authorname
            author.username = new_username
            author.email = new_email
            author.save()
            messages.success(request, 'Author updated successfully!')
            return redirect('author') 
    total_authors = Author.objects.count()
    total_books = Book.objects.count()
    context = {
                'author': author,
                'total_authors': total_authors,
                'total_books': total_books,
                }
    return render(request, 'auth_edit.html', context)

@login_required
def remove_author(request, pk):
    author = Author.objects.get(pk=pk)
    if author:
        author.delete()
    return redirect('author') 

class AuthorListAPIView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [SearchFilter]
    search_fields = ['authorname', 'email']



