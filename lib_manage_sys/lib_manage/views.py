from pyexpat.errors import messages
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NewUserRegForm,addBookForm,userRegForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Book, UserGetBooks, UserReg
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.signals import user_logged_in
from datetime import datetime, timedelta




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

def addBookView(request,id=0):
    if request.method == 'POST':
        if id==0:
            form = addBookForm(request.POST)
        else:
            book = get_object_or_404(Book, id=request.POST.get('book_id'))
            form = addBookForm(request.POST,instance=book)
        if form.is_valid():
            form.save()
        return redirect('home') 
    else:
        if id==0:
            form = addBookForm()
            return render(request,'lib_manage/Add_Book.html',{'form':form})
        else:
            book = get_object_or_404(Book, id=id)
            form = addBookForm(instance=book)
            return render(request, 'lib_manage/update_book.html', {'form': form, 'book_id': book.id})



def searchBook(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        searched_books = Book.objects.filter(name__icontains=name)
        context = {'searched_books': searched_books}
        return render(request, 'lib_manage/search.html', context)


def deleteBook(request,id):
    if  request.method == 'POST':
        Book.objects.filter(id=id).delete()
        return JsonResponse({'message': 'Item deleted successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

        
def user_reg(request):
    if request.method == 'POST':
        form = userRegForm(request.POST)
        if form.is_valid():
            id_num = form.cleaned_data['id_num']
            try:
                user = UserReg.objects.get(id_num=id_num)
                html_content = '''
                <html>
                <body>
                    <p style="font-size: 30px;">User is already registered.Try Another</p>
                    <br>
                    <a href="" class="btn btn-primary">Go to Home</a>
                </body>
                </html>
                '''
                return HttpResponse(html_content)   
            except:
                form.save()
                user = UserReg.objects.get(id_num=id_num)
                return render(request,'lib_manage/user_Id.html',{'user_id':user.reg_num})      
    else:
        form = userRegForm()

    return render(request,'lib_manage/user_Reg.html',{'form':form})


def getBook(request):
    if request.method == 'POST':
        user_reg_num  = request.POST.get('user_Id')
        book_id = request.POST.get('book_Id')
        print(book_id)
        
        try:
            user = UserReg.objects.get(reg_num=user_reg_num)
            print(UserGetBooks.objects.filter(user=user).count())
            print(UserGetBooks.objects.filter(user=user).count())
            print(UserGetBooks.objects.filter(user=user).count())
            if UserGetBooks.objects.filter(user=user).count()>1:
                context = {
                    'error_message': "He already has got 2 books",
                    'searched_books': Book.objects.all(),  # You may want to adjust this based on your actual use case
                    'book_id':book_id
                }
                return render(request, 'lib_manage/search.html', context)
        except UserReg.DoesNotExist:
            context = {
                'error_message': "User not found. Please check the registration number.",
                'searched_books': Book.objects.all(),  # You may want to adjust this based on your actual use case
                'book_id':book_id
            }
            return render(request, 'lib_manage/search.html', context)
       
        book = get_object_or_404(Book, id=book_id)
        UserGetBooks.objects.create(book=book, user=user)

        book = Book.objects.get(id=book_id)
        book.qty = book.qty-1
        book.save()

        return redirect('home')
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def handover(request):
    user_ID = request.POST.get('user_id')
    if not user_ID:
        print("No user ID provided.")
        return render(request, 'lib_manage/hand_over.html')

    try:
        user = UserReg.objects.get(reg_num=user_ID)
        userGetBooks = UserGetBooks.objects.filter(user=user)
        print(f"Found {userGetBooks.count()} books for user {user.name}.")
    except UserReg.DoesNotExist:
        print("User not found.")
        userGetBooks = []  # Empty list if user not found

    context = {
        'userGetBooks': userGetBooks
    }
    return render(request, 'lib_manage/hand_over.html', context)


def handoverDelete(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_Id')
        user_id = request.POST.get('user_Id')
        print(book_id)
        print(user_id)

        if book_id and user_id:
            try:
                user_get_book = UserGetBooks.objects.filter(book_id=book_id, user_id=user_id)
                user_get_book.delete()
                book = Book.objects.get(id=book_id)
                book.qty = book.qty+1
                book.save()
                return redirect('handover')
            except UserGetBooks.DoesNotExist:
                return HttpResponseBadRequest("The record does not exist.")
        else:
            return HttpResponseBadRequest("Invalid data.")
    else:
        return HttpResponseBadRequest("Invalid request method.")
    

def logout(request):
    return render(request, 'lib_manage/login.html')

@receiver(user_logged_in)
def send_email(sender, request, user, **kwargs):
    try:
        handOverDate = (datetime.now() + timedelta(days=2)).date()
        usergetbooks = UserGetBooks.objects.all()
        for i in usergetbooks:
            if handOverDate == i.dueDate:
                user1 = UserGetBooks.objects.filter(user=i.user)
                for userTemp in user1:
                    if not (i.emailStatus):
                        toEmail = UserReg.objects.get(reg_num=i.user.reg_num).email
                        send_mail("This is Subject", "This is message", "imeshisuranga00@gmail.com", [toEmail],fail_silently=False,)
                        i.emailStatus = True
                        i.save()
    except BadHeaderError:
        return HttpResponse("Invalid header found.")
    return HttpResponseRedirect("/contact/thanks/")


def filter(request,category):
    print(category)
    searched_books = Book.objects.filter(category=category)
    context = {'searched_books': searched_books}
    return render(request, 'lib_manage/search.html', context)

    
    


