from django.shortcuts import render,redirect
from .models import Student,Book,IssuedBook
from django.urls import reverse,reverse_lazy
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from datetime import date
from .forms import add_book_form,searchForm,SearchFilterField,IssueBookForm,DeleteForm
from django.contrib import messages
from django.core.paginator import Paginator
import re
# Create your views here.


def index (request):
    if (request.user.is_authenticated and not request.user.is_superuser):
        return redirect('profile')
    
    return render (request,"library/index.html")


@login_required()
def after_login (request):
    if request.user.is_superuser and request.session['user_type']=='student':
        logout(request)
        return redirect('student_login')
    elif request.user.is_superuser and request.session['user_type']=='admin':
        return redirect('add_book')# or redirect (reverse('admin:index)) 
    elif not request.user.is_superuser and request.session['user_type']=='admin':
        logout(request)
        return redirect('admin_login')
    elif not request.user.is_superuser and request.session['user_type']=='student':
        return redirect('profile')
    

@login_required()
def profile(request):
    return render(request,"library/profile.html")

@login_required
def edit_profile(request):
    passwordNotMatch=False
    form={}
    if request.method ==  "POST":
        form['username'] = request.POST['username']
        form['firstname'] = request.POST['firstname']
        form['lastname'] = request.POST['lastname']
        form['email'] = request.POST['email']
        form['mobile']=request.POST['mobile']
        form['className']=request.POST['className']
        form['roll']=request.POST['roll']
        form['branch'] = request.POST['branch']
        if (request.FILES and request.FILES['image']):
            print(request.FILES['image'])
            print(f"type: {type(request.FILES['image'])}")
            form['image']=request.FILES['image']
        try:
            user= request.user
            student=Student.objects.get(user=user)
            
            user.username=form['username']
            user.first_name=form['firstname']
            user.last_name=form['lastname']
            user.email=form['email']
            
            student.phone=form['mobile']
            student.roll_no=form['roll']
            student.classroom=form['className']
            student.branch=form['branch']
            if (request.FILES and request.FILES['image']):
                student.image=form['image']
                
            
            student.save()
            user.save()
            return redirect('profile')
        
        except IntegrityError as err:
                return render(request,"library/edit_profile.html",{"form":form,"errors":err})
        
        
        
            
    return render(request,"library/edit_profile.html")

def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('add_book') 
        else:
            return redirect(reverse('profile'))
    else:
        request.session['user_type']="admin"
        return redirect('login')

        
        

def student_login(request):
    if request.user.is_authenticated:
            if not request.user.is_superuser:
                return redirect('profile')
            else :
                return redirect ('/admin')# or redirect (reverse('admin:index)) 
    else:
        request.session['user_type']="student"
        return redirect('login')


def student_registration(request):
    if (request.user.is_authenticated and not request.user.is_superuser):
        return redirect('profile')
    passwordNotMatch=False
    form={}
    if request.method ==  "POST":
        form['username'] = request.POST['username']
        form['firstname'] = request.POST['firstname']
        form['lastname'] = request.POST['lastname']
        form['email'] = request.POST['email']
        form['mobile']=request.POST['mobile']
        form['className']=request.POST['className']
        form['roll']=request.POST['roll']
        form['branch'] = request.POST['branch']
        if (request.FILES and request.FILES['image']):
            print(request.FILES['image'])
            print(f"type: {type(request.FILES['image'])}")
            form['image']=request.FILES['image']
        
        form['password'] = request.POST['password']
        form['passwordConfirm'] = request.POST['passwordConfirm']
       
        if not(form['password']==form['passwordConfirm']):
            passwordNotMatch = True
            print("Password Mismatch")
            return render(request,"library/student_registration.html",{"passwordNotMatch":passwordNotMatch,"form":form})
        
        else:
            try:
                user= User.objects.create_user(username=form['username'],email=form['email']
                                              ,password=form['password'],first_name=form['firstname']
                                              ,last_name=form['lastname'])
                student=Student.objects.create(user=user,phone=form['mobile'],classroom=form['className'],
                                               branch=form['branch'],roll_no=form['roll'],image=form['image'])
                student.save()
                user.save()
                login(request,user)
                return redirect('profile')
            except IntegrityError as err:
                return render(request,"library/student_registration.html",{"form":form,"errors":err})
        
        
    return render(request,"library/student_registration.html",{"passwordNotMatch":passwordNotMatch,"form":form})




@login_required(login_url="/student_login")
def student_issued_books (request):
    
    student = Student.objects.get(user=request.user)
    issued_books = IssuedBook.objects.filter(student_id=student.pk)
    books_details =[]
    fees=0
    for i in issued_books:
        book= Book.objects.get(isbn=i.isbn)
        t=tuple([book.isbn,request.user.id,request.user.get_full_name,book.name,book.author,i.issued_date,i.expiry_date,0])
        spanDays = (i.expiry_date-i.issued_date).days
        print(spanDays)
        days=date.today()-i.issued_date
        
        
        d=days.days
        print("days",d)
        fees=0
        
        if(d>spanDays):
            fees=(d-spanDays)*5
            print(f'days:{d} , Difference {d-14} , Fees : {fees}')
        t=list(t)
        
        t.insert(7,fees)
        t=tuple(t)
        
        books_details.append(t)
        
    return render(request,"library/student_issued_books.html",{"books_details":books_details})




@login_required(login_url='/admin_login')
def add_book (request):
    
    form = add_book_form()
    
    if request.method=="POST":
        form=add_book_form(request.POST)
        if form.is_valid:
            book=form.save(commit=True) #it's True by default
            book.save()
            messages.add_message(request,messages.SUCCESS,f"Book {book.name} was added Succesfully!")    
            return redirect('view_books')    
        # else:
        #     errors=form.errors
        #     return render(request,'library/add_book.html')
    return render (request,"library/add_book.html",{"form":form})

def view_books(request):
    books = Book.objects.all().order_by('-name')
    
    return render(request,'library/view_books.html',{'books':books})
    

        
def view_students(request):
    
    students= Student.objects.all()
    return render(request,'library/view_students.html',{"students":students})
    pass


def issue_book(request):
    form=IssueBookForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        book=form.cleaned_data['books']
        student=form.cleaned_data['students']
        issued_date=form.cleaned_data['issued_date']
        expiry_date=form.cleaned_data['expiry_date']
        
        i=IssuedBook(student_id=student.id,isbn=book.isbn,issued_date=issued_date,expiry_date=expiry_date)
        i.save()
        messages.add_message(request,messages.SUCCESS,str(book)+"issued succesfully")
        return redirect('view_issued_books',page_num=1)
    return render(request,'library/issue_book.html',{"form":form})


def delete_issued_book(request,page_num):
    deleteForm=DeleteForm(request.POST or None)
    if request.method=="POST" and  deleteForm.is_valid():
        issued_book_id=deleteForm.cleaned_data['issued_book_id']
        if issued_book_id:
            print('Delete = ',issued_book_id)
            i=IssuedBook.objects.get(id=issued_book_id)
            i.delete()
    return redirect('view_issued_books',page_num,permanent=False)
    
    
def view_issued_books(request,page_num):
    data=[]
    form=searchForm(request.POST or None)
    # deleteForm=DeleteForm(request.POST or None)
    # if request.method=="POST" and  deleteForm.is_valid():
    #     issued_book_id=deleteForm.cleaned_data['issued_book_id']
    #     if issued_book_id:
    #         print('Delete = ',issued_book_id)
    #         i=IssuedBook.objects.get(id=issued_book_id)
    #         i.delete()
    #         return redirect('view_issued_books',page_num,permanent=False)
    issued_books = IssuedBook.objects.all()
    
    for i in issued_books:
        s=Student.objects.get(id=i.student_id)
        b=Book.objects.get(isbn=i.isbn)
        spanDays = (i.expiry_date-i.issued_date).days
        days=date.today()-i.issued_date
        d=days.days
        fees=0
        if(d>spanDays):
            fees=(d-spanDays)*5
        data.append([i,s,b,fees])
    
    if request.method=="POST" and form.is_valid():
        # I had a bug here cant use cleaned_data as I have a multiwidget field 
        #  so I used raw retrievement method 
        # search_item=form.fields['item']
        search_item=form.cleaned_data['item']#request.POST.get('searchBy_0')
        # same bug ghere
        # by=form.cleaned_data['by']
        by=form.cleaned_data['searchBy']#request.POST.get('searchBy_1')
        
        if by=='name':
            std=Student.objects.filter(user__first_name__contains=search_item)
            
            if std :
                for s in std:
                    
                    issued_books=IssuedBook.objects.filter(student_id=s.id)#id==1 just for test ,it should be studen_id=s.id
                    
                    data=[]
                    for i in issued_books:
                        s=Student.objects.get(id=i.student_id)
                        b=Book.objects.get(isbn=i.isbn)
                        
                        spanDays = (i.expiry_date-i.issued_date).days
                        days=date.today()-i.issued_date
                        d=days.days
                        fees=0
                        if(d>spanDays):
                            fees=(d-spanDays)*5
                        data.append([i,s,b,fees])
            else:
                data=[]
        elif by=='isbn':
            if len(search_item)==13:# fix a bug ,isbn is 13 , actually I just need to modefy values in the database 
                issued_books = IssuedBook.objects.filter(isbn=search_item)
                
                if issued_books:
                    data=[]
                    for i in issued_books:
                        s=Student.objects.get(id=i.student_id)
                        b=Book.objects.get(isbn=i.isbn)
                        
                        spanDays = (i.expiry_date-i.issued_date).days
                        days=date.today()-i.issued_date
                        d=days.days
                        fees=0
                        if(d>spanDays):
                            fees=(d-spanDays)*5
                        data.append([i,s,b,fees])
                else:
                    data=[]
            else:
                messages.add_message(request,messages.ERROR,'ISBN Must have 13 digits')
        elif by=='book_name':
            bks=Book.objects.filter(name__contains=search_item)
            if bks:
                for bk in bks:
                    issued_books=IssuedBook.objects.filter(isbn=bk.isbn)
                    data=[]
                    for i in issued_books:
                        s=Student.objects.get(id=i.student_id)
                        b=Book.objects.get(isbn=i.isbn)
                        
                        spanDays = (i.expiry_date-i.issued_date).days
                        days=date.today()-i.issued_date
                        d=days.days
                        fees=0
                        if(d>spanDays):
                            fees=(d-spanDays)*5
                        data.append([i,s,b,fees])
            else:
                data=[]
                        
                
        p=Paginator(data,per_page=1000)
        page=p.get_page(1)
        return render(request,'library/view_issued_books.html',{"page":page,"form":form})
                        
                    
    p=Paginator(data,per_page=4)
    page=p.get_page(page_num)
    return render(request,'library/view_issued_books.html',{"page":page,"form":form})
    
