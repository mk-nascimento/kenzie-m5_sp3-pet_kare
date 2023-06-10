from rest_framework import serializers

from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer
from .models import SexPet


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=SexPet.choices, required=False)

    group = GroupSerializer()
    traits = TraitSerializer(many=True)
