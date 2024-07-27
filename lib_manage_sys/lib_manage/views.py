from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NewUserRegForm,addBookForm,userRegForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Book


# Create your views here.



def loginView(request):
    books = Book.objects.all
    context = {'books':books}
    if request.user.is_authenticated:
        return render(request,'lib_manage/index.html',context)
    else:
        return redirect('login')

def registerView(request):
    form = NewUserRegForm()
    if request.method == "POST":
        form = NewUserRegForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    context={'form':form}
    return render(request, 'registration/register.html', context)

def addBookView(request):
    if request.method == 'POST':
        form = addBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = addBookForm()

    return render(request,'lib_manage/Add_Book.html',{'form':form})

def searchBook(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        searched_books = Book.objects.filter(name__icontains=name)
        context = {'searched_books': searched_books, 'name': name}
        return render(request, 'lib_manage/search.html', context)


def deleteBook(request,id):
    if  request.method == 'POST':
        Book.objects.filter(id=id).delete()
        return JsonResponse({'message': 'Item deleted successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def updateBook(request, id):
    book = get_object_or_404(Book, id=id)
    form = addBookForm(instance=book)
    return render(request, 'lib_manage/update_book.html', {'form': form, 'book_id': book.id})

    
        
def updateBookConfirm(request):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=request.POST.get('book_id'))
        form = addBookForm(request.POST,instance=book)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        return redirect('home')
        
def user_reg(request):
    if request.method == 'POST':
        form = userRegForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = userRegForm()

    return render(request,'lib_manage/user_Reg.html',{'form':form})

