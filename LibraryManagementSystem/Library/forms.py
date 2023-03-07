
from .models import Book,Student
from django import forms
from datetime import date ,timedelta

class add_book_form(forms.ModelForm): #there is a diifference between Form and ModelForm 
                                     #form dosn't hhave save method  ,it's not used to create 
                                     #model objects 
                                     #it is used to gather data 
                                     #but model form can be saved using save method 
                                     #and it is used to save model objetcs
    
    name=forms.CharField(label="Book Name", max_length=50, required=True,widget=forms.TextInput(attrs={
        "class":"bookInfo",
        "name":"bookName",
        "type":"text",
        "id":"id_name",
        
    }))
    
    author = forms.CharField(label="Author", max_length=50, required=True,widget=forms.TextInput(attrs={
        "class":"bookInfo",
        "name":"author",
        "type":"text",
        "id":"id_author",
    }))
    
    
    isbn = forms.IntegerField(label="ISBN", required=True,max_value=9999999999999,min_value=1000000000000,widget=forms.TextInput(attrs={
        "class":"bookInfo",
        "name":"author",
        "type":"number",
        "id":"id_isbn",
        "max":"9999999999999",
        "min":"1000000000000",
        
    }))
    
    
    
    category=forms.CharField(label="Category", max_length=50, required=True,initial="N/A",widget=forms.TextInput(attrs={
        "class":"bookInfo",
        "name":"category",
        "type":"text",
        "id":"id_category"
    }))
    
    
    class Meta:
        model = Book
        fields=['name','author','isbn','category']
        
# ----------------------Search Forms ------------------
class SearchFilterWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search','name':'item'}),
            forms.Select(attrs={'class': 'form-control',
                                'name':'by'}, choices=[('name', 'Name'), ('isbn', 'ISBN'), ('book', 'Book')]),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split(',')
        return [None, None]

class SearchFilterField(forms.MultiValueField):
    widget = SearchFilterWidget

    def __init__(self, *args, **kwargs):
        fields = [
            forms.CharField(),
            forms.CharField(),
        ]
        super().__init__(fields, *args, **kwargs)

    def compress(self, values):
        if values:
            return ','.join(values)
        return ''
    
    
# this is not a model form 
# it is only used to retrieve the search item from
#search box 

class searchForm(forms.Form):
    SEARCH_BY_CHOICES = (('std_name','Student Name'),('book_name','Book Name'),('isbn','ISBN'))
    item=forms.CharField (label='',max_length=50, required=True,widget=forms.TextInput(
        attrs={
            "class":"form-control",
            "placeholder":"search",
            "type":"text",
            "label":"none",
            "name":"item"
            }
        )
        )
    searchBy = forms.ChoiceField(label='', choices=SEARCH_BY_CHOICES, required=False,initial=SEARCH_BY_CHOICES[0],
                                 widget=forms.Select(attrs={
                                     "class":"Default select example mb-3" ,
                                     "aria-label":".form-select-lg example",
                                     "name":"searchBy",
                                 })
                                 )
    
    
    

class IssueBookForm (forms.Form):
    BOOKS=Book.objects.all()
    STUDENTS=Student.objects.all()
    print(BOOKS[0])
    print(STUDENTS[0])
    books= forms.ModelChoiceField(label='Choose a Book :', queryset=BOOKS, required=True,initial=BOOKS[0],
                             
                             widget=forms.Select(attrs={
                                    "class":"form-select" ,
                                    "aria-label":"Default select ",
                                    "name":"book",
                                 
                             }))
    
    students= forms.ModelChoiceField(label='Choose a Student :', queryset=STUDENTS, required=True,initial=STUDENTS[0],
                             
                             widget=forms.Select(attrs={
                                    "class":"form-select" ,
                                    "aria-label":"Default select ",
                                    "name":"student",
                                 
                             }))
    
    def expiry():
        return date.today()+timedelta(days=14)
    
    issued_date =forms.DateField(label='Issued on:',initial=date.today(),widget=forms.DateInput(attrs={
        "class":"form-control",
        "type":"date",
        "name":"issued_date",
        
    }))
    expiry_date=forms.DateField(label='Expires on:',initial=expiry(),widget=forms.DateInput(attrs={
        "class":"form-control",
        "type":"date",
        "name":"expiry_date",
    }))
    
    
class DeleteForm(forms.Form):
    issued_book_id=forms.CharField(label='', max_length=50, required=False,widget=forms.TextInput(attrs={
        
        "type":"text",
        "value":"",# when the form is included in the tabel as Delete buttons we pass student_id to it as {{id}}
        "name":"issued_book_id",
        "class":"issued_book_id",
    }))
    

            
            
