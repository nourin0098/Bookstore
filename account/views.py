from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from author.models import Author
from book.models import Book

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                total_authors = Author.objects.count()
                total_books = Book.objects.count()

                context = {
                    'total_authors': total_authors,
                    'total_books': total_books,
                }
                return render(request, 'dashboard.html', context)
            else:
                messages.error(request, 'Your account is not active. Please contact the administrator.')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login') 

@login_required
def dash(request):
    return render(request, 'dashboard.html')

