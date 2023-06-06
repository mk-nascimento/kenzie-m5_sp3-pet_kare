# shell do Django
from pets.models import Pet
from groups.models import Group
from traits.models import Trait

pet_data = {"name": "Beethoven", "age": 1, "weight": 30, "sex": "Male"}
# Criação da instancia de Pet
p1 = Pet(**pet_data)

# Criação e persistindo o grupo
group_data = {"scientific_name": "canis familiaris"}
g1 = Group.objects.create(**group_data)

# Associando o grupo ao pet e persistindo o pet
p1.group = g1
p1.save()


# Criação e persistência das características
trait_1_data = {"name": "curious"}
trait_2_data = {"name": "hairy"}
t1 = Trait.objects.create(**trait_1_data)
t2 = Trait.objects.create(**trait_2_data)

# Associando as características ao pet
p1.traits.add(t1)
p1.traits.add(t2)

# Tentando deletar um grupo associado a pets
g1.delete()
# ProtectedError
