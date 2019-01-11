'''
Created on Mar 13, 2017

@author: jupark
'''
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Product, PRODUCTS

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'first_name', 'last_name', 'groups',)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('pk','name','category')

'''
Generate dynamic serializers for dynamic models
'''
SERIALIZERS = {}
LOCALSERIALIZERS = {}
def fabricSerializer(myModel):
    class MySerializerClass(serializers.ModelSerializer):

        class Meta:
            model = myModel
            fields = '__all__'
    return MySerializerClass

for key, myClass in PRODUCTS.iteritems():
    SERIALIZERS[key] = fabricSerializer(myClass)