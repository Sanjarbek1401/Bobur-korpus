from rest_framework import serializers
from .models import AuthorInfo,Baburnoma,DivanCategory,DivanGroup,DivanLittleGroup,DivanText,AdminContact


class AuthorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorInfo
        fields = '__all__'

class BaburnomaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Baburnoma
        fields = '__all__'

class DivanTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = DivanText
        fields = '__all__'


class DivanLittleGroupSerializer(serializers.ModelSerializer):
    texts = DivanTextSerializer(many=True,read_only=True)
    class Meta:
        model = DivanLittleGroup
        fields = ['id', 'name','group','texts']

class DivanGroupSerializer(serializers.ModelSerializer):
    little_groups = DivanLittleGroupSerializer(many=True,read_only=True)

    class Meta:
        model = DivanGroup
        fields = ['id','name','category','little_groups']

class DivanCategorySerializer(serializers.ModelSerializer):
    groups = DivanGroupSerializer(many=True,read_only=True)

    class Meta:
        model = DivanCategory
        fields = ['id','name','groups']

class AdminContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminContact
        fields = '__all__'

