from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.exceptions import APIException

from webapp.models import Users, Albums, Pictures
from webapp.serializers import AlbumsSerializer, PicturesSerializer, UsersSerializer


# api to get and add images to and from the album
# note: for adding image we need to pass the data as a form
@csrf_exempt
@api_view(['POST', 'GET'])
def pictures_add_get(request):
    
    # getting album id is a must
    album = Albums.objects.get(albumId=request.POST['albumId'])

    if request.method == 'POST':
        # creating a picture instance to save into the picture model
        picture_instance = Pictures()
        picture_instance.picture = request.FILES['picture']
        picture_instance.albumId = album
        picture_instance.caption = request.POST['caption']
        picture_instance.fontColor = request.POST['fontColor']
            
        picture_instance.save()
        return Response({}, status=201)

    if request.method == 'GET':
        pictures_arr = Pictures.objects.filter(albumId=album.albumId)

        return Response(list(pictures_arr.values()), status=200)

# api to add and get album
# request is recieved and passed as json
@csrf_exempt
@api_view(['GET', 'POST'])
def album_get_create(request):

    if request.method == 'POST':
        payload = JSONParser().parse(request)

        album_serializer = AlbumsSerializer(data=payload)
        if album_serializer.is_valid():
            album_serializer.save()
            return Response(album_serializer.data, status=201)
        
        raise APIException("Could not save album, try again")

    if request.method == 'GET':
        if not request.session['user_id']:
            raise APIException("Invalid user, please login again")

        albums = Albums.objects.filter(username = request.session['user_id'])
        albums = list(albums.values())

        return Response(albums, status=200)

    raise APIException("Invalid request")

# login validation for user
# can be modified to token method
# currently saves the user in session
@csrf_exempt
@api_view(['POST'])
def login_user(request):

    payload = JSONParser().parse(request)

    if payload['username'] and payload['password']:
        user = Users.objects.filter(username=payload['username']).first()

    else:
        raise APIException("Please enter username and password")

    if not user:
        raise APIException("Incorrect Username")

    # checking if the hashed password matches the entered password
    if not check_password(payload['password'], user.password):
        raise APIException("Incorrect Password")
    
    request.session['user_id'] = user.userId

    return Response({}, status=200)

# logout method to set the session null
@csrf_exempt
@api_view(['GET'])
def logout_user(request):
    request.session['user_id'] = None
    return Response({}, status=200)

# register method to register a new user
# checks if the user already exists
@csrf_exempt
@api_view(['POST'])
def register_user(request):

    payload = {}

    if request.body:
        payload = request
        payload = JSONParser().parse(payload)

        # checks for username and password fields
        if not payload['username']:
            raise APIException("Please enter username") 
        
        if not payload['password']:
            raise APIException("Please enter password") 

        # hashing the password
        payload['password'] = make_password(payload['password'])
    
    else:
        raise APIException("Incorrect request") 
    
    existing_user = Users.objects.filter(username=payload['username']).first()

    if existing_user:
        raise APIException("Username already exists")

    user_serializer = UsersSerializer(data=payload)
    if user_serializer.is_valid():
        user_serializer.save()
        return Response(user_serializer.data, status=201)

    raise APIException("Failed to register user")
