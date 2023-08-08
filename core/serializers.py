from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer

class UserSeializers(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['email', 'id', 'username', 'first_name', 'last_name']


class UserCreateSerializers(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']