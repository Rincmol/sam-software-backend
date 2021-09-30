from rest_framework import serializers
from django.contrib.auth.models import User
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    mobile= serializers.CharField(max_length=12, min_length=10),
    #username = serializers.CharField(max_length=15, min_length=2)
    
    class Meta:
        model = User
        fields = ['username', 'mobile', 'password'
                  ]

    def validate(self, attrs):
        mobile= attrs.get('mobile', '')
        username= attrs.get('username', '')
        password= attrs.get('password', '')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'username': ('username is already in use')})
        if User.objects.filter(mobile=mobile).exists():
            raise serializers.ValidationError(
                {'mobile': ('Mobile is already in use')})
        if User.objects.filter(password=password).exists():
            raise serializers.ValidationError(
                {'password': ('Password is already in use, Choice another one')})
       
        return super().validate(attrs)
        

        

    def create(self, validated_data):
        return User.objects.create(**validated_data)



class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['username', 'password']










