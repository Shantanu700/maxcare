from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from datetime import date


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not password : 
            raise ValueError("Password is must !")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class MyUser(AbstractUser):
    class Types(models.TextChoices): 
        PATIENT = "PATIENT" , "patient"
        DOCTOR = "DOCTOR" , "doctor"
        ADMIN = "ADMIN" , "admin"
    type = models.CharField(max_length = 8 , choices = Types.choices, default = Types.PATIENT) 
    choices_of_marital_status = {
        "UM":"Unmarrid",
        "MA":"Married",
    }
    choices_of_gender = {
        "M":"Male",
        "F":"Female",
    }
    email = models.EmailField(max_length=50, null=False, unique=True)
    phone_number = models.CharField(max_length=10, null=False)
    gender = models.CharField(max_length=2,choices=choices_of_gender,null=False)
    address = models.TextField(max_length=510, null=False)
    city = models.CharField(max_length=20, null=False)
    state = models.CharField(max_length=30, null=False)
    pincode = models.IntegerField(null=False)
    dob = models.DateField(null=False)
    marital_status = models.CharField(max_length=2, choices=choices_of_marital_status, default='UM')
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def username(self):
        return self.get_username()

class PatientManager(models.Manager): 
    def create_user(self , email , password = None): 
        if not email or len(email) <= 0 :  
            raise  ValueError("Email field is required !") 
        if not password : 
            raise ValueError("Password is must !") 
        email  = email.lower() 
        user = self.model( 
            email = email 
        ) 
        user.set_password(password) 
        user.save(using = self._db) 
        return user 
      
    def get_queryset(self , *args,  **kwargs): 
        queryset = super().get_queryset(*args , **kwargs) 
        queryset = queryset.filter(type = MyUser.Types.PATIENT) 
        return queryset     

class Patient(MyUser):
    choices_of_blood = {
        'a+':'A+',
        'b+':'B+',
        'a-':'A-',
        'b-':'B-',
        'ab-':'AB-',
        'o-':'O-',
        'ab+':'AB+',
        'o+':'O+',
    }
    patient_details = models.OneToOneField(MyUser,parent_link=True, on_delete=models.CASCADE)
    emergency_contact = models.CharField(max_length=10,null=False)
    weight = models.FloatField(null=False)
    height = models.FloatField(null=False)
    daibitic = models.BooleanField(default=False,null=True)
    blood_grp = models.CharField(max_length=3,null=False, choices=choices_of_blood)
    allergy = models.CharField(max_length=20)
    med_issue = models.CharField(max_length=225)

    objects = PatientManager()

    def save(self , *args , **kwargs): 
        self.type = MyUser.Types.PATIENT 
        self.is_patient = True
        return super().save(*args , **kwargs) 

class DoctorManager(models.Manager): 
    def create_user(self , email , password = None): 
        if not email or len(email) <= 0 :  
            raise  ValueError("Email field is required !") 
        if not password : 
            raise ValueError("Password is must !") 
        email  = email.lower() 
        user = self.model( 
            email = email 
        ) 
        user.set_password(password) 
        user.save(using = self._db) 
        return user 
      
    def get_queryset(self , *args,  **kwargs): 
        queryset = super().get_queryset(*args , **kwargs) 
        queryset = queryset.filter(type = MyUser.Types.DOCTOR) 
        return queryset

class Doctor(MyUser):
    doctor_details = models.OneToOneField(MyUser,parent_link=True, on_delete=models.CASCADE)
    degree = models.CharField(max_length=50, null=False, blank=False)
    specialization = models.CharField(max_length=50, null=False, blank=False)
    experience = models.IntegerField(validators=[MinValueValidator(2)])
    doc_img = models.ImageField(max_length=500,upload_to='doctors')


    objects = DoctorManager()

    def save(self , *args , **kwargs): 
        self.type = MyUser.Types.DOCTOR 
        self.is_doctor = True
        return super().save(*args , **kwargs) 