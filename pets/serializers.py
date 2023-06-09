from rest_framework import serializers

from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer
from .models import SexPet


class Pet(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.CharField(max_length=20, choices=SexPet.choices)

    group = GroupSerializer()
    traits = TraitSerializer(many=True)
