from rest_framework.views import APIView, Request, Response, status
from rest_framework.pagination import PageNumberPagination

from groups.models import Group
from traits.models import Trait

from .models import Pet
from .serializers import PetSerializer


class PetView(APIView, PageNumberPagination):
    def post(self, request: Request):
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group = serializer.validated_data.pop("group")
        traits_list = serializer.validated_data.pop("traits")

        try:
            group_db = Group.objects.get(
                scientific_name__iexact=group["scientific_name"]
            )
        except Group.DoesNotExist:
            group_db = Group.objects.create(**group)

        pet = Pet.objects.create(**serializer.validated_data, group=group_db)

        for trait_pet in traits_list:
            try:
                trait_pet_db = Trait.objects.get(name__iexact=trait_pet["name"])
            except Trait.DoesNotExist:
                trait_pet_db = Trait.objects.create(**trait_pet)

            pet.traits.add(trait_pet_db)

        print(f"{pet.id=}")
        serializer = PetSerializer(instance=pet)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request: Request):
        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request)
        serializer = PetSerializer(instance=result_page, many=True)

        return self.get_paginated_response(serializer.data)
