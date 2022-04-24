from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.exceptions import APIException

import pymongo
import certifi

# @api_view(['GET'])
# def get_all_users(request):
#     cluster = pymongo.MongoClient(settings.CONNECTION_STRING, tlsCAFile=certifi.where())
#     collection = cluster['instagramlite']['Users']
#     users = list(collection.find({}, {'username': 1, 'password':1, '_id': 0}))
#     print(users)
#     return Response(users)

def get_user_collection():
    cluster = pymongo.MongoClient(settings.CONNECTION_STRING, tlsCAFile=certifi.where())
    collection = cluster['instagramlite']['Users']
    return collection

@api_view(['POST'])
def login_user(request):

    collection = get_user_collection()
    user = collection.find_one({'username': request.POST['username']})

    if not user:
        raise APIException("Incorrect Username")

    if not check_password(request.POST['password'], user['password']):
        raise APIException("Incorrect Password")
    
    user['_id'] = str(user['_id'])
    request.session['user'] = user
    return Response(user, status=200)

@api_view(['GET'])
def logout_user(request):
    request.session['user'] = None
    return Response({}, status=200)

@api_view(['POST'])
def register_user(request):

    if not request.POST['username']:
        raise APIException("No username entered")

    if not request.POST['password']:
        raise APIException("No password entered")

    if not (request.POST['first_name'] and request.POST['last_name']):
        raise APIException("Name not entered correctly")


    Users = get_user_collection()
    existing_user = Users.find_one({'username': request.POST['username']}, {'_id': 0})

    if existing_user:
        raise APIException("Username already exists")

    user_instance = {
        'username': request.POST['username'],
        'password': make_password(request.POST['password']),
        'first_name': request.POST['first_name'],
        'last_name': request.POST['last_name']
    }

    Users.insert_one(user_instance)
    user_instance['_id'] = str(user_instance['_id'])

    return Response(user_instance, status=201)

