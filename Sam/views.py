from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.urls.conf import path
from django.utils import encoding
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from .serializers import UserSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User,Item
from Sam.forms import ItemForm
from django.conf import settings
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
import django.contrib.auth.password_validation as validators
from django.contrib.auth.hashers import check_password

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




