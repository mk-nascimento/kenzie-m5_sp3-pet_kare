from rest_framework.views import APIView, Request, Response, status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

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

        serializer = PetSerializer(instance=pet)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request: Request):
        trait_query = request.query_params.get("trait", None)
        pets = Pet.objects.all()

        if trait_query:
            pets = pets.filter(traits__name__iexact=trait_query)
        result_page = self.paginate_queryset(pets, request)
        serializer = PetSerializer(instance=result_page, many=True)

        return self.get_paginated_response(data=serializer.data)


class PetDetailView(APIView, PageNumberPagination):
    def get(self, _: Request, pet_id: int):
        pet = get_object_or_404(Pet, pk=pet_id)
        serializer = PetSerializer(instance=pet)

        return Response(serializer.data)

    def patch(self, resquest: Request, pet_id: int):
        pet = get_object_or_404(Pet, pk=pet_id)

        serializer = PetSerializer(data=resquest.data, partial=True)
        serializer.is_valid(raise_exception=True)

        group = serializer.validated_data.pop("group", None)
        traits_list: list = serializer.validated_data.pop("traits", None)

        if group:
            try:
                group_db = Group.objects.get(
                    scientific_name__iexact=group["scientific_name"]
                )
            except Group.DoesNotExist:
                group_db = Group.objects.create(**group)

            pet.group = group_db

        if traits_list:
            new_traits: list = []
            for trait_pet in traits_list:
                try:
                    trait_pet_db = Trait.objects.get(name__iexact=trait_pet["name"])
                except Trait.DoesNotExist:
                    trait_pet_db = Trait.objects.create(**trait_pet)
                new_traits.append(trait_pet_db)

            pet.traits.set(new_traits)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()
        serializer = PetSerializer(instance=pet)

        return Response(data=serializer.data)

    def delete(self, _: Request, pet_id: int):
        pet = get_object_or_404(Pet, pk=pet_id)
        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
