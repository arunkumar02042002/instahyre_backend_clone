from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status


# Local Import
from .serializers import UserLoginSerializer
from common.handlers import validation_error_handler

User = get_user_model()

# Create your views here.
class LoginView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        # Expecting email and password
        request_data = request.data
        serializer = self.serializer_class(data=request_data)

        # If invalid input or missing fields
        if serializer.is_valid() is False:
            return Response({
                "status": "error",
                "message": validation_error_handler(serializer.errors),
                "payload": {
                    "errors": serializer.errors,
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        email = validated_data['email']
        password = validated_data['password']

        user = User.objects.filter(email=email).first()

        # If user not found
        if user is None:
            return Response({
                "status": "error",
                "message": "No user found with this email.",
                "payload": {}
            }, status=status.HTTP_404_BAD_REQUEST)
        
        validated_password = check_password(password, user.password)

        # In password is wrong
        if validated_password is False:
            return Response({
                "status": "error",
                "message": "Invalid Password!",
                "payload": {}
            }, status=status.HTTP_403_FORBIDDEN)

        # If user is not active or deleted
        if user.is_active is False:
            return Response({
                "status": "error",
                "message": "Account not activated yet. Please activate your account first.",
                "payload": {}
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Fetch user details
        serializer_data = self.serializer_class(
            user, context={"request": request}
        )

        # Generate token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            "status":"success",
            "message": "Successfully Loged In!",
            "payload": {
                "token":token.key,
                **serializer_data,
            }
        }, status=status.HTTP_200_OK)