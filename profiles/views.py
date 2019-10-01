from rest_framework.views import APIView
from rest_framework.response import Response

class HellooApiView(APIView):
    """Testing API View"""
    def get(self, request, format=None):
        an_apiview= [

        ]
        return Response({'message':'Hello!!!','an_apiview':an_apiview})


