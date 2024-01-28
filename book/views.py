from django.shortcuts import render,redirect
from .models import Book,Author
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import BookSerializer
from rest_framework import generics
from rest_framework.filters import SearchFilter
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def book_list(request):
    book = Book.objects.all() 
    #searching
    keyword = request.GET.get('q','')
    if keyword:
        book = book.filter(
            Q(bookid__icontains=keyword) | 
            Q(bookname__icontains=keyword) | 
            Q(created_date__icontains=keyword)  |
            Q(author__authorname__icontains=keyword)        
        )

        # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(book, 10) 
    try:
        book = paginator.page(page)
    except PageNotAnInteger:
        book = paginator.page(1)
    except EmptyPage:
        book = paginator.page(paginator.num_pages)
    total_authors = Author.objects.count()
    total_books = Book.objects.count()
    context = {
                'books': book,
                'search_query': keyword,
                'total_authors': total_authors,
                'total_books': total_books,
            }
    return render(request,'books.html',context)

@login_required
def add_book(request):
    authors = Author.objects.all()
    if request.method == 'POST':
        bookid = request.POST.get('bookid')
        bookname = request.POST.get('bookname')
        author = request.POST.get('author')
        existing_book = Book.objects.filter(
            bookid=bookid,
            bookname=bookname,
            author_id=author
        )

        if existing_book.exists():
            messages.error(request, 'A book with the same details already exists!')
        else:
            author = get_object_or_404(Author, id=author)
            Book.objects.create(bookid=bookid, bookname=bookname, author=author)
            messages.success(request, 'Book created successfully!')
            return redirect('books')
    total_authors = Author.objects.count()
    total_books = Book.objects.count()
    context = {
                'authors': authors,
                'total_authors': total_authors,
                'total_books': total_books,
            }
    return render(request, 'book_add.html',context)

@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    authors = Author.objects.all()

    if request.method == 'POST':
        new_bookid = request.POST.get('bookid')
        new_bookname = request.POST.get('bookname')
        author_id = request.POST.get('author')
        existing_book = Book.objects.filter(
            bookid=new_bookid,
            bookname=new_bookname,
            author=author_id
        ).exclude(pk=pk)

        if existing_book.exists():
            messages.error(request, 'A book with the edited details already exists!')
        else:
            author = get_object_or_404(Author, id=author_id)
            book.bookid = new_bookid
            book.bookname = new_bookname
            book.author = author
            book.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('books')
    total_authors = Author.objects.count()
    total_books = Book.objects.count()
    context = {
                'book': book, 
                'authors': authors,
                'total_authors': total_authors,
                'total_books': total_books,
            }
    return render(request, 'book_edit.html', context)

@login_required
def remove_book(request, pk):
    book = Book.objects.get(pk=pk)
    if book:
        book.delete()
    return redirect('books') 


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ['bookid', 'bookname', 'author__authorname']