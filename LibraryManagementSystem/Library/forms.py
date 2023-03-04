
from .models import Book
from django import forms

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
        
    
    
    