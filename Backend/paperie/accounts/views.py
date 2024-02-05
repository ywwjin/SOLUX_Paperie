'''from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer 

#추가
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
		
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
		
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()
        
        # Token 발급을 위한 정보 설정
        token_data = {
            'username': user.username,
            'password': request.data.get('password')
        }
        
        # Token 발급을 위한 API 요청
        token_view = TokenObtainPairView.as_view()
        token_response = token_view(request=request, data=token_data)
        token_response.is_valid(raise_exception=True)
        
        return Response(token_response.data, status=status.HTTP_201_CREATED)
    

@api_view(['POST'])
def logout(request):
    if request.method == 'POST':
        # 액세스 토큰을 헤더에서 가져오기
        access_token = request.headers.get('Authorization')

        if access_token:
            # 액세스 토큰에서 'Bearer ' 부분 제거
            access_token = access_token.replace('Bearer ', '')

        if request.method == 'POST':
            body = json.loads(request.body)
            refresh_token = body.get('refresh')

            if refresh_token:
                # RefreshToken 인스턴스 생성
                refresh_token_object = RefreshToken()
                # refresh_token 문자열을 유효한 토큰 객체로 변환
                refresh_token_object.token = refresh_token

                # 로그아웃 처리
                refresh_token_object.blacklist()
                return Response({"message": "로그아웃 하셨습니다."}, status=status.HTTP_200_OK)

    # POST 요청이 아닌 경우 예외 처리
    return Response({"error": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)'''
import mysql.connector
import json
from django.http import HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import TokenObtainPairSerializer
from .serializers import MyTokenObtainPairSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from .models import Token
from django.contrib.auth.models import User
from django.db import IntegrityError


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')

    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Try to get the existing user
        user = User.objects.get(username=request.data.get('username'))

        return Response({'error': '이미 존재하는 사용자입니다.'}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        # If the user does not exist, create a new user
        user = User.objects.create_user(
            username=request.data.get('username'),
            password=password
        )

        # Return a success response
        return Response({'message': '회원가입이 성공적으로 완료되었습니다.'}, status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    
    # Use TokenObtainPairSerializer directly
    serializer = TokenObtainPairSerializer(data=request.data)
    
    if serializer.is_valid():
        # Serializer is valid, return the token in the response
        token_response = serializer.validated_data
        user_name = request.data.get('username')
        access_token = token_response['access']
        refresh_token = token_response['refresh']

        # Save tokens to MySQL database
        save_tokens_in_mysql(user_name, access_token, refresh_token)

        return Response(token_response, status=status.HTTP_200_OK)
    else:
        # Serializer is not valid, return the errors in the response
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


User = get_user_model()

def save_tokens_in_mysql(user_name, access_token, refresh_token):
    try:
        user = User.objects.get(username=user_name)

        token, created = Token.objects.get_or_create(user_name=user, defaults={'access_token': access_token, 'refresh_token': refresh_token})

        if not created:
            token.access_token = access_token
            token.refresh_token = refresh_token
            token.save()

        return True
    except ObjectDoesNotExist:
        return False  # User with the given username does not exist.
    except IntegrityError as e:
        return False  # IntegrityError occurred, handle it as needed.
    except Token.DoesNotExist:
        return False  # Token.DoesNotExist exception handling if needed.

    

    
@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    user_name = request.data.get('username')

    try:
        # Get the user
        user = get_user_model().objects.get(username=user_name)

        # Delete the tokens associated with the user
        Token.objects.filter(user_name=user_name).delete()

        return Response({'message': '로그아웃이 성공적으로 완료되었습니다.'}, status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        # User with the given username does not exist
        return Response({'error': '존재하지 않는 사용자입니다.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Handle other exceptions if needed
        return Response({'error': f'에러 발생: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)