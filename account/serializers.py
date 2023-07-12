from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = User
    #     fields = '__all__'
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=8, write_only=False)
    password_confirmation = serializers.CharField(required=True, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirmation']

    def validate(self, attrs):
        password_confirmation = attrs.pop('password_confirmation')
        if password_confirmation != attrs['password']:
            raise serializers.ValidationError('Passwords don\'t match')

        if not attrs['first_name'][0].istitle() or not attrs['last_name'][0].istitle():
            raise serializers.ValidationError('First or last names should start with')

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        request = self.context.get('request')
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username,
                                password=password,
                                request=request)
            if not user:
                raise serializers.ValidationError('Incorrect username or password')
        else:
            raise serializers.ValidationError('No username or password')
        data['user'] = user
        return data

    def validate_username(self, username):
        print(username)
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username not found')
        return username


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
