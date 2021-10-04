from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.urls.conf import path
from django.utils import encoding
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from .serializers import UserSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Employee, Group, Job, Ledger, Supplier, User,Item
from Sam.forms import ItemForm
from django.conf import settings
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
import django.contrib.auth.password_validation as validators
from django.contrib.auth.hashers import check_password
import os
from django.contrib import messages

# Create your views here.


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self,request):
        username = request.data['username']
        password = request.data['password']
       
        
        user = User.objects.filter(username=username).first()
        user1 = User.objects.filter(password=password).first()
        #user2 = User.objects.filter(username='admin', password='Admin@1234').first()
        
        if (username == 'admin' and password == 'Admin@1234') :
            return HttpResponse('Admin Login Successfully')
        
        else :
            if user is None :
                raise AuthenticationFailed('User not found!')

        
            if not user1:
                raise AuthenticationFailed('Incorrect password!')
        
            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }
            return HttpResponse('User Login Successfully')
            token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')


            response = Response()

            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
             'jwt': token
             }
            return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

# CRUD Operations

# Item 

def items(request):
    if request.method == "POST":
        itm = Item()
        itm.item_name = request.POST.get('item_name')
        itm.item_desc = request.POST.get('item_desc')
        itm.item_barcode = request.POST.get('item_barcode')
        itm.item_category = request.POST.get('item_category')
        itm.item_unit_prim = request.POST.get('item_unit_prim')
        itm.item_unit_sec = request.POST.get('item_unit_sec')
        itm.open_balance = request.POST.get('open_balance')
        itm.buying_price = request.POST.get('buying_price')
        itm.sell_price = request.POST.get('sell_price')
        
        if len(request.FILES) != 0:
            itm.image1 = request.FILES['image1']
            itm.image2 = request.FILES['image2']
            itm.image3 = request.FILES['image3']
            itm.image4 = request.FILES['image4']
        itm.save()
        return redirect('/itemshow')            
    return render(request,'item.html')


def itemshow(request):
    itemz = Item.objects.all()
    context = {'itemz':itemz}
    return render(request,'itemshow.html',context)


def ItemEdit(request,id):
    itm = Item.objects.get(id=id)   
    if request.method == 'POST':
        if len(request.FILES)!= 0:
            if len(itm.image1 and itm.image2 and itm.image3 and itm.image3) > 0 :
                os.remove(itm.image1.path or itm.image2.path or itm.image3.path or itm.image4.path)  
            itm.image1 = request.FILES['image1']
            itm.image2 = request.FILES['image2']
            itm.image3 = request.FILES['image3']
            itm.image4 = request.FILES['image4']
        itm.item_name = request.POST.get('item_name')
        itm.item_desc = request.POST.get('item_desc')
        itm.item_barcode = request.POST.get('item_barcode')
        itm.item_category = request.POST.get('item_category')
        itm.item_unit_prim = request.POST.get('item_unit_prim')
        itm.item_unit_sec = request.POST.get('item_unit_sec')
        itm.open_balance = request.POST.get('open_balance')
        itm.buying_price = request.POST.get('buying_price')
        itm.sell_price = request.POST.get('sell_price')
        itm.save()
        messages.success(request,"Item updated succesfully")
        return redirect('/itemshow')
    context = {'itm':itm}
    return render(request,'itemedit.html',context)

def ItemDelete(request, id):  
    itm = Item.objects.get(id=id)  
    itm.delete()  
    return redirect("/itemshow")  
    # context = {'itm':itm}
    # return render(request,'itemedit.html',context)

# Customer

def CustomerAdd(request):
    if request.method == "POST":
        cus = Customer()
        cus.customer_name = request.POST.get('customer_name')
        cus.vat_reg_no = request.POST.get('vat_reg_no')
        cus.cr_no = request.POST.get('cr_no')
        cus.expired_on = request.POST.get('expired_on')
        cus.land_phone = request.POST.get('land_phone')
        cus.mobile = request.POST.get('mobile')
        cus.contact_person = request.POST.get('contact_person')
        cus.contact_mobile = request.POST.get('contact_mobile')
        cus.email = request.POST.get('email')
        cus.address = request.POST.get('address')
        cus.open_balance = request.POST.get('open_balance')
        cus.credit_lim_am = request.POST.get('credit_lim_am')
        cus.credit_lim_dur = request.POST.get('credit_lim_dur')

        cus.save()
        return redirect("/customerview")  
    return render(request,'customer.html')


def CustomerView(request):
    cus = Customer.objects.all() 
    context = {'cus':cus}
    return render(request,'customerview.html',context)

def customerEdit(request,id):
    cus = Customer.objects.get(id=id)  
    if request.method == 'POST':
        cus.customer_name = request.POST.get('customer_name')
        cus.vat_reg_no = request.POST.get('vat_reg_no')
        cus.cr_no = request.POST.get('cr_no')
        cus.expired_on = request.POST.get('expired_on')
        cus.land_phone = request.POST.get('land_phone')
        cus.mobile = request.POST.get('mobile')
        cus.contact_person = request.POST.get('contact_person')
        cus.contact_mobile = request.POST.get('contact_mobile')
        cus.email = request.POST.get('email')
        cus.address = request.POST.get('address')
        cus.open_balance = request.POST.get('open_balance')
        cus.credit_lim_am = request.POST.get('credit_lim_am')
        cus.credit_lim_dur = request.POST.get('credit_lim_dur')
        cus.save()
        messages.success(request,"customer updated succesfully")
        return redirect('/customerview')
    context = {'cus':cus}
    return render(request,'customeredit.html',context)

def customerDelete(request, id):  
    cus = Customer.objects.get(id=id)  
    cus.delete()  
    return redirect("/customerview")  
    # context = {'cus':cus}
    # return render(request,'customeredit.html',context)

# Supplier

def SupplierAdd(request):
    if request.method == "POST":
        sup = Supplier()
        sup.customer_name = request.POST.get('customer_name')
        sup.vat_reg_no = request.POST.get('vat_reg_no')
        sup.cr_no = request.POST.get('cr_no')
        sup.expired_on = request.POST.get('expired_on')
        sup.land_phone = request.POST.get('land_phone')
        sup.mobile = request.POST.get('mobile')
        sup.contact_person = request.POST.get('contact_person')
        sup.contact_mobile = request.POST.get('contact_mobile')
        sup.email = request.POST.get('email')
        sup.address = request.POST.get('address')
        sup.open_balance = request.POST.get('open_balance')
        sup.credit_lim_am = request.POST.get('credit_lim_am')
        sup.credit_lim_dur = request.POST.get('credit_lim_dur')
        sup.bank_acc_name = request.POST.get('bank_acc_name')
        sup.bank_acc_no = request.POST.get('bank_acc_no')

        sup.save()
        return redirect("/suppliershow")  
    return render(request,'supplier.html')

def suppliershow(request):
    sup = Supplier.objects.all()
    context = {'sup':sup}
    return render(request,'suppliershow.html',context)


def supplierEdit(request,id):
    sup = Supplier.objects.get(id=id)  
    if request.method == 'POST':
        sup.customer_name = request.POST.get('customer_name')
        sup.vat_reg_no = request.POST.get('vat_reg_no')
        sup.cr_no = request.POST.get('cr_no')
        sup.expired_on = request.POST.get('expired_on')
        sup.land_phone = request.POST.get('land_phone')
        sup.mobile = request.POST.get('mobile')
        sup.contact_person = request.POST.get('contact_person')
        sup.contact_mobile = request.POST.get('contact_mobile')
        sup.email = request.POST.get('email')
        sup.address = request.POST.get('address')
        sup.open_balance = request.POST.get('open_balance')
        sup.credit_lim_am = request.POST.get('credit_lim_am')
        sup.credit_lim_dur = request.POST.get('credit_lim_dur')
        sup.bank_acc_name = request.POST.get('bank_acc_name')
        sup.bank_acc_no = request.POST.get('bank_acc_no')
        sup.save()
        messages.success(request,"supplier updated succesfully")
        return redirect('/suppliershow')
    context = {'sup':sup}
    return render(request,'supplieredit.html',context)

def supplierDelete(request, id):  
    sup = Supplier.objects.get(id=id)  
    sup.delete()  
    return redirect("/suppliershow")  
    # context = {'sup':sup}
    # return render(request,'supplieredit.html',context)

# Job 

def jobadd(request):
    if request.method == "POST":
        jb = Job()
        jb.job_name = request.POST.get('job_name')
        jb.job_desc = request.POST.get('job_desc')
        if len(request.FILES) != 0:
            jb.imag1 = request.FILES['imag1']
            jb.imag2 = request.FILES['imag2']
            jb.imag3 = request.FILES['imag3']
            jb.imag4 = request.FILES['imag4']
        jb.save()
        return redirect('/jobshow')            
    return render(request,'job.html')


def jobshow(request):
    jobz = Job.objects.all()
    context = {'jobz':jobz}
    return render(request,'jobshow.html',context)


def JobEdit(request,id):
    jb = Job.objects.get(id=id)  
    if request.method == 'POST':
        if len(request.FILES)!= 0:
            if len(jb.imag1 and jb.imag2 and jb.imag3 and jb.imag3) > 0 :
                os.remove(jb.imag1.path and jb.imag2.path and jb.imag3.path and jb.imag4.path)
            jb.imag1 = request.FILES['imag1']
            jb.imag2 = request.FILES['imag2']
            jb.imag3 = request.FILES['imag3']
            jb.imag4 = request.FILES['imag4']
        jb.job_name = request.POST.get('job_name')
        jb.job_desc = request.POST.get('job_desc')
        jb.save()
        messages.success(request,"Job updated succesfully")
        return redirect('/jobshow')
    context = {'jb':jb}
    return render(request,'jobedit.html',context)


#Group

def group(request):
    if request.method == "POST":
        gp = Group()
        gp.group_name = request.POST.get('group_name')
        gp.category = request.POST.get('category')
        gp.save()
        return redirect('/groupshow')            
    return render(request,'group.html')

def groupshow(request):
    gp = Group.objects.all()
    context = {'gp':gp}
    return render(request,'groupshow.html',context)


def groupEdit(request,id):
    gp = Group.objects.get(id=id)  
    if request.method == 'POST':
        gp.group_name = request.POST.get('group_name')
        gp.category = request.POST.get('category')
        gp.save()
        messages.success(request,"Group updated succesfully")
        return redirect('/groupshow')
    context = {'gp':gp}
    return render(request,'groupedit.html',context)

def groupDelete(request, id):  
    gp = Group.objects.get(id=id)  
    gp.delete()  
    return redirect("/groupshow")  
    # context = {'itm':itm}
    # return render(request,'itemedit.html',context)


# Ledger

def ledger(request):
    if request.method == "POST":
        lg = Ledger()
        lg.ledger_name = request.POST.get('ledger_name')
        lg.group_name = request.POST.get('group_name')
        lg.category = request.POST.get('category')
        lg.opening_bal = request.POST.get('opening_bal')
        lg.save()
        return redirect('/ledgershow')            
    return render(request,'ledger.html')

def ledgershow(request):
    lg = Ledger.objects.all()
    context = {'lg':lg}
    return render(request,'ledgershow.html',context)


def ledgerEdit(request,id):
    lg = Ledger.objects.get(id=id)  
    if request.method == 'POST':
       lg.ledger_name = request.POST.get('ledger_name')
       lg.group_name = request.POST.get('group_name')
       lg.category = request.POST.get('category')
       lg.opening_bal = request.POST.get('opening_bal')
       lg.save()
       messages.success(request,"ledger updated succesfully")
       return redirect('/ledgershow')
    context = {'lg':lg}
    return render(request,'ledgeredit.html',context)

def ledgerDelete(request, id):  
    lg = Ledger.objects.get(id=id)  
    lg.delete()  
    return redirect("/ledgershow")  
    # context = {'itm':itm}
    # return render(request,'itemedit.html',context)

# Employee

def EmployeeAdd(request):
    if request.method == "POST":
        emp = Employee()
        emp.emp_name = request.POST.get('emp_name')
        emp.nationality = request.POST.get('nationality')
        emp.birth_date = request.POST.get('birth_date')
        emp.joining_date = request.POST.get('joining_date')
        emp.designation = request.POST.get('designation')
        emp.department = request.POST.get('department')
        emp.salary_categ = request.POST.get('salary_categ')
        emp.passport_no = request.POST.get('passport_no')
        emp.expir = request.POST.get('expir')
        emp.id_no = request.POST.get('id_no')
        emp.id_expir = request.POST.get('id_expir')
        emp.basic = request.POST.get('basic')
        emp.housing = request.POST.get('housing')
        emp.transportation = request.POST.get('transportation')
        emp.food = request.POST.get('food')
        emp.mobile = request.POST.get('mobile')
        emp.other = request.POST.get('other')
        emp.netpay = request.POST.get('netpay')

        
        if len(request.FILES) != 0:
            emp.img1 = request.FILES['img1']
            emp.img2 = request.FILES['img2']
            emp.img3 = request.FILES['img3']
            emp.img4 = request.FILES['img4']
        emp.save()
        return redirect('/employeeshow')            
    return render(request,'employee.html')


def employeeshow(request):
    employeez = Employee.objects.all()
    context = {'employeez':employeez}
    return render(request,'employeeshow.html',context)


def employeeEdit(request,id):
    emp = Employee.objects.get(id=id)   
    if request.method == 'POST':
        if len(request.FILES)!= 0:
            if len(emp.img1 and emp.img2 and emp.img3 and emp.img3) > 0 :
                os.remove(emp.img1.path or emp.img2.path or emp.img3.path or emp.img4.path)  
            emp.img1 = request.FILES['img1']
            emp.img2 = request.FILES['img2']
            emp.img3 = request.FILES['img3']
            emp.img4 = request.FILES['img4']
        emp.emp_name = request.POST.get('emp_name')
        emp.nationality = request.POST.get('nationality')
        emp.birth_date = request.POST.get('birth_date')
        emp.joining_date = request.POST.get('joining_date')
        emp.designation = request.POST.get('designation')
        emp.department = request.POST.get('department')
        emp.salary_categ = request.POST.get('salary_categ')
        emp.passport_no = request.POST.get('passport_no')
        emp.expir = request.POST.get('expir')
        emp.id_no = request.POST.get('id_no')
        emp.id_expir = request.POST.get('id_expir')
        emp.basic = request.POST.get('basic')
        emp.housing = request.POST.get('housing')
        emp.transportation = request.POST.get('transportation')
        emp.food = request.POST.get('food')
        emp.mobile = request.POST.get('mobile')
        emp.other = request.POST.get('other')
        emp.netpay = request.POST.get('netpay')
        emp.save()
        messages.success(request,"employee updated succesfully")
        return redirect('/employeeshow')
    context = {'emp':emp}
    return render(request,'employeedit.html',context)

def employeeDelete(request, id):  
    emp = Employee.objects.get(id=id)  
    emp.delete()  
    return redirect("/employeeshow")  
    # context = {'emp':emp}
    # return render(request,'employeedit.html',context)