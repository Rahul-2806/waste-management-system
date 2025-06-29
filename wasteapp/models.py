from django.db import models

# Create your models here.

class pmodel(models.Model):
    Item = models.CharField(max_length=100)
    Category = models.CharField(max_length=100)
    Subcategory = models.CharField(max_length=100)
    Des = models.CharField(max_length=100)
    Amnt = models.CharField(max_length=100)
    Stock = models.CharField(max_length=100)
    Img = models.FileField(upload_to='Products')

    class Meta:
        db_table = "product"


from django.db import models

class Staff(models.Model):
    sid = models.AutoField(primary_key=True)  # Staff ID
    name = models.CharField(max_length=100)   # Staff Name
    gender = models.CharField(max_length=10)  # Gender (M/F)
    dob = models.DateField()                  # Date of Birth
    address = models.CharField(max_length=255)  # Address
    place = models.CharField(max_length=100)   # Place
    phone = models.CharField(max_length=15)   # Phone number
    adhaar = models.CharField(max_length=12)  # Aadhar number (assuming 12 digits)
    email = models.EmailField(max_length=100) # Email address
    img = models.ImageField(upload_to='staff_images/')  # Image field for staff photo

    class Meta:
        db_table = "staff"  # The table name in the database

    def __str__(self):
        return self.name  # Return the staff name when displaying the instancez
    


class Customer(models.Model):
    Cid = models.AutoField(primary_key=True)  # Customer ID
    Name = models.CharField(max_length=100)   # Customer Name
    Address = models.CharField(max_length=255)  # Address
    Phone = models.CharField(max_length=15)   # Phone number
    Gender = models.CharField(max_length=10)  # Gender (M/F)
    Email = models.EmailField(max_length=100) # Email address
    
    Img = models.ImageField(upload_to='customer_images/')  # Image field for customer photo

    class Meta:
        db_table = "customer"  # The table name in the database

    def __str__(self):
        return self.Name

        
        