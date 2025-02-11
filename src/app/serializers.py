from rest_framework import serializers
from django.contrib.auth.models import User
from .models import SWOTAnalysis, SWOTItem


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user
    

class SWOTItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SWOTItem
        fields = ['id', 'category', 'content', 'created_at']

class SWOTAnalysisSerializer(serializers.ModelSerializer):
    items = SWOTItemSerializer(many=True)
    
    class Meta:
        model = SWOTAnalysis
        fields = ['id', 'user', 'title', 'created_at', 'items']
        read_only_fields = ['id', 'created_at', 'user']

    def create(self, validated_data):
        # ネストしたitemsデータを分離
        items_data = validated_data.pop('items');
        analysis = SWOTAnalysis.objects.create(**validated_data)
        for item in items_data:
            SWOTItem.objects.create(analysis=analysis, **item)
        return analysis
