from django.db.models import Subquery
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from django.apps import apps
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from profiles import serializers
from profiles import models
from profiles import permissions
from django.shortcuts import get_object_or_404
from rest_framework.parsers import FileUploadParser
from .models import UserProfile, ProfileAboutItem, ProfileSettings

from django.conf import settings

#from django_filters.rest_framework import DjangoFilterBackend

from friendship.models import Friend, FriendshipRequest
from .serializers import FriendshipRequestSerializer


config = apps.get_app_config('rest_friendship')


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProfileSerializer
    queryset = models.UserProfile.objects.all()
    http_method_names = ['post','get']
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    #filter_class = SettingsFilter
    #filter_backends = (filters.SearchFilter,)
    #search_fields = ('name','email',)


class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

<<<<<<< HEAD
=======
# class CustomObtainAuthToken(ObtainAuthToken):

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['id']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.id,
#             'email': user.email
#         })

>>>>>>> 1ec8d68395c6eb5eb5019654baef117eacc15e7b
class ProfileAboutView(APIView):
    def get(self, request):
        foodie_partner = request.GET.get('foodie_partner', None)
        #location_range = request.GET.get('location_range', None)
        min_age = request.GET.get('min_age', None)
        max_age = request.GET.get('max_age', None)
        gender = request.GET.get('gender', None)

        query = ProfileSettings.objects.filter(
            foodie_partner__iexact=gender, min_age__level__lte=ProfileAboutItem.age, max_age__level_gte=ProfileAboutItem.age)
        serializer = ProfileAboutItemSerializer(query, many=True)
        return Response(serializer.data)
    
    
# class FileUploadView(APIView):
#     parser_class = (FileUploadParser,)

#     def post(self, request, *args, **kwargs):

#       file_serializer = ProfileAboutItemSerializer(data=request.data)

#       if file_serializer.is_valid():
#           file_serializer.save()
#           return Response(status=status.HTTP_201_CREATED)
#       else:
#           return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileAboutItemViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    parser_class = (FileUploadParser,)
    serializer_class = serializers.ProfileAboutItemSerializer
    http_method_names = ['post', 'put', 'get']
    queryset = ProfileAboutItem.objects.all()
    permission_classes = (permissions.UpdateOwnAbout, IsAuthenticated)
    
    
#     # @action(detail=True, methods=['post','put'])
#     # def upload_docs(request,pk=None):
#     #     try:
#     #         file = request.data['file']
#     #     except KeyError:
#     #         raise ParseError('Request has no resource file attached')
#     #     profile_image = ProfileAboutItem.objects.create(image=file)
#     #     return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)

    # def get_queryset(self):
    #     profile_settings = models.ProfileSettings.objects.all()
    #     ps = models.ProfileAboutItem.objects.all()
    #     print(ps)
    #     print(self.request.user.id)
    #     return ps.filter(gender__in=Subquery(profile_settings.values('foodie_partner')),
    #                                            user_settings__min_age__lte=ps.get(
    #                                                id=self.request.user.id).age,
    #                                            user_settings__max_age__gte=ps.get(
    #                                                id=self.request.user.id).age)
        
            
            


class ProfileSettingsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['post', 'put', 'get']
    serializer_class = serializers.ProfileSettingsSerializer
    queryset = models.ProfileSettings.objects.all()
    permission_classes = (permissions.UpdateOwnSettings, IsAuthenticated)

    def get_queryset(self):
        return ProfileSettings.objects.filter(user_profile=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)
        
        
class ImageViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['post', 'put', 'get','delete']
    serializer_class = serializers.ImageSerializer
    queryset = models.Image.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()
        
class BioViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['post', 'put', 'get','delete']
    serializer_class = serializers.BioSerializer
    queryset = models.Bio.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save()
        
        
class FriendViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = config.permission_classes
    serializer_class = config.user_serializer

    def list(self, request):
        friends = Friend.objects.friends(request.user)
        serializer = self.serializer_class(friends, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def requests(self, request):
        friend_requests = Friend.objects.unrejected_requests(user=request.user)
        return Response(FriendshipRequestSerializer(friend_requests, many=True).data)

    @action(detail=False)
    def sent_requests(self, request):
        friend_requests = Friend.objects.sent_requests(user=request.user)
        return Response(FriendshipRequestSerializer(friend_requests, many=True).data)

    @action(detail=False)
    def rejected_requests(self, request):
        friend_requests = Friend.objects.rejected_requests(user=request.user)
        return Response(FriendshipRequestSerializer(friend_requests, many=True).data)

    def create(self, request):
        """
        Creates a friend request
        POST data:
        - user_id
        - message
        """

        friend_obj = Friend.objects.add_friend(
            request.user,                                                     # The sender
            get_object_or_404(get_user_model(),
                              email=request.data['email']),  # The recipient
            message=request.data.get('message', 'Add Me')
        )

        return Response(
            FriendshipRequestSerializer(friend_obj).data,
            status.HTTP_201_CREATED
        )

    def destroy(self, request, pk=None):
        """
        Deletes a friend relationship
        The user id specified in the URL will be removed from the current user's friends
        """

        user_friend = get_object_or_404(get_user_model(), pk=pk)

        if Friend.objects.remove_friend(request.user, user_friend):
            message = 'deleted'
            status_code = status.HTTP_204_NO_CONTENT
        else:
            message = 'not deleted'
            status_code = status.HTTP_304_NOT_MODIFIED

        return Response(
            {"message": message},
            status=status_code
        )


class FriendshipRequestViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = config.permission_classes

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        friendship_request = get_object_or_404(FriendshipRequest,
                                               pk=pk, to_user=request.user)

        friendship_request.accept()
        return Response(
            FriendshipRequestSerializer(friendship_request).data,
            status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        friendship_request = get_object_or_404(
            FriendshipRequest, pk=pk, to_user=request.user)
        friendship_request.reject()
        return Response(
            FriendshipRequestSerializer(friendship_request).data,
            status.HTTP_201_CREATED
        )

# class SettingsFilter(filters.FilterSet):
    #settings = filters.ModelChoiceFilter(queryset=models.ProfileSettings.objects.all())
