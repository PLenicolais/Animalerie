from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from django.contrib import messages
from .models import Animal, Equipement

# Create your views here.
def animal_list(request):
    animals = Animal.objects.filter()
    return render(request, 'animalerie/animal_list.html', {'animals': animals})

def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    lieu = animal.lieu
    form=MoveForm()
    return render(request,
                  'animalerie/animal_detail.html',
                  {'animal': animal, 'lieu': lieu, 'form': form})
def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    lieu = animal.lieu
    form = MoveForm()
    if request.method == "POST":
        ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
        form = MoveForm(request.POST, instance=animal)
        if form.is_valid():
            form.save(commit=False)
            nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
            if nouveau_lieu.disponibilite=="Libre" and nouveau_lieu.id_equip=="Mangeoire" and animal.etat=='Affamé':
                animal.etat="Repus"
                animal.save()
                nouveau_lieu.disponibilite="Occupé"
                nouveau_lieu.save()
                messages.add_message(request, messages.INFO, 'Déplacé vers la mangeoire !')
            elif nouveau_lieu.disponibilite=="Libre" and nouveau_lieu.id_equip=="Roue" and animal.etat=='Repus':
                ancien_lieu.disponibilite="Libre"
                ancien_lieu.save()
                animal.etat="Fatigué"
                animal.save()
                nouveau_lieu.disponibilite = "Occupé"
                nouveau_lieu.save()
                messages.add_message(request, messages.INFO, 'Déplacé vers la roue !')
            elif nouveau_lieu.disponibilite=="Libre" and nouveau_lieu.id_equip=="Nid" and animal.etat=='Fatigué':
                ancien_lieu.disponibilite="Libre"
                ancien_lieu.save()
                animal.etat="Endormi"
                animal.save()
                nouveau_lieu.disponibilite = "Occupé"
                nouveau_lieu.save()
                messages.add_message(request, messages.INFO, 'Déplacé vers le nid !')
            elif nouveau_lieu.disponibilite=="Libre" and nouveau_lieu.id_equip=="Litière" and animal.etat=='Endormi':
                ancien_lieu.disponibilite="Libre"
                ancien_lieu.save()
                animal.etat="Affamé"
                animal.save()
                nouveau_lieu.disponibilite = "Libre"
                nouveau_lieu.save()
                messages.add_message(request, messages.INFO, 'Déplacé vers la litière !')
            else :
                print('message')
                messages.add_message(request, messages.INFO, "Désolé, ce n'est pas possible !")
        return redirect('animal_detail', id_animal=id_animal)
    else:
        form = MoveForm()
        return render(request,
                    'animalerie/animal_detail.html',
                    {'animal': animal, 'lieu': lieu, 'form': form})

