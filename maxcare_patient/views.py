from django.db.models import F,Q
from django.http import JsonResponse
import json
import re
# import magic
from django.conf import settings
from django.shortcuts import get_object_or_404
from maxcare_patient.models import *
from django.contrib.auth import authenticate, login, logout
import os

# Create your views here.
def patient_registration(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        first_name = data.get('first_name')
        if not first_name.isalpha():
            print(first_name)
            return JsonResponse({"Err":"Invalid First name, should be in alphabets"}, status=422)
        last_name = data.get('last_name')
        e_mail = data.get('email')
        if not e_mail:
            print('Email')
            return JsonResponse({"Err":"Email is required"},status=422)
        if not bool(re.match(r"[a-zA-Z0-9_\-\.]+[@][a-z]+[\.][a-z]{2,3}",e_mail)):
            print('err in email format')
            return JsonResponse({"Err":"Invalid Email, should in the form abc@xyz.com"},status=422)
        mobile = data.get('mobile')
        if not (mobile.isnumeric() and len(mobile) == 10):
            print(mobile)
            print('err in mobile')
            return JsonResponse({"Err":"Invalid Phone, shoud be of 10 digits and numeric"},status=422)
        passwd_1 = data.get('passwd1')
        passwd_2 = data.get('passwd2')
        if not (passwd_1 and passwd_2):
            print('err in Password')
            return JsonResponse({"Err":"Both passwords are required"},status=422)
        if passwd_1 != passwd_2:
            print('err in Password')
            return JsonResponse({"status":"passwords do not match"}, status=409)
        if not bool(re.match(r"^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,16}$",passwd_1)):
            print('err in Password')
            return JsonResponse({"Err":"Weak Password, should include an upper case, a number, an special Symbol and should be of length between 8 to 16"},status=400)
        gender = data.get('gender')
        if not gender:
            print('err in Gender')
            return JsonResponse({'status':'GENDER is required'},status=422)
        address = data.get('address')
        if not address:
            print('err in address')
            return JsonResponse({'status':'ADDRESS is required'},status=422)
        city = data.get('city')
        if not city:
            print('err in City')
            return JsonResponse({'status':'CITY is required'},status=422)
        state = data.get('state')
        if not state:
            print('err in state')
            return JsonResponse({'status':'STATE is required'},status=422)
        pincode = data.get('pincode')
        if not pincode:
            print('err in pincode')
            return JsonResponse({'status':'PINCODE is required'},status=422)
        dob = data.get('dob')
        if not dob:
            print('err in dob')
            return JsonResponse({'status':'DOB is required'},status=422)
        dob = dob.split('-')
        dob = date(int(dob[0]),int(dob[1]),int(dob[2]))
        marital_status = data.get('maritalStatus')
        emergency_contact = data.get('emergency_contact')
        if not emergency_contact:
            print('err in emergency')
            return JsonResponse({'status':'EMERGENCY CONTACT is required'},status=422)
        weight = data.get('Weight')
        if not weight:
            print('err in wgt')
            return JsonResponse({'status':'WEIGHT is required'},status=422)
        height = data.get('height')
        if not height:
            print('err in hgt')
            return JsonResponse({'status':'HEIGHT is required'},status=422)
        daibitic = data.get('diabitic')
        blood_grp = data.get('blood_Group')
        if not blood_grp:
            print('err in blood_grp')
            return JsonResponse({'status':'BLOOD GRP is required'},status=422)
        blood_grp = list(Patient.choices_of_blood.keys())[list(Patient.choices_of_blood.values()).index(blood_grp)]
        allergy = data.get('allergy')
        med_issue = data.get('prv_medissue')
        if MyUser.objects.filter(email=e_mail).exists():
            return JsonResponse({"status":"User already exists with this email"},status=409)
        pat = Patient(first_name=first_name,last_name=last_name,email=e_mail,password=passwd_1,phone_number=mobile,gender=gender,address=address,dob=dob,marital_status=marital_status,emergency_contact=emergency_contact,weight=weight,height=height,daibitic=daibitic,blood_grp=blood_grp,pincode=pincode,allergy=allergy,med_issue=med_issue)
        pat.save()
        return JsonResponse({'status':'Patient registered Succesfully'})
    return JsonResponse({"status":"Invalid request method"},status=405)

def signin(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        e_mail = data.get('email')
        passwd = data.get('passwd')
        if e_mail and passwd:
            if MyUser.objects.filter(email=e_mail).exists():
                User = authenticate(email=e_mail,password=passwd)
                print(User)
                if User is not None:
                    login(request,User)
                    return JsonResponse({"status":"Logged in Successfully", "is_admin": User.is_superuser, 'is_doctor':User.is_doctor, 'is_patient':User.is_patient},status=200 )
                return JsonResponse({"Err":"Password entered is incorrect"},status=400)
            return JsonResponse({"Err":"No user with these credentials"},status=400)
        return JsonResponse({'Err':'Email and Password are required'},status=422)
    return JsonResponse({"Err":"Invalid request method"},status=405)


