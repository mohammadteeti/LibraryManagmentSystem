

from django.urls import path,include
from Library import views
import django.contrib.auth.views as auth_views

urlpatterns = [
    
    
    path ("",views.index,name="index"),
    # path ("add_book/",views.add_book,name="add_book"),
    # path ("view_books/",views.view_books,name="view_books"),
    # path ("view_students/",views.view_students,name="view_students"),
    # path ("issue_book/",views.issue_book,name="issue_book"),
    # path("view_issued_book/",views.view_issued_book,name="view_issued_book"),
    # path ("student_issued_books/",views.student_issued_books,name="student_issued_books"),
      path("profile/",views.profile,name="profile"),
      path("student_issued_books/",views.student_issued_books,name="student_issued_books"),
      path("edit_profile/",views.edit_profile,name="edit_profile"),
      path("after_login/",views.after_login,name="after_login"),
    # path ("edit_profile/",views.edit_profile,name="edit_profile"),
    path ("student_registration/",views.student_registration,name="student_registration"),
    # path("change_password/",views.change_password,name="change_password"),
    path ("student_login/",views.student_login,name="student_login"),
    path ("admin_login/",views.admin_login,name="admin_login"),
    
    path ("add_book/",views.add_book,name="add_book"),
    path ('view_books/',views.view_books,name='view_books'),
    path ('view_student/',views.view_students,name='view_students'),
    path ('issue_book/',views.issue_book,name='issue_book'),
    path ('view_issued_books/<int:page_num>',views.view_issued_books,name='view_issued_books'),
    path('issue_book/',views.issue_book,name='issue_book'),
    path('delete_issued_book/<int:page_num>',views.delete_issued_book,name='delete_issued_book'),
    # path ("logout",views.logout,name="logout"),
    # path ("delete_book/<int:book_id>/",views.delete_book,name="delete_book"),
    # path ("delete_student/<int:student_id",views.delete_student,name="delete_student"),
   
   
    #very very very Important Note :
    #to override password reset and change user registration in general 
    #1. Add templates dirctory to the 'DIRS' dict in Settings (aadd full path using BASE_DIR)   
    #2. for password change add two templates (password_change_form) and (password_change_done)
    
    #3. for Password reset we have to do the follwing :
    # A)add 5 Templates 
          #password_reset_form.html -> to enter email
          #password_reset_done.html -> to prompt email sent 
          #password_reset_email.html -> email templates : must contain {{protocole}}://{{domain}}{%url 'password_reset_confirm'  uidb64=uid token=token%}
          
          #uidb64 : arguments generated by django to authenticate the request when user clicks the link in the email 
          #this argument is sent with the link to the user email with the token 
          
          #token is a randomly generated string by django also to confirm user request from email 
          #token is sent with the link on email
          
          
          #password_reset_confirm.html -> form to enter new password after coming from email link
          #password_reset_complete.html ->prompt reset successfull 
          
    #B) we must  add the following to urls.py if we want to overrid the built in functionality 
        #note the uidb64 and token in the url is a must (they are filled by django)
          
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
  #c) we can override the PasswordResetConfirm view  by creating a class based view in views.py and 
      #pass the email template that we want 
       

    
    
    
]
