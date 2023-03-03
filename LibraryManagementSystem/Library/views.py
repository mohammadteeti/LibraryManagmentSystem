from django.shortcuts import render,redirect
from .models import Student,Book,IssuedBook
from django.urls import reverse,reverse_lazy
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from datetime import date
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
        return redirect('/admin')# or redirect (reverse('admin:index)) 
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
            user= User.objects.get(username=request.user.username)
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
            return redirect('/admin') # or redirect (reverse('admin:index)) 
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



