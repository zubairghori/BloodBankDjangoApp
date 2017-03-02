from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model


class UserSerilizer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            no=validated_data['no'],
            userType=validated_data['userType'],
            age = validated_data['age'],
            password = validated_data['password'],
            bgType = validated_data['bgType'],
            rhValue = validated_data['rhValue']
        )
        # user.set_password(validated_data['password'])
        user.save()
        return user


    class Meta:
        model = User
        fields = '__all__'


# class BloodGroupSerilizer(serializers.ModelSerializer):
#     # user = serializers.RelatedField(many=True,read_only=True)
#     # user = serializers.RelatedField(source='user', read_only=True)
#
#     def create(self, validated_data):
#         bg = BloodGroup.objects.create(
#             bgType=validated_data['bgType'],
#             rhValue=validated_data['rhValue'],
#         )
#         # user.set_password(validated_data['password'])
#         bg.save()
#         return bg
#
#
#     class Meta:
#         model = BloodGroup
#         fields = '__all__'





