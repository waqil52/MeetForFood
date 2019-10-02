from rest_framework import serializers

class HelloSerializer(serializers.Serializer):
    """Serializes a namefield for testing api"""
    name = serializers.CharField(max_length=20)
    
    
