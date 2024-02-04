from rest_framework import status
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
    return Response({"error": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)