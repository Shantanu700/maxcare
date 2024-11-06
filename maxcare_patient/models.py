from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from datetime import datetime


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
        extra_fields.setdefault("type",MyUser.Types.ADMIN)
        return self.create_user(email, password, **extra_fields)


class MyUser(AbstractUser):
    class Types(models.TextChoices): 
        PATIENT = "PATIENT" , "patient"
        DOCTOR = "DOCTOR" , "doctor"
        ADMIN = "RECEPTIONIST" , "receptionist"
    type = models.CharField(max_length = 15 , choices = Types.choices, default = Types.PATIENT) 
    choices_of_marital_status = {
        "UM":"Unmarrid",
        "MA":"Married",
        "DI":"Divorced",
        "W":"Widowed"
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
    pincode = models.IntegerField(null=True)
    dob = models.DateField(null=False)
    marital_status = models.CharField(max_length=2, choices=choices_of_marital_status, default='UM')
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name','phone_number','gender','address','city','state','pincode','dob']

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
    is_daibitic = models.BooleanField(default=False,null=True)
    blood_grp = models.CharField(max_length=3, null=True, choices=choices_of_blood)
    allergy = models.CharField(max_length=255, null=True)
    med_issue = models.CharField(max_length=225, null=True)
    is_deleted = models.BooleanField(default=0)

    # objects = PatientManager()

    def save(self , *args , **kwargs): 
        self.type = MyUser.Types.PATIENT 
        self.set_password(self.password)
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

class Specialization(models.Model):
    degree = models.CharField(max_length=50,unique=False, default='MBBS')
    speciality = models.CharField(max_length=50)


class Doctor(MyUser):
    choices_of_degree = {
        'MBBS':'Bachelor of Medicine, Bachelor of Surgery',
        'BDS':'Bachelor of Dental Surgery',
        'BAMS':'Bachelor of Ayurvedic Medicine and Surgery',
        'BUMS':'Bachelor of Unani Medicine and Surgery',
        'BHMS':'Bachelor of Homeopathy Medicine and Surgery',
        'BYNS':'Bachelor of Yoga and Naturopathy Sciences',
        'B.V.Sc & AH':'Bachelor of Veterinary Sciences and Animal Husbandry',
    }
    doctor_details = models.OneToOneField(MyUser,parent_link=True, on_delete=models.CASCADE)
    # degree = models.CharField(max_length=50, null=False, blank=False, choices=choices_of_degree)
    specialization = models.ForeignKey(Specialization, on_delete=models.RESTRICT, default=1)
    experience = models.IntegerField(validators=[MinValueValidator(2)])
    doc_img = models.ImageField(max_length=500,upload_to='doctors')
    doc_fee = models.IntegerField(default=2000)
    is_deleted = models.BooleanField(default=0)
    # objects = DoctorManager()

    def save(self , *args , **kwargs): 
        self.type = MyUser.Types.DOCTOR 
        self.is_doctor = True
        self.set_password(self.password)
        return super().save(*args , **kwargs) 
    
class Appointments(models.Model):
    choices_of_status = {
        'Pending':'PENDING',
        'Request Initiated':'REQUEST INITIATED',
        'Paid':'PAID',
        'Confirmed':'CONFIRMED',
        'Prescribed':'PRESCRIBED',
        'Rejected':'REJECTED',
        'Refunded':'REFUNDED',
    }
    patient = models.ForeignKey(Patient,on_delete=models.RESTRICT)
    doctor = models.ForeignKey(Doctor, on_delete=models.RESTRICT)
    symptoms = models.TextField(max_length=510)
    symptoms_date = models.DateField()
    request_date = models.DateTimeField(default=datetime.now)
    prefered_date = models.DateField()
    status = models.CharField(max_length=20,default='Pending',choices=choices_of_status)
    transaction_id = models.CharField(max_length=15,null=True)
    admin_verf = models.BooleanField(default=0)
    doc_verf = models.BooleanField(default=0)
    admin_approval_datetime = models.DateTimeField(null=True)
    doctor_approval_datetime = models.DateTimeField(null=True)
    prescribed_datetime = models.DateTimeField(null=True)
    # btn_class = models.CharField(max_length=50,default='d-none')
    rejection_remark = models.TextField(max_length=510,null=True)

class sidebar(models.Model):
    name = models.CharField(max_length=25)
    url = models.CharField(max_length=25)
    priority = models.IntegerField()
    visibility = models.CharField(max_length=15,choices=MyUser.Types.choices, default=MyUser.Types.ADMIN)
    icon = models.CharField(max_length=50)

    class Meta:
        unique_together = ('visibility','priority')




class Precription(models.Model):
    medicine_name = models.CharField(max_length=100)
    valid_date = models.DateField()
    frequency = models.IntegerField(validators=[MaxValueValidator(3)])
    appoint = models.ForeignKey(Appointments, on_delete=models.RESTRICT)