from django.db.models import F,Q
from django.core.paginator import Paginator
from django.core.files import File
from django.http import JsonResponse,HttpResponse
import json
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string,get_template,select_template
import re
from django.utils.html import strip_tags
import magic
from django.conf import settings
from django.shortcuts import get_object_or_404
from maxcare_patient.models import *
from django.contrib.auth import authenticate, login, logout
import os
from django.shortcuts import redirect,render
from datetime import date,datetime,timedelta
from django_renderpdf.helpers import render_pdf 

def patient_registration(request):
    if request.method == 'GET':
        data_choices_of_marital_status = list(MyUser.choices_of_marital_status.items())
        data_choices_of_gender = list(MyUser.choices_of_gender.items())
        data_choices_of_blood = list(Patient.choices_of_blood.items())
        return JsonResponse({'marital_status':data_choices_of_marital_status,'gender':data_choices_of_gender,'blood':data_choices_of_blood})
    if request.method == 'POST':
        data = request.POST
        first_name = data.get('first_name')
        if first_name is None or not first_name.isalpha():
            return JsonResponse({"status":"Invalid First name, should be in alphabets"}, status=422)
        first_name = first_name.strip()
        last_name = data.get('last_name')
        if last_name is not None:
            if not last_name.isalpha():
                return JsonResponse({"status":"Invalid last name, should be in alphabets"}, status=422)
            last_name = last_name.strip()
        else:
            last_name = ''
        e_mail = data.get('email')
        if not e_mail:
            return JsonResponse({"status":"Email is required"},status=422)
        if not bool(re.match(r"[a-zA-Z0-9_\-\.]+[@][a-z]+[\.][a-z]{2,3}",e_mail)):
            return JsonResponse({"status":"Invalid Email, should in the form abc@xyz.com"},status=422)
        mobile = data.get('mobile')
        if mobile is None or not (mobile.isnumeric() and len(mobile) == 10):
            return JsonResponse({"status":"Invalid Phone, shoud be of 10 digits and numeric"},status=422)
        passwd_1 = data.get('passwd1')
        passwd_2 = data.get('passwd2')
        if not (passwd_1 and passwd_2):
            return JsonResponse({"status":"Both passwords are required"},status=422)
        if passwd_1 != passwd_2:
            print('err in Password')
            return JsonResponse({"status":"passwords do not match"}, status=409)
        if not bool(re.match(r"^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,16}$",passwd_1)):
            print('err in Password')
            return JsonResponse({"status":"Weak Password, should include an upper case, a number, an special Symbol and should be of length between 8 to 16"},status=400)
        gender = data.get('gender')
        if gender is None or gender not in MyUser.choices_of_gender.keys():
            return JsonResponse({'status':'Gender is invalid'},status=422)
        # gender = list(Patient.choices_of_gender.keys())[list(Patient.choices_of_gender.values()).index(gender)]        
        address = data.get('address')
        if not address:
            return JsonResponse({'status':'Address is required'},status=422)
        city = data.get('city')
        if not city or (len(city) > 20 or len(city) < 2):
            print('err in City')
            return JsonResponse({'status':'City is invalid'},status=422)
        state = data.get('state')
        if not state or len(state) > 30:
            print('err in state')
            return JsonResponse({'status':'State is required'},status=422)
        pincode = data.get('pincode')
        if pincode:
            if len(pincode) != 6:
                return JsonResponse({'status':'Pincode is invalid'},status=422)
        else:
            pincode = None
        dob = data.get('dob')
        if not dob:
            return JsonResponse({'status':'DOB is required'},status=422)
        if not bool(re.match(r'^([20]{2}|[19]{2})?[0-9]{2}(-)(1[0-2]|0?[1-9])\2(3[01]|[12][0-9]|0?[1-9])$',dob)):
            return JsonResponse({'status':'Date of birth is invalid'},status=422)
        dob = dob.split('-')
        dob = date(int(dob[0]),int(dob[1]),int(dob[2]))
        marital_status = data.get('maritalStatus')
        if marital_status not in MyUser.choices_of_marital_status.keys():
            return JsonResponse({'status':'Invalid marital status'},status=422)
        # marital_status = list(Patient.choices_of_marital_status.keys())[list(Patient.choices_of_marital_status.values()).index(marital_status)]        
        emergency_contact = data.get('emergency_contact')
        if not emergency_contact or not (emergency_contact.isnumeric() and len(emergency_contact) == 10):
            return JsonResponse({'status':'EMERGENCY CONTACT is invalid'},status=422)
        weight = data.get('Weight')
        if not weight or not bool(re.match(r'^(\d{1,3})(()|(\.(\d{1,2})))$',weight)):
            return JsonResponse({'status':'Weight is invalid'},status=422)
        height = data.get('height')
        if not height or not bool(re.match(r'^(\d{2,3})(()|(\.(\d{1})))$',height)):
            return JsonResponse({'status':'Height is invalid'},status=422)
        daibitic = data.get('diabitic')
        blood_grp = data.get('blood_Group')
        if blood_grp:
            if blood_grp not in Patient.choices_of_blood.keys():
                return JsonResponse({'status':'Blood grp is invalid'},status=422)
        # blood_grp = list(Patient.choices_of_blood.keys())[list(Patient.choices_of_blood.values()).index(blood_grp)]
        allergy = data.get('allergy')
        if allergy:
            if len(allergy) > 255:
                return JsonResponse({'status':'Allergy is invalid'},status=422)
        med_issue = data.get('prv_medissue')
        if med_issue:
            if len(med_issue) > 255:
                return JsonResponse({'status':'Allergy is invalid'},status=422)
        if MyUser.objects.filter(email=e_mail).exists():
            return JsonResponse({"status":"User already exists with this email"},status=409)
        pat = Patient(first_name=first_name,last_name=last_name,email=e_mail,password=passwd_1,phone_number=mobile,gender=gender,address=address,dob=dob,marital_status=marital_status,emergency_contact=emergency_contact,weight=weight,height=height,is_daibitic=daibitic,blood_grp=blood_grp,pincode=pincode,allergy=allergy,med_issue=med_issue,city=city,state=state)
        pat.save()
        User = authenticate(email=e_mail,password=passwd_1)
        login(request,User)
        return JsonResponse({'status':'Patient registered Succesfully','route':'/patient/patientappointment','user_auhenticated':request.user.is_authenticated})
    return JsonResponse({"status":"Invalid request method"},status=405)

def doctor_registration(request):
    if request.method == 'GET':
        degree = request.GET.get('degree')
        data_choices_of_degree = list(Doctor.choices_of_degree.keys())
        if degree is None:
            return JsonResponse({'degree':data_choices_of_degree})
        data_choices_of_specialization = list(Specialization.objects.filter(degree=degree).values('id','speciality'))
        return JsonResponse({'degree':data_choices_of_degree,'specialization':data_choices_of_specialization})
    if request.method == 'POST':
        data = request.POST
        first_name = data.get('first_name')
        if first_name is None or not first_name.isalpha():
            return JsonResponse({"status":"Invalid First name, should be in alphabets"}, status=422)
        first_name = first_name.strip()
        last_name = data.get('last_name')
        if last_name is not None:
            if not last_name.isalpha():
                return JsonResponse({"status":"Invalid last name, should be in alphabets"}, status=422)
            last_name = last_name.strip()
        else:
            last_name = ''
        e_mail = data.get('email')
        if not e_mail:
            return JsonResponse({"status":"Email is required"},status=422)
        if not bool(re.match(r"[a-zA-Z0-9_\-\.]+[@][a-z]+[\.][a-z]{2,3}",e_mail)):
            return JsonResponse({"status":"Invalid Email, should in the form abc@xyz.com"},status=422)
        mobile = data.get('mobile')
        if mobile is None or not (mobile.isnumeric() and len(mobile) == 10):
            return JsonResponse({"status":"Invalid Phone, shoud be of 10 digits and numeric"},status=422)
        passwd_1 = data.get('passwd1')
        passwd_2 = data.get('passwd2')
        if not (passwd_1 and passwd_2):
            return JsonResponse({"status":"Both passwords are required"},status=422)
        if passwd_1 != passwd_2:
            print('err in Password')
            return JsonResponse({"status":"passwords do not match"}, status=409)
        if not bool(re.match(r"^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,16}$",passwd_1)):
            print('err in Password')
            return JsonResponse({"status":"Weak Password, should include an upper case, a lower case, a number, an special Symbol and should be of length between 8 to 16"},status=400)
        gender = data.get('gender')
        if gender is None or gender not in MyUser.choices_of_gender.keys():
            return JsonResponse({'status':'Gender is invalid'},status=422)
        # gender = list(Patient.choices_of_gender.keys())[list(Patient.choices_of_gender.values()).index(gender)]        
        address = data.get('address')
        if not address:
            return JsonResponse({'status':'Address is required'},status=422)
        city = data.get('city')
        if not city or (len(city) > 20 or len(city) < 2):
            print('err in City')
            return JsonResponse({'status':'City is invalid'},status=422)
        state = data.get('state')
        if not state or len(state) > 30:
            print('err in state')
            return JsonResponse({'status':'State is required'},status=422)
        pincode = data.get('pincode')
        if pincode:
            if len(pincode) != 6:
                return JsonResponse({'status':'Pincode is invalid'},status=422)
        else:
            pincode = None
        dob = data.get('dob')
        if not dob:
            return JsonResponse({'status':'DOB is required'},status=422)
        if not bool(re.match(r'^([20]{2}|[19]{2})?[0-9]{2}(-)(1[0-2]|0?[1-9])\2(3[01]|[12][0-9]|0?[1-9])$',dob)):
            return JsonResponse({'status':'Date of birth is invalid'},status=422)
        dob = dob.split('-')
        dob = date(int(dob[0]),int(dob[1]),int(dob[2]))
        age = datetime.today.year - dob.year
        marital_status = data.get('maritalStatus')
        if marital_status not in MyUser.choices_of_marital_status.keys():
            return JsonResponse({'status':'Invalid marital status'},status=422)
        # if not degree:
        #     return JsonResponse({'status':'DEGREE is required'},status=422)
        # change 1
        specialization_id = data.get('specialization')
        print(specialization_id)
        if not specialization_id or not Specialization.objects.filter(id=specialization_id).exists():
            return JsonResponse({'status':'Invalid Specialization ID'},status=422)
        experience = data.get('experience')
        if not experience or (int(experience) < 2 and age-int(experience) >= 24):
            return JsonResponse({'status':'Experience is invalid'},status=422)
        doc_img = request.FILES.get('file')
        if not doc_img:
            return JsonResponse({'status':'Doctor Image is required'},status=422)
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
        doc = Doctor(first_name=first_name,last_name=last_name,email=e_mail,password=passwd_1,phone_number=mobile,gender=gender,address=address,dob=dob,marital_status=marital_status,pincode=pincode,specialization_id=specialization_id,experience=experience,doc_img=doc_img,city=city,state=state)
        doc.save()
        User = authenticate(email=e_mail,password=passwd_1)
        login(request,User)
        return JsonResponse({'status':'Doctor registered Succesfully','route':'/doctor/drpendingAppointments'})
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
        return JsonResponse({"status":"No User was autherized"},status=401)
    return JsonResponse({"status":"Invalid request method"},status=405)

def signout(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({"status":"Logged out Successfully",'route':'/login'},status=200 )
        return JsonResponse({"status":"No User was autherized"},status=401)
    return JsonResponse({"status":"Invalid request method"},status=405)

def info(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                pat_id = request.GET.get('id')
                if pat_id is None or not pat_id:
                    pat_lsit = Patient.objects.filter(is_deleted=0).values('first_name','last_name','id','email','gender')
                    doc_list = Doctor.objects.filter(is_deleted=0).values()
                    return JsonResponse({'doctors':list(doc_list),'patatients':list(pat_lsit)})
                else:
                    pat_lsit = Patient.objects.filter(id=pat_id).values('id','first_name','last_name','email','phone_number','gender','address','city','state','pincode','dob','marital_status','emergency_contact','weight','height','is_daibitic','blood_grp','allergy','med_issue')
                    return JsonResponse(list(pat_lsit),safe=False)
        # change 2
        docs = Doctor.objects.filter(is_deleted=0).values('first_name','last_name','doc_img','specialization__degree','specialization__speciality','experience','doc_fee','id')
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
                    accepted_by_admin = Appointments.objects.filter(Q(admin_approval_datetime__date=find_date) & (Q(status='Request Initiated') | Q(status='Paid'))).count()
                    rejected_by_admin = Appointments.objects.filter(Q(admin_approval_datetime__date=find_date) & Q(status='Rejected')).count()
                    accepted_by_doc = Appointments.objects.filter(Q(doctor_approval_datetime__date=find_date) & Q(status='Confirmed')).count()
                    refunded_by_doc = Appointments.objects.filter(Q(doctor_approval_datetime__date=find_date) & Q(status='Refunded')).count()
                    find_date_list = [find_date.strftime("%d-%m-%Y"),total_queries,accepted_by_admin,rejected_by_admin,accepted_by_doc,refunded_by_doc]
                    date_list.append(find_date_list)
                    print(date_list)
                return JsonResponse(date_list,safe=False)
            return JsonResponse({'status':"You don't have access to update any thing here"},status=401)
        return JsonResponse({'status':'Unauthorised'},status=401)
    return JsonResponse({"status":"Invalid request method"},status=400)

def manage_appointments(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_patient:
                requested_status = request.GET.get('status')
                if requested_status:
                    data = Appointments.objects.filter(patient_id=request.user.id,status=requested_status).order_by('-request_date').values('doctor__first_name','doctor__last_name','doctor__doc_fee','prefered_date','status','symptoms','id')
                else:
                    data = Appointments.objects.filter(patient_id=request.user.id).order_by('-request_date').values('doctor__first_name','doctor__last_name','doctor__doc_fee','prefered_date','status','symptoms','id')
                return JsonResponse(list(data),safe=False)
            elif request.user.is_superuser:
                requested_status = request.GET.get('status')
                request_page = request.GET.get('page_number')
                if request_page is None or not request_page:
                    request_page = 1
                if requested_status is not None:
                    if requested_status.title() == 'Request Initiated':
                        data = Appointments.objects.filter(Q(status=requested_status) | Q(status='Paid')).values('id','patient__first_name','patient__last_name','doctor__first_name','doctor__last_name','prefered_date','status','symptoms','request_date').order_by('-request_date')
                        return JsonResponse(list(data),safe=False)
                    data = Appointments.objects.filter(status=requested_status).values('id','patient__first_name','patient__last_name','doctor__first_name','doctor__last_name','prefered_date','status','symptoms','request_date').order_by('-request_date')                    
                    paginator = Paginator(data, 25)
                    page_obj = paginator.get_page(request_page)
                    print(page_obj.object_list, paginator.num_pages)
                    next_page = page_obj.next_page_number() if page_obj.has_next() else None
                    prev_page = page_obj.previous_page_number() if page_obj.has_previous() else None
                    print(prev_page, next_page)
                    return JsonResponse({'previous page':prev_page,'next page':next_page,'total_no_of_pages':paginator.num_pages,'data':list(page_obj.object_list),'no_of_records':len(list(page_obj.object_list))})
                return JsonResponse({'status':'Requested status is required'},status=422)
            elif request.user.is_doctor:
                requested_status = request.GET.get('status')
                if requested_status is not None:
                    if requested_status.title() not in ['Paid','Confirmed','Prescribed']:
                        return JsonResponse({'status':'Invalid Status'},status=422)    
                    data = Appointments.objects.filter(status=requested_status, doctor_id=request.user.id).values('id','patient__first_name','patient__last_name','doctor__first_name','doctor__last_name','prefered_date','status','symptoms','request_date').order_by('-request_date')
                    return JsonResponse(list(data),safe=False)
                return JsonResponse({'status':'Requested status is required'},status=422)
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
                if not Appointments.objects.filter(id=appo_id).exists():
                    return JsonResponse({'status':'Appointment for requested id not found'},status=404)
                appoint = Appointments.objects.get(id=appo_id)
                if appoint.status in ['Confirmed','Rejected','Refunded','Prescribed']:
                    return JsonResponse({'status':"You can't update this appointment"},status=422)
                if updated_status.title() == 'Request Initiated':
                    appoint.status = updated_status.title()
                    # appoint.btn_class = 'btn-danger'
                    appoint.admin_verf = True
                    appoint.admin_approval_datetime = datetime.now()
                    appoint.save()
                    subject, from_email, to = "Request initiated for appointment on Maxcare Health", "max.care13524@gmail.com", appoint.patient.email
                    html_content = render_to_string('RI_template.html',{'username':appoint.patient.first_name,'doctor_first_name':appoint.doctor.first_name,'doctor_last_name':appoint.doctor.last_name,'date':appoint.prefered_date,'day':appoint.prefered_date.strftime('%A')})
                    text_content = strip_tags(html_content)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send(fail_silently=True)
                    return JsonResponse({'status':'Status updated successfully'})
                if updated_status == 'Rejected':
                    appoint.status = updated_status
                    # appoint.btn_class = 'd-none'
                    appoint.admin_verf = True
                    appoint.admin_approval_datetime = datetime.now()
                    remark = data.get('remark')
                    if remark is None or not remark:
                        return JsonResponse({'status':'Remark is required for rejection'},status=422)
                    appoint.rejection_remark = remark
                    appoint.save()
                    subject, from_email, to = "Request canceled for appointment on Maxcare Health", "max.care13524@gmail.com", appoint.patient.email
                    print(remark)
                    html_content = render_to_string('Rejected_template.html',{'username':appoint.patient.first_name,'doctor_first_name':appoint.doctor.first_name,'doctor_last_name':appoint.doctor.last_name,'date':appoint.prefered_date,'day':appoint.prefered_date.strftime('%A'),'status':updated_status,'person':'Receptionist','reason':remark})
                    text_content = strip_tags(html_content)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send(fail_silently=True)
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
                if not Appointments.objects.filter(id=appo_id).exists():
                    return JsonResponse({'status':'Appointment for requested id not found'},status=404)
                appoint = Appointments.objects.get(id=appo_id)
                if appoint.status not in ['Paid']:
                    return JsonResponse({'status':"You can't update this appointment"},status=422)
                if updated_status == 'Confirmed':
                    appoint.status = updated_status
                    # appoint.btn_class = 'd-none'
                    appoint.doc_verf = True
                    appoint.doctor_approval_datetime = datetime.now()
                    appoint.save()
                    subject, from_email, to = "Appointment confirmation on Maxcare Health", "max.care13524@gmail.com", appoint.patient.email
                    html_content = render_to_string('html_mail.html',{'username':appoint.patient.first_name,'doctor_first_name':appoint.doctor.first_name,'doctor_last_name':appoint.doctor.last_name,'date':appoint.prefered_date,'day':appoint.prefered_date.strftime('%A')})
                    text_content = strip_tags(html_content)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send(fail_silently=True)
                    return JsonResponse({'status':'Status updated successfully'})
                if updated_status == 'Prescribed':
                    appoint.status = updated_status
                    # appoint.btn_class = 'd-none'
                    appoint.doc_verf = True
                    appoint.prescribed_datetime = datetime.now()
                    appoint.save()
                    #create pdf
                    data = Precription.objects.filter(appoint_id=appo_id).values('medicine_name', 'valid_date', 'frequency')
                    doc_info = Appointments.objects.filter(id=appo_id).values('doctor__first_name','doctor__last_name')
                    pat_info = Appointments.objects.filter(id=appo_id).values('patient__first_name','patient__last_name')
                    print(doc_info[0])
                    print(pat_info[0])
                    f = open('Media/doctors/prescription.pdf','wb+')
                    myfile = File(f) 
                    render_pdf(
                            template='prescription_template.html',
                            file_=myfile,
                            context={'result':list(data),
                                    'appointment_id':appo_id,
                                    'dr':doc_info[0],
                                    'pt':pat_info[0]
                                    },
                        )
                    f.close()
                    #send mail with attachment
                    subject, from_email, to = "Prescription of appointment on Maxcare Health", "max.care13524@gmail.com", appoint.patient.email
                    html_content = render_to_string('prescription_mail.html',{'username':appoint.patient.first_name,'doctor_first_name':appoint.doctor.first_name,'doctor_last_name':appoint.doctor.last_name,'date':appoint.prefered_date,'day':appoint.prefered_date.strftime('%A')})
                    text_content = strip_tags(html_content)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.attach_file('Media/doctors/prescription.pdf')
                    msg.send(fail_silently=True)
                    return JsonResponse({'status':'Status updated successfully'})
                if updated_status == 'Refunded':
                    appoint.status = updated_status
                    # appoint.btn_class = 'd-none'
                    appoint.doc_verf = True
                    appoint.doctor_approval_datetime = datetime.now()
                    remark = data.get('remark')
                    if remark is None:
                        return JsonResponse({'status':'Remark is required for rejection'},status=422)
                    appoint.rejection_remark = remark
                    appoint.save()
                    subject, from_email, to = "Request canceled for appointment on Maxcare Health", "max.care13524@gmail.com", appoint.patient.email
                    print(remark)
                    html_content = render_to_string('Rejected_template.html',{'username':appoint.patient.first_name,'doctor_first_name':appoint.doctor.first_name,'doctor_last_name':appoint.doctor.last_name,'date':appoint.prefered_date,'day':appoint.prefered_date.strftime('%A'),'status':updated_status,'person':'Doctor','reason':remark})
                    text_content = strip_tags(html_content)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send(fail_silently=True)
                    return JsonResponse({'status':'Status updated successfully'})
                return JsonResponse({'status':'Invalid update status'},status=422)
            return JsonResponse({'status':"You don't have access to update any thing here"},status=401)
        return JsonResponse({'status':'Unauthorised'},status=401)
    return JsonResponse({"status":"Invalid request method"},status=400)
            
def manage_prescription(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_doctor:
                if request.body:
                    data = json.loads(request.body)
                    appo_id = data.get('id')
                    if not appo_id:
                        return JsonResponse({'status':'Appointment ID is required'},status=422)
                    med_name = data.get('medicineName')
                    if not med_name:
                        return JsonResponse({'status':'Appointment ID is required'},status=422)
                    valid_date = data.get('prescribeDate')
                    if not valid_date:
                        return JsonResponse({'status':'Prescribed date is required'},status=422)
                    frequency = data.get('frequency')
                    if not frequency:
                        return JsonResponse({'status':'Frequency is required'},status=422)
                    prescription = Precription(medicine_name=med_name, valid_date=valid_date, frequency=frequency, appoint_id=appo_id)
                    Appointments.objects.filter(id=appo_id).update(status='Prescribed')
                    prescription.save()
                    return JsonResponse({'status':'Prescription created successfully'})
                return JsonResponse({'status':'Nothing is found in body'},status=401)
            return JsonResponse({'status':'You are not a doctor'}, status=401)
        return JsonResponse({'status':'Unauthorised'}, status=401)
    elif request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_doctor:
                appo_id = request.GET.get('id')
                if not appo_id:
                    return JsonResponse({'status':'Appointment ID is required'},status=400)
                prescription = Precription.objects.filter(appoint__doctor_id=request.user.id,appoint_id=appo_id).values('medicine_name','valid_date','frequency')
                return JsonResponse(list(prescription),safe=False)
            elif request.user.is_patient:
                appo_id = request.GET.get('id')
                if not appo_id:
                    return JsonResponse({'status':'Appointment ID is required'},status=400)
                prescription = Precription.objects.filter(appoint__patient_id=request.user.id,appoint_id=appo_id).values('medicine_name','valid_date','frequency')
                data = Appointments.objects.get(id=appo_id)
                return JsonResponse(list(prescription),safe=False)
            return JsonResponse({'status':'You are not a doctor'}, status=401)
        return JsonResponse({'status':'Unauthorised'}, status=401)

    return JsonResponse({"status":"Invalid request method"},status=400)


def test(request):
    if request.method == 'GET':
        # page_no = request.GET.get('page_number')
        # data = Appointments.objects.filter(status='Pending').values('id','patient__first_name','patient__last_name','doctor__first_name','doctor__last_name','prefered_date','status','symptoms','request_date').order_by('-request_date')
        # paginator = Paginator(data, 25)
        # page_obj = paginator.page(page_no)
        # print(page_obj.object_list, paginator.num_pages)
        # next_page = page_obj.next_page_number() if page_obj.has_next() else None
        # prev_page = page_obj.previous_page_number() if page_obj.has_previous() else None
        # print(prev_page, next_page)
        # return JsonResponse({'previous page':prev_page,'next page':next_page,'total_no_of_pages':paginator.num_pages,'data':list(page_obj.object_list),'no_of_records':len(list(page_obj.object_list))})
        subject = "hello"
        from_email = "max.care13524@gmail.com"
        to = "max.care13524@gmail.com"
        text_content = "This is an important message."
        html_content = "<p>This is an <strong>important</strong> message.</p>"
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return JsonResponse({"status":"mail sent"},status=400)
