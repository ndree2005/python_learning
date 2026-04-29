from rest_framework import serializers
from pos_app.models import ( TableResto, User, StatusModel, Category, MenuResto)
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class RegisterUserSerializers(serializers.ModelSerializer):

    email = serializers.EmailField(required = True, 
            validators =[UniqueValidator(queryset= User.objects.all())] )
    password1 = serializers.CharField(write_only = True, 
            required = True, validators = [validate_password] )
    password2 = serializers.CharField(write_only = True, 
            required = True )
    
    class Meta:
        model = User
        fields  = [ 'username', 'email', 'password1', 'password2',
                    'is_active', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name' : {'required' : True},
            'last_name'  : {'required' : True}
        }

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({
                'password' : 'kata sandi tidak sama mohon ulang pengisian password jika tidak akun anda akan di banned permanen dan di jadikan promosi iklan judol untuk kepentingan pemerintah....'            
            })
        return attrs

    def create(self, validate_data):
        user = User.objects.create(
            username = validate_data['username'],
            email = validate_data['email'],
            is_active = validate_data['is_active'],
            first_name = validate_data['first_name'],
            last_name = validate_data['last_name']
        )
        user.set_password(validate_data['password1'])
        user.save()
        return user

class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if username and password:
            user = authenticate(username = username, password = password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    msg = 'status pengguna tidaak aktif..'
                    raise ValidationError({'message' : msg})
            else:
                msg = 'anda tidak dapat login dengan username dan password yang benar..'
                raise ValidationError({'message' : msg})
        else:
            msg = 'mohon isi username dan password untuk login..'
            raise ValidationError({'message' : msg})
        return data
        

class TableRestoSerializers(serializers.ModelSerializer):
    class Meta:
        model = TableResto
        fields = ('id', 'code', 'name', 'capacity', 'table_status', 'status',)


class MenuRestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuResto
        fields = ('id', 'code', 'name', 'price', 'description', 'image_menu', 'category', 'menu_status', 'status', 'user_create', 'user_update', 'created_on', 'last_modified')

