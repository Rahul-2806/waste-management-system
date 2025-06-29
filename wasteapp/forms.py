from django import forms
from django.forms import CharField
from wasteapp.models import pmodel,Staff,Customer


class pform(forms.Form):
    Img = forms.FileField()
    
    class Meta:
        model = pmodel
        fields = ['Item','Category','Subcategory','Des','Amnt','Img']



from django import forms

class StaffForm(forms.Form):
    name = forms.CharField(max_length=100)    # Staff Name
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])  # Gender: M or F
    dob = forms.DateField()  # Date of Birth
    address = forms.CharField(max_length=255)  # Address
    place = forms.CharField(max_length=100)    # Place
    phone = forms.CharField(max_length=15)     # Phone
    adhaar = forms.CharField(max_length=12)    # Aadhaar Number
    email = forms.EmailField()                 # Email
    img = forms.FileField(required=False)      # Profile Image (Optional)

    class Meta:
        model = Staff  # Assuming `Staff` is your model
        fields = ['name', 'gender', 'dob', 'address', 'place', 'phone', 'adhaar', 'email', 'img']



class CustomerForm(forms.Form):
    name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=15)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    email = forms.EmailField()
    Img = forms.ImageField(required=False)  

    class Meta:
        model = Customer  # Assuming `Customer` is your model
        fields = ['Name','Address', 'Phone','Gender', 'Email', 'Img']






        