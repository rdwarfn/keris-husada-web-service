from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

# from django_rest_passwordreset.signals import reset_password_token_created

from manajemen.models import User
from manajemen.api.user.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, JWTAuthentication)
    permission_classes  = (DjangoModelPermissions, IsAuthenticated)
    serializer_class    = UserSerializer
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    search_fields = [
        'username', 
        'email',
        'phone_number',
        'user_type',
    ]

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


def validate_username(request):
    username = request.GET.get('username', None)
    print(request.user)
    response = User.objects.filter(username__iexact=username).exists()
    return JsonResponse({ "is_exist": response })


def validate_email(request):
    email = request.GET.get('email', None)
    print(request.user)
    response = User.objects.filter(email__iexact=email).exists()
    return JsonResponse({ "is_exist": response })










# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
#     """
#     Handles password reset tokens
#     When a token is created, an e-mail needs to be sent to the user
#     :param sender: View Class that sent the signal
#     :param instance: View Instance that sent the signal
#     :param reset_password_token: Token Model Object
#     :param args:
#     :param kwargs:
#     :return:
#     """
#     # send an e-mail to the user
#     context = {
#         'current_user': reset_password_token.user,
#         'username': reset_password_token.user.username,
#         'email': reset_password_token.user.email,
#         'reset_password_url': "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
#     }

#     # render email text
#     email_html_message = render_to_string('email/user_reset_password.html', context)
#     email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

#     msg = EmailMultiAlternatives(
#         # title:
#         "Password Reset for {title}".format(title="Some website title"),
#         # message:
#         email_plaintext_message,
#         # from:
#         "noreply@somehost.local",
#         # to:
#         [reset_password_token.user.email]
#     )
#     msg.attach_alternative(email_html_message, "text/html")
#     msg.send()
