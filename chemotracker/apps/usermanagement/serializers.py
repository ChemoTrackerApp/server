from apps.usermanagement.models import User
from rest_framework import serializers

"""
first_name = models.CharField()
    last_name = models.CharField()
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    dob = models.DateField(null=True)

    # 0 = not known, 1 = male, 2 = female, 9 = not applicable
    sex = models.PositiveSmallIntegerField()
    date_joined = models.DateTimeField(default=timezone.now)
    phone = models.CharField(max_length=20, null=True)
    address = models.TextField()
    password = models.CharField(maxlength=255)

"""
class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    dob = serializers.DateField()
    phone = serializers.CharField(max_length=20)
    sex = serializers.IntegerField()
    address = serializers.TextField()
    password = serializers.CharField(max_length=255)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
            return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password")
        instance.__dict__.update(validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance