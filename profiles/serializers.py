from rest_framework import serializers

from profiles import models

class HelloSerializer(serializers.Serializer):
    """Serializes a namefield for testing api"""
    name = serializers.CharField(max_length=20)
    
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('id','name','email','password')
        extra_kwargs = {
            'password':{
                'write_only': True,
                'style':{'input_type': 'password'}   
            }
        }


    def create(self,validated_data):
        user = models.UserProfile.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password']


        )
        return user

