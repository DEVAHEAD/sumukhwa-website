from django.shortcuts import render
# views.py 랑 serializers.py 작성하고 settings 수정하기
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *
from rest_framework.status import *
from rest_framework import views
from rest_framework.response import Response
import jwt
import datetime
from django.http import HttpResponseRedirect
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from .models import *


class SignUpView(views.APIView):
    serializer_class = UserSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            username=serializer.data['username']
            request.session['username']=username
            return HttpResponseRedirect('../../sumukhwa/projectList')
            #Response({'message': '회원가입 성공', 'data': serializer.data}, status=HTTP_201_CREATED)
        else:
            print("!!!!!!!!!!!!!!!!!f the sign up",serializer.data)
        return render(request,'register.html',context={'message': '회원가입 실패', 'data': serializer.errors})
        #return Response({'message': '회원가입 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data['username']
            request.session['username']=username
            print('LoginView\n!!!!!!!!!!!!!!!!!',username)
            return HttpResponseRedirect('../../sumukhwa/projectList')
        else:
            print("!!!!!!!!!!!!!f the login:",serializer.data)
        return render(request,'login.html',context={'message': "로그인 실패", 'data': serializer.errors})
        #return Response({'message': "로그인 실패", 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)
