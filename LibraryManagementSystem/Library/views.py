from django.shortcuts import render,redirect
from django.urls import reverse,reverse_lazy
from django.contrib.auth import login,logout


from django.contrib.auth.decorators import login_required

# Create your views here.


def index (request):
    
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
    pass


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
    pass
