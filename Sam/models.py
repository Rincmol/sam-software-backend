from django.db import models
import datetime
import os

# Create your models here.


def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('Sam/static/uploads/', filename)

class Item(models.Model):
    item_name       =   models.TextField(max_length=100)
    item_desc       =   models.TextField(max_length=500,null=True)
    item_barcode    =   models.TextField(max_length=50)
    item_category   =   models.TextField(max_length=50)
    item_unit_prim  =   models.TextField(max_length=100)
    item_unit_sec   =   models.TextField(max_length=100)
    open_balance    =   models.TextField(max_length=100)
    buying_price    =   models.TextField(max_length=50)
    sell_price      =   models.TextField(max_length=50)
    image1          =   models.ImageField(upload_to=filepath, null=True,blank=True)
    image2          =   models.ImageField(upload_to=filepath, null=True,blank=True)
    image3          =   models.ImageField(upload_to=filepath, null=True,blank=True)
    image4          =   models.ImageField(upload_to=filepath, null=True,blank=True)
    class Meta:  
        db_table = "sam_item" 


        
         
class Customer(models.Model):
    customer_name   =   models.TextField(max_length=100)
    vat_reg_no      =   models.TextField(max_length=100)
    cr_no           =   models.TextField(max_length=100)
    expired_on      =   models.TextField(max_length=100)
    land_phone      =   models.TextField(max_length=100)
    mobile          =   models.TextField(max_length=100)
    contact_person  =   models.TextField(max_length=100)
    contact_mobile  =   models.TextField(max_length=100)
    email           =   models.TextField(max_length=100)
    address         =   models.TextField(max_length=100)
    open_balance    =   models.TextField(max_length=100)
    credit_lim_am   =   models.TextField(max_length=100)
    credit_lim_dur  =   models.TextField(max_length=100)

class Supplier(models.Model):
    customer_name   =   models.TextField(max_length=100)
    vat_reg_no      =   models.TextField(max_length=100)
    cr_no           =   models.TextField(max_length=100)
    expired_on      =   models.TextField(max_length=100)
    land_phone      =   models.TextField(max_length=100)
    mobile          =   models.TextField(max_length=100)
    contact_person  =   models.TextField(max_length=100)
    contact_mobile  =   models.TextField(max_length=100)
    email           =   models.TextField(max_length=100)
    address         =   models.TextField(max_length=100)
    open_balance    =   models.TextField(max_length=100)
    credit_lim_am   =   models.TextField(max_length=100)
    credit_lim_dur  =   models.TextField(max_length=100)
    bank_acc_name   =   models.TextField(max_length=100)
    bank_acc_no     =   models.TextField(max_length=100)



class User(models.Model):
    mobile   =   models.CharField(max_length=12, unique=True)
    username    =   models.CharField(max_length=15)
    password    =   models.CharField(max_length=15)


    class Login(models.Model):
        username    =   models.CharField(max_length=15)
        password    =   models.CharField(max_length=15)

    class Job(models.Model):
        job_name    =   models.TextField(max_length=100)
        job_desc    =   models.TextField(max_length=500,null=True)
        imag1       =   models.ImageField(upload_to=filepath, null=True,blank=True)
        imag2       =   models.ImageField(upload_to=filepath, null=True,blank=True)
        imag3       =   models.ImageField(upload_to=filepath, null=True,blank=True)
        imag4       =   models.ImageField(upload_to=filepath, null=True,blank=True)

    class Employee(models.Model):
        emp_name     =    models.TextField(max_length=100)
        nationality  =    models.TextField(max_length=100)
        birth_date   =    models.TextField(max_length=100)
        joining_date =    models.TextField(max_length=100)
        designation  =    models.TextField(max_length=100)
        department   =    models.TextField(max_length=100)
        salary_categ =    models.TextField(max_length=100)
        passport_no  =    models.TextField(max_length=100)
        expir        =    models.TextField(max_length=100)
        id_no        =    models.TextField(max_length=100)
        id_expir     =    models.TextField(max_length=100)
        img1         =   models.ImageField(upload_to=filepath, null=True,blank=True)
        img2         =   models.ImageField(upload_to=filepath, null=True,blank=True)
        img3         =   models.ImageField(upload_to=filepath, null=True,blank=True)
        img4         =   models.ImageField(upload_to=filepath, null=True,blank=True)
        basic        =    models.TextField(max_length=100)
        housing      =    models.TextField(max_length=100)
        transportation =    models.TextField(max_length=100)
        food         =    models.TextField(max_length=100)
        mobile       =    models.TextField(max_length=100)
        other        =    models.TextField(max_length=100)
        netpay       =    models.TextField(max_length=100)


    class Group(models.Model):
        group_name    =    models.TextField(max_length=100)
        category      =    models.TextField(max_length=100)


    class Ledger(models.Model):
        ledger_name    =    models.TextField(max_length=100)
        group_name     =    models.TextField(max_length=100)
        category       =    models.TextField(max_length=100)
        opening_bal    =    models.TextField(max_length=100)
        




    
