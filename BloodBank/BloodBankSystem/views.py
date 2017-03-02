from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.permissions import is_authenticated,AllowAny
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .Serilizers import UserSerilizer
from rest_framework.views import APIView,Response
from .models import User
from rest_framework.authtoken.models import Token
from django.db.models import Q

class UserData(APIView):
    # def get(self,request):
    #     try:
    #         id = request.GET['id']
    #     except:
    #         return Response({'data':'','message':'Failed','error':'Invalid Parameter'})
    #     else:
    #         user = User.objects.all().filter(id=id).first()
    #         if user is None:
    #            return Response({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'})
    #         else:
    #             if user.userType == False:
    #                 filtered = filteredBloodGroupForRecipient(user.bgType)
    #                 return Response({'data': {'user': UserSerilizer(user).data, 'donars': filtered.data}, 'message': 'Sucessfully Login', 'error': ''})
    #             filtered = filteredBloodGroupForDonar(user.bgType)
    #             return Response({'data': {'user': UserSerilizer(user).data, 'recipients': filtered.data},'message': 'Sucessfully Login', 'error': ''})

    def post(self,request):
        try:
            id = request.GET['id']
        except:
            return Response({'data':'','message':'Failed','error':'Invalid Parameter'})
        else:
            user = User.objects.all().filter(id=id).first()
            if user is None:
               return Response({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'})
            else:
                try:
                    userType = request.data['userType']
                    age = request.data['age']
                    bgType = request.data['bgType']
                except:
                    return Response({'data': '', 'message': 'Failed', 'error': 'Invalid body parameters'})
                else:
                    if userType is not None and age is not None and bgType is not None:
                        data = UserSerilizer(User.objects.all().filter(userType=userType,age=age,bgType=bgType), many=True).data
                        if userType == 'False':
                            return Response({'data': {'user': UserSerilizer(user).data, 'donars': data},
                                             'message': 'Sucessfully ', 'error': ''})
                        return Response({'data': {'user': UserSerilizer(user).data, 'recipients': data},
                                         'message': 'Sucessfully ', 'error': ''})

    def delete(self,request):
        try:
            id = request.GET['id']
        except:
            return Response({'data': '', 'message': 'Failed', 'error': 'Invalid Parameter'})
        else:
            user = User.objects.all().filter(id=id)
            if user.first() is None:
                return Response({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'})
            else:
                user.delete()
                return Response({'data': '','message': 'User with '+id+' Sucessfully Deleted', 'error': ''})

    def put(self,request):
        object = UserSerilizer(data=request.data)
        if object.is_valid():
            id = request.GET['id']
            if len(User.objects.all().filter(id=id)) == 0:
                return Response({'data':'', 'message': 'User with id '+id+ 'not available', 'error': ''})
            user = User.objects.all().filter(id=id).first()
            user.name = request.data['name']
            user.email = request.data['email']
            user.no = request.data['no']
            user.userType = request.data['userType']
            user.age = request.data['age']
            user.password = request.data['password']
            user.bgType = request.data['bgType']
            user.rhValue = request.data['rhValue']
            user.save()
            return Response({'data': '', 'message': 'Edit Sucessfully', 'error': ''})
        return Response({'data': '', 'message': 'Failed', 'error': 'Invalid Data/Parameters'})



class getAllUsers(APIView):
    def get(self,request):
        try:
            id = request.GET['id']
        except:
            return Response({'data': '', 'message': 'Failed', 'error': 'Invalid Parameter'})
        else:
            user = User.objects.all().filter(id=id).first()
            if user is None:
                return Response({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'})
            else:
                filtered = User.objects.all().filter(~Q(id=id))
                return Response({'data': {'user': UserSerilizer(user).data, 'All': UserSerilizer(filtered,many=True).data},'message': 'Sucessfull', 'error': ''})


class getAlldonars(APIView):
    def get(self,request):
        try:
            id = request.GET['id']
        except:
            return Response({'data': '', 'message': 'Failed', 'error': 'Invalid Parameter'})
        else:
            user = User.objects.all().filter(id=id).first()
            if user is None:
                return Response({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'})
            else:
                filtered = User.objects.all().filter(userType=False)
                return Response({'data': {'user': UserSerilizer(user).data, 'donars': UserSerilizer(filtered,many=True).data},'message': 'Sucessfull', 'error': ''})

class getAllRecipients(APIView):
    def get(self,request):
        try:
            id = request.GET['id']
        except:
            return Response({'data': '', 'message': 'Failed', 'error': 'Invalid Parameter'})
        else:
            user = User.objects.all().filter(id=id).first()
            if user is None:
                return Response({'data': '', 'message': 'Failed', 'error': 'Invalid User ID'})
            else:
                filtered = User.objects.all().filter(userType=True)
                return Response({'data': {'user': UserSerilizer(user).data, 'Recipients': UserSerilizer(filtered,many=True).data},'message': 'Sucessfull', 'error': ''})


class Signup(APIView):

    # Signup
    def post(self, request):
        object = UserSerilizer(data=request.data)
        if object.is_valid():
            email = request.data['email']
            if len(User.objects.all().filter(email=email)) == 0:
                object.save()
                return Response({'data': object.data, 'message': 'Sucessfully Registered', 'error': ''})
            return Response({'data': '', 'message': 'Failed', 'error': 'User with ' + email + ' Already registered'})
        return Response({'data': '', 'message': 'Failed', 'error': 'Invalid Data/Parameters'})

    # Login

class Login(APIView):

    # Login
    def post(self, request,):
        try:
            email = request.data['email']
            password = request.data['password']
        except:
            return Response({'data': '', 'message': 'Failed', 'error': 'Invalid Parameters'})
        else:
            user = User.objects.all().filter(email=email,password=password)
            if len(user) != 0:
                user = user.first()
                if user.userType == False:
                    filtered = filteredBloodGroupForRecipient(user.bgType,user.rhValue)
                    return Response({'data': {'user':UserSerilizer(user).data, 'recipients':filtered.data}, 'message': 'Sucessfully Login', 'error': ''})
                filtered = filteredBloodGroupForDonar(user.bgType,user.rhValue)
                return Response({'data': {'user': UserSerilizer(user).data, 'donars': filtered.data},'message': 'Sucessfully Login', 'error': ''})

            return Response({'data': '', 'message': 'Failed', 'error': 'Invalid email/Password'})





# userType == False is Donar and other is Recipient

def filteredBloodGroupForRecipient(bgType,rhValue=False):
    print(bgType)
    if rhValue == False:
        if bgType.lower() == 'a':
           return  UserSerilizer(User.objects.all().filter(Q(userType=True, bgType='C') | Q(userType=True, bgType='A')),many=True)
        elif bgType.lower() == 'b':
            return UserSerilizer(User.objects.all().filter(Q(userType=True, bgType='C') | Q(userType=True, bgType='B')),many=True)
        elif bgType.lower() == 'c':
            return UserSerilizer(User.objects.all().filter(userType=True, bgType='C'),many=True)
        elif bgType.lower() == 'ab':
            return UserSerilizer(User.objects.all().filter(userType=True),many=True)
        else:
            return "Error"
    else:
        if bgType.lower() == 'a':
            return UserSerilizer(User.objects.all().filter(Q(userType=True, bgType='C') | Q(userType=True, bgType='A')).filter(rhValue=True),
                                 many=True)
        elif bgType.lower() == 'b':
            return UserSerilizer(User.objects.all().filter(Q(userType=True, bgType='C') | Q(userType=True, bgType='B')).filter(rhValue=True),
                                 many=True)
        elif bgType.lower() == 'c':
            return UserSerilizer(User.objects.all().filter(userType=True, bgType='C').filter(rhValue=True), many=True)
        elif bgType.lower() == 'ab':
            return UserSerilizer(User.objects.all().filter(userType=True).filter(rhValue=True), many=True)
        else:
            return "Error"


def filteredBloodGroupForDonar(bgType,rhValue=False):
    print(bgType)
    if rhValue == False:
        if bgType.lower() == 'a':
           return  UserSerilizer(User.objects.all().filter(Q(userType=False, bgType='AB') | Q(userType=False, bgType='A')).filter(rhValue=False),many=True)
        elif bgType.lower() == 'b':
            return UserSerilizer(User.objects.all().filter(Q(userType=False, bgType='B') | Q(userType=False, bgType='AB')).filter(rhValue=False),many=True)
        elif bgType.lower() == 'c':
            return UserSerilizer(User.objects.all().filter(userType=False).filter(rhValue=False),many=True)
        elif bgType.lower() == 'ab':
            return UserSerilizer(User.objects.all().filter(userType=False,bgType='AB').filter(rhValue=False),many=True)
        else:
            return "Error"
    else:
        if bgType.lower() == 'a':
           return  UserSerilizer(User.objects.all().filter(Q(userType=False, bgType='AB') | Q(userType=False, bgType='A')),many=True)
        elif bgType.lower() == 'b':
            return UserSerilizer(User.objects.all().filter(Q(userType=False, bgType='B') | Q(userType=False, bgType='AB')),many=True)
        elif bgType.lower() == 'c':
            return UserSerilizer(User.objects.all().filter(userType=False),many=True)
        elif bgType.lower() == 'ab':
            return UserSerilizer(User.objects.all().filter(userType=False,bgType='AB'),many=True)
        else:
            return "Error"