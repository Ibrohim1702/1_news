from rest_framework import serializers

from sayt.models import Category


class CtgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'