from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions
from .models import SWOTAnalysis

# Serializerの読み込み
from .serializers import SWOTAnalysisSerializer
from .serializers import UserRegistrationSerializer


@ensure_csrf_cookie
def csrf_token_view(request):
    """
    このエンドポイントにアクセスすると、ブラウザに CSRF クッキーがセットされます。
    """
    return JsonResponse({'detail': 'CSRF cookie has been set'})


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })


class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'ユーザ登録が成功しました'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request, format=None):

        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            # セッション認証の場合は login() を呼ぶ
            login(request, user)
            # またはトークン認証の場合はトークン発行処理を行います
            return Response({'message': 'ログイン成功'}, status=status.HTTP_200_OK)
        return Response({'error': '認証に失敗しました'}, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    def post(self, request, format=None):
        logout(request)  # セッションを破棄する
        return Response({'message': 'ログアウトしました'}, status=status.HTTP_200_OK)
    
class SWOTAnalysisViewSet(viewsets.ModelViewSet):
    serializer_class = SWOTAnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        print("get_queryset: current_user", current_user)
        # 現在のユーザーが作成したSWOT分析のみを返す
        return SWOTAnalysis.objects.filter(user=current_user)

    def perform_create(self, serializer):
        # 現在のユーザーを分析に紐づける
        serializer.save(user=self.request.user)