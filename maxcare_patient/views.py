from django.db.models import F,Q
from django.http import JsonResponse
import json
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import re
from django.utils.html import strip_tags
import magic
from django.conf import settings
from django.shortcuts import get_object_or_404
from maxcare_patient.models import *
from django.contrib.auth import authenticate, login, logout
import os
from django.shortcuts import redirect
from datetime import date,datetime,timedelta


def patient_registration(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        first_name = data.get('first_name')
        if not first_name.isalpha():
            print(first_name)
            return JsonResponse({"status":"Invalid First name, should be in alphabets"}, status=422)
        last_name = data.get('last_name')
        e_mail = data.get('email')
        if not e_mail:
            print('Email')
            return JsonResponse({"status":"Email is required"},status=422)
        if not bool(re.match(r"[a-zA-Z0-9_\-\.]+[@][a-z]+[\.][a-z]{2,3}",e_mail)):
            print('err in email format')
            return JsonResponse({"status":"Invalid Email, should in the form abc@xyz.com"},status=422)
        mobile = data.get('mobile')
        if not (mobile.isnumeric() and len(mobile) == 10):
            print(mobile)
            print('err in mobile')
            return JsonResponse({"status":"Invalid Phone, shoud be of 10 digits and numeric"},status=422)
        passwd_1 = data.get('passwd1')
        passwd_2 = data.get('passwd2')
        if not (passwd_1 and passwd_2):
            print('err in Password')
            return JsonResponse({"status":"Both passwords are required"},status=422)
        if passwd_1 != passwd_2:
            print('err in Password')
            return JsonResponse({"status":"passwords do not match"}, status=409)
        if not bool(re.match(r"^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,16}$",passwd_1)):
            print('err in Password')
            return JsonResponse({"status":"Weak Password, should include an upper case, a number, an special Symbol and should be of length between 8 to 16"},status=400)
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
        pat = Patient(first_name=first_name,last_name=last_name,email=e_mail,password=passwd_1,phone_number=mobile,gender=gender,address=address,dob=dob,marital_status=marital_status,emergency_contact=emergency_contact,weight=weight,height=height,daibitic=daibitic,blood_grp=blood_grp,pincode=pincode,allergy=allergy,med_issue=med_issue,city=city,state=state)
        pat.save()
        return JsonResponse({'status':'Patient registered Succesfully','route':'/patient/patientappointment'})
    return JsonResponse({"status":"Invalid request method"},status=405)

def doctor_registration(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        first_name = data.get('first_name')
        if not first_name.isalpha():
            return JsonResponse({"status":"Invalid First name, should be in alphabets"}, status=422)
        last_name = data.get('last_name')
        e_mail = data.get('email')
        if not e_mail:
            return JsonResponse({"status":"Email is required"},status=422)
        if not bool(re.match(r"[a-zA-Z0-9_\-\.]+[@][a-z]+[\.][a-z]{2,3}",e_mail)):
            return JsonResponse({"status":"Invalid Email, should in the form abc@xyz.com"},status=422)
        mobile = data.get('mobile')
        if not (mobile.isnumeric() and len(mobile) == 10):
            return JsonResponse({"status":"Invalid Phone, shoud be of 10 digits and numeric"},status=422)
        passwd_1 = data.get('passwd1')
        passwd_2 = data.get('passwd2')
        if not (passwd_1 and passwd_2):
            return JsonResponse({"status":"Both passwords are required"},status=422)
        if passwd_1 != passwd_2:
            return JsonResponse({"status":"passwords do not match"}, status=409)
        if not bool(re.match(r"^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,16}$",passwd_1)):
            return JsonResponse({"status":"Weak Password, should include an upper case, a number, an special Symbol and should be of length between 8 to 16"},status=400)
        gender = data.get('gender')
        if not gender:
            return JsonResponse({'status':'GENDER is required'},status=422)
        address = data.get('address')
        if not address:
            return JsonResponse({'status':'ADDRESS is required'},status=422)
        city = data.get('city')
        if not city:
            return JsonResponse({'status':'CITY is required'},status=422)
        state = data.get('state')
        if not state:
            return JsonResponse({'status':'STATE is required'},status=422)
        pincode = data.get('pincode')
        if not pincode:
            return JsonResponse({'status':'PINCODE is required'},status=422)
        dob = data.get('dob')
        if not dob:
            return JsonResponse({'status':'DOB is required'},status=422)
        dob = dob.split('-')
        dob = date(int(dob[0]),int(dob[1]),int(dob[2]))
        marital_status = data.get('maritalStatus')
        degree = data.get('degree')
        if not degree:
            return JsonResponse({'status':'DEGREE is required'},status=422)
        specialization = data.get('specialization')
        if not specialization:
            return JsonResponse({'status':'SPECIALIZATION is required'},status=422)
        experience = int(data.get('experience'))
        if not experience:
            return JsonResponse({'status':'EXPERIENCE is required'},status=422)
        doc_img = request.FILES.get('file')
        if not doc_img:
            return JsonResponse({'status':'DOCTOR IMAGE is required'},status=422)
        ext = doc_img.name.split('.')[-1]
        content_type = doc_img.content_type
        mime_type = magic.from_buffer(doc_img.read(1024), mime=True)
        size = doc_img.size
        if size > settings.MAX_IMG_SIZE:
            return JsonResponse({'status':f'size {size} larger than 1 MB'},status=422)
        if content_type not in settings.ALLOWED_IMG_TYPES.values():
            return JsonResponse({'status':'invalid image content-type'},status=422)
        if ext not in settings.ALLOWED_IMG_TYPES.keys():
            return JsonResponse({'status':'invalid image extension'},status=422)
        if mime_type not in settings.ALLOWED_IMG_TYPES.values() and mime_type != content_type:
            return JsonResponse({'status':'invalid image mime-type'},status=422)
        if MyUser.objects.filter(email=e_mail).exists():
            return JsonResponse({"status":"User already exists with this email"},status=409)
        doc = Doctor(first_name=first_name,last_name=last_name,email=e_mail,password=passwd_1,phone_number=mobile,gender=gender,address=address,dob=dob,marital_status=marital_status,pincode=pincode,degree=degree,specialization=specialization,experience=experience,doc_img=doc_img,city=city,state=state)
        doc.save()
        return JsonResponse({'status':'Doctor registered Succesfully','route':'/doctor/drpendingappointments'})
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
                    return JsonResponse({"status":"Logged in Successfully", "is_admin": User.is_superuser, 'is_doctor':User.is_doctor, 'is_patient':User.is_patient,'route':f'/{User.type.lower()}'},status=200 )
                return JsonResponse({"status":"Password entered is incorrect"},status=400)
            return JsonResponse({"status":"No user with these credentials"},status=400)
        return JsonResponse({'status':'Email and Password are required'},status=422)
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_doctor:
                return JsonResponse({'route':'/doctor/drpendingAppointments'})
            elif request.user.is_patient:
                return JsonResponse({'route':'/patient/patientappointment'})
            elif request.user.is_superuser:
                return JsonResponse({'route':'/receptionist/appointments'})
            else:
                return JsonResponse({'route':'/login'})
        return JsonResponse({"status":"No User was autherized"},status=400)
    return JsonResponse({"status":"Invalid request method"},status=405)

def signout(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({"status":"Logged out Successfully",'route':'/login'},status=200 )
        return JsonResponse({"status":"No User was autherized"},status=400)
    return JsonResponse({"status":"Invalid request method"},status=405)

def info(request):
    if request.method == 'GET':
        docs = Doctor.objects.all().values('first_name','last_name','doc_img','degree','specialization','experience','doc_fee','id')
        return JsonResponse(list(docs),safe=False)

def side_panel(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_patient:
                data = sidebar.objects.filter(visibility=MyUser.Types.PATIENT).values('name','url','icon').order_by('priority')
                return JsonResponse(list(data),safe=False)
            elif request.user.is_superuser:
                data = sidebar.objects.filter(visibility=MyUser.Types.ADMIN).values('name','url','icon').order_by('priority')
                return JsonResponse(list(data),safe=False)
            elif request.user.is_doctor:
                data = sidebar.objects.filter(visibility=MyUser.Types.DOCTOR).values('name','url','icon').order_by('priority')
                return JsonResponse(list(data),safe=False)
            return JsonResponse({'status':'You are no one here'},status=422)
        return JsonResponse({'status':'You are not authorized'},status=401)
    return JsonResponse({'status':'Invalid request method'},status=405)

def get_data(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                data = request.GET
                query_date = data.get('date')
                if query_date is None or not query_date:
                    query_date = datetime.today()
                else:
                    query_date = query_date.split('-')
                    query_date = date(int(query_date[0]),int(query_date[1]),int(query_date[2]))
                date_list = [['Date','Total Requests','Accepted by Receptionist','Rejected by Receptionist','Accepted by Doctor','Refunded']]
                for i in range(5):
                    find_date = query_date - timedelta(days=i)
                    total_queries = Appointments.objects.filter(request_date__date=find_date).count()
                    accepted_by_admin = Appointments.objects.filter(Q(request_date__date=find_date) & (Q(status='Request Initiated') | Q(status='Paid'))).count()
                    rejected_by_admin = Appointments.objects.filter(Q(request_date__date=find_date) & Q(status='Rejected')).count()
                    accepted_by_doc = Appointments.objects.filter(Q(request_date__date=find_date) & Q(status='Confirmed')).count()
                    refunded_by_doc = Appointments.objects.filter(Q(request_date__date=find_date) & Q(status='Refunded')).count()
                    find_date_list = [find_date.strftime("%d-%m-%Y"),total_queries,accepted_by_admin,rejected_by_admin,accepted_by_doc,refunded_by_doc]
                    date_list.append(find_date_list)
                return JsonResponse(date_list,safe=False)
            return JsonResponse({'status':"You don't have access to update any thing here"},status=401)
        return JsonResponse({'status':'Unauthorised'},status=401)
    return JsonResponse({"status":"Invalid request method"},status=400)


                 


def manage_appointments(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_patient:
                data = Appointments.objects.filter(patient_id=request.user.id).order_by('-request_date').values('doctor__first_name','doctor__last_name','prefered_date','status','symptoms','btn_class')
                return JsonResponse(list(data),safe=False)
            elif request.user.is_superuser:
                requested_status = request.GET.get('status')
                if requested_status.title() == 'Request Initiated':
                    data = Appointments.objects.filter(Q(status=requested_status) | Q(status='Paid')).values('id','patient__first_name','patient__last_name','doctor__first_name','doctor__last_name','prefered_date','status','symptoms','request_date').order_by('-request_date')
                    return JsonResponse(list(data),safe=False)
                data = Appointments.objects.filter(status=requested_status).values('id','patient__first_name','patient__last_name','doctor__first_name','doctor__last_name','prefered_date','status','symptoms','request_date').order_by('-request_date')
                return JsonResponse(list(data),safe=False)
            elif request.user.is_doctor:
                requested_status = request.GET.get('status')
                if requested_status.title() not in ['Paid','Confirmed']:
                    return JsonResponse({'status':'Invalid Status'},status=422)    
                data = Appointments.objects.filter(status=requested_status, doctor_id=request.user.id).values('id','patient__first_name','patient__last_name','doctor__first_name','doctor__last_name','prefered_date','status','symptoms','request_date').order_by('-request_date')
                return JsonResponse(list(data),safe=False)
            return JsonResponse({'status':'You are no one here'},status=400)
        return JsonResponse({'status':'Unautherised access'},status=401)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_patient:
                data = request.POST
                print(data)
                doc_id = data.get('doc_id')
                if doc_id is None:
                    return JsonResponse({"status":"Doctor ID is required"},status=422)
                symptoms = data.get('symptoms')
                if symptoms is None:
                    return JsonResponse({'status':'Symptoms are required'},status=422)
                symptoms_date = data.get('suffer_date')
                if symptoms_date is None or not symptoms_date:
                    return JsonResponse({'status':'Symptoms date is required'},status=422)
                symptoms_date = symptoms_date.split('-')
                symptoms_date = date(int(symptoms_date[0]),int(symptoms_date[1]),int(symptoms_date[2]))
                prefered_date = data.get('preferred_date')
                if prefered_date is None or not prefered_date:
                    return JsonResponse({'status':'Prefered date is required'},status=422)        
                prefered_date = prefered_date.split('-')
                prefered_date = date(int(prefered_date[0]),int(prefered_date[1]),int(prefered_date[2]))
                pat = Patient.objects.get(patient_details=request.user)
                appointment = Appointments(patient=pat,doctor_id=doc_id,symptoms=symptoms,symptoms_date=symptoms_date,prefered_date=prefered_date)
                appointment.save()
                return JsonResponse({'status':'Appointment requested successfully'})
            return JsonResponse({'status':'User is not patient'},status=405)
        return JsonResponse({'status':'No User logged in'},status=401)
    if request.method == 'PUT': 
        if request.user.is_authenticated:
            if request.user.is_superuser:
                data = json.loads(request.body)
                print(data)
                appo_id = data.get('id')
                if appo_id is None:
                    return JsonResponse({'status':'Appointment ID is required'},status=422)
                updated_status = data.get('updated_status')
                if updated_status is None or not updated_status:
                    return JsonResponse({'status':'Updated Status is required'},status=422)
                appoint = Appointments.objects.get(id=appo_id)
                if appoint.status in ['Confirmed','Rejected']:
                    return JsonResponse({'status':"You can't update this appointment"},status=422)
                if updated_status.title() == 'Request Initiated':
                    appoint.status = updated_status.title()
                    appoint.btn_class = 'btn-danger'
                    appoint.admin_verf = True
                    appoint.admin_approval_datetime = datetime.now()
                    appoint.save()
                    return JsonResponse({'status':'Status updated successfully'})
                if updated_status == 'Rejected':
                    appoint.status = updated_status
                    appoint.btn_class = 'd-none'
                    appoint.admin_verf = True
                    appoint.admin_approval_datetime = datetime.now()
                    remark = data.get('remark')
                    if remark is None:
                        return JsonResponse({'status':'Remark is required for rejection'},status=422)
                    appoint.rejection_remark = remark
                    appoint.save()
                    return JsonResponse({'status':'Status updated successfully'})
                return JsonResponse({'status':'Invalid status'},status=422)
            elif request.user.is_doctor:
                data = json.loads(request.body)
                appo_id = data.get('id')
                if appo_id is None or not appo_id:
                    return JsonResponse({'status':'Appointment ID is required'},status=422)
                updated_status = data.get('updated_status')
                if updated_status is None or not updated_status:
                    return JsonResponse({'status':'Updated Status is required'},status=422)
                appoint = Appointments.objects.get(id=appo_id)
                if appoint.status != 'Paid':
                    return JsonResponse({'status':"You can't update this appointment"},status=422)
                if updated_status == 'Confirmed':
                    appoint.status = updated_status
                    appoint.btn_class = 'd-none'
                    appoint.doc_verf = True
                    appoint.doctor_approval_datetime = datetime.now()
                    appoint.save()
                    subject, from_email, to = "Appointment confirmation on Maxcare Health", "shantanugupta13524@gmail.com", appoint.patient.email
                    html_content = render_to_string('html_mail.html',{'username':appoint.patient.first_name,'doctor_first_name':appoint.doctor.first_name,'doctor_last_name':appoint.doctor.last_name,'date':appoint.prefered_date,'day':appoint.prefered_date.strftime('%A')})
                    text_content = strip_tags(html_content)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    return JsonResponse({'status':'Status updated successfully'})
                if updated_status == 'Refunded':
                    appoint.status = updated_status
                    appoint.btn_class = 'd-none'
                    appoint.doc_verf = True
                    appoint.doctor_approval_datetime = datetime.now()
                    remark = data.get('remark')
                    if remark is None:
                        return JsonResponse({'status':'Remark is required for rejection'},status=422)
                    appoint.rejection_remark = remark
                    appoint.save()
                    return JsonResponse({'status':'Status updated successfully'})
                return JsonResponse({'status':'Invalid update status'},status=422)
            return JsonResponse({'status':"You don't have access to update any thing here"},status=401)
        return JsonResponse({'status':'Unauthorised'},status=401)
    return JsonResponse({"status":"Invalid request method"},status=400)
            

def test(request):
    if request.method == 'POST':
        # text = render_to_string()

        subject, from_email, to = "Appointment confirmation on Maxcare Health", "shantanugupta13524@gmail.com", "shantanugupta13524@gmail.com"
        text_content = "This is an important message."
        html_content = render_to_string('html_mail.html',{'username':'Shantanu'})
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return JsonResponse({'status':'Mail sent successfully'})
    # if request.method == 'POST':
    #     if request.user.is_authenticated:
    #         if request.user.is_superuser:
    #             data = json.loads(request.body)
    #             query_date = data.get('date')
    #             if query_date is None or not query_date:
    #                 query_date = datetime.today()
    #             else:
    #                 query_date = query_date.split('-')
    #                 query_date = date(int(query_date[0]),int(query_date[1]),int(query_date[2]))
    #             date_list = [['Date','Total Requests','Accepted by Receptionist','Rejected by Receptionist','Accepted by Doctor','Refunded']]
    #             for i in range(5):
    #                 find_date = query_date - timedelta(days=i)
    #                 total_queries = Appointments.objects.filter(request_date__date=find_date).count()
    #                 accepted_by_admin = Appointments.objects.filter(Q(request_date__date=find_date) & (Q(status='Request Initiated') | Q(status='Paid'))).count()
    #                 rejected_by_admin = Appointments.objects.filter(Q(request_date__date=find_date) & Q(status='Rejected')).count()
    #                 accepted_by_doc = Appointments.objects.filter(Q(request_date__date=find_date) & Q(status='Confirmed')).count()
    #                 refunded_by_doc = Appointments.objects.filter(Q(request_date__date=find_date) & Q(status='Refunded')).count()
    #                 find_date_list = [find_date.strftime("%d-%m-%Y"),total_queries,accepted_by_admin,rejected_by_admin,accepted_by_doc,refunded_by_doc]
    #                 date_list.append(find_date_list)
    #             return JsonResponse(date_list,safe=False)
    #         return JsonResponse({'status':"You don't have access to update any thing here"},status=401)
    #     return JsonResponse({'status':'Unauthorised'},status=401)
    return JsonResponse({"status":"Invalid request method"},status=400)
