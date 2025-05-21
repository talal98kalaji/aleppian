from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate, get_user_model
from .serializers import RegisterSerializer, DataEntrySerializer, get_tokens_for_user
from .permissions import IsSuperUser
from rest_framework.decorators import api_view, permission_classes
User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        user = authenticate(**request.data)
        if not user:
            return Response({'detail': 'incorrect Data'}, status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_tokens_for_user(user)

        return Response({
            'refresh': tokens['refresh'],
            'access': tokens['access'],
            'role': user.role })

class CreateSuperUserView(APIView):
    permission_classes = [IsAuthenticated, IsSuperUser]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_staff = True
            user.is_superuser = True
            user.save()
            return Response({'id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUser]


class CreateDataEntryView(APIView):
    permission_classes = [IsAuthenticated, IsSuperUser]   
    def post(self, request):
        serializer = DataEntrySerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'is_superuser': user.is_superuser,

    })