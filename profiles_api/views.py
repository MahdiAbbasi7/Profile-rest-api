from rest_framework.views import  APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from profiles_api import models
from profiles_api import serializers
from profiles_api import permission


class HelloAPIView(APIView):
    """ Test API view """
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None ):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django views',
            'Gives you the most contol over you application logic',
            'Is mapped manually to URLs',
        ]
        return Response({'message':'hello', 'an_apiview':an_apiview,})


    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    def put(self, request, pk=None):
        """Handel updating an object """
        return Response({'method':'PUT'})

    def patch(self,request, pk=None):
        """Handel a partial update of an object  """
        return Response({'method':'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object """
        return Response({'method':'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test Hello view set """
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a list of objects """
        a_viewset = [
                "Uses actions(list, create, retrieve,update, partial_update, destroy)",
                "Automaticly maps to URLs using Routers",
                "Provides more functionality with less code",
        ]

        return Response({"method":"Hello","message":a_viewset})

    def create(self, request):
        """create a hello message with name """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                    )
    def retrieve(self, request, pk=None):
        return Response({"message":"GET"})

    def update(self, request, pk=None):
        return Response({"message":"PUT"})

    def update_partial(self, request, pk=None):
        return Response({"message":"PATCH"})

    def destroy(self, request, pk=None):
        return Response({"message":"DELETE"})


class UserProfileViewSet(viewsets.ModelViewSet):
    """ Handel creating and updating user profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permission.UpdateOwnProfile,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginAPIView(ObtainAuthToken):
    """Handel creating user authentication tockens."""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ProfileFeedItemViewSet(viewsets.ModelViewSet):
    """Handels Creating, reading and updating profile feed items."""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permission.UpdateOwnStatus,IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user to the logged in user"""
        serializer.save(user_profile=self.request.user)
