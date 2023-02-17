from django.db import models
from datetime import datetime ,timedelta
# Create your models here.

class Book (models.Model):
    name = models.CharField(("Name"), max_length=50)
    author=models.CharField(("Author"), max_length=50)
    isbn = models.PositiveIntegerField("ISBN")
    category =models.CharField(("Category"), max_length=50)
    
    def __str__(self) -> str:
        return f"{self.name} by {self.author}:[{self.isbn}] "
    

class Student (models.Model):
   user = models.OneToOneField("User", verbose_name=("Student"), on_delete=models.CASCADE)
   classroom =models.CharField(("Class Room"), max_length=50)
   branch=models.CharField(("Branch"), max_length=10)
   roll_no=models.CharField(("Roll No."),blank=True)
   phone = models.CharField(("Phone No."), max_length=50,blank=True)
   image=models.ImageField(("Image"), upload_to="", blank=True)
   
   def __str__(self) -> str:
       return f"{self.user} [{self.classroom}] [{self.branch}] [{self.roll_no}]"

def expiry():
    
    return datetime.today()- timedelta(days=14)

class IssuedBook(models.Model):
    student_id = models.CharField(("Student ID"), max_length=100)
    isbn =models.CharField(("ISBN"), max_length=13)
    issued_date = models.DateField(("Issued On"), auto_now=False)
    expiry_date=models.DateField(("Expires in:"),default=expiry())
    
    
    
   
    
    
    