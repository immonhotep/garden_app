from .models import Plant
from collections import defaultdict


def navbar_context(request):
    plant_categories=[("Vegetables","fa-carrot"),("Fruits","fa-lemon"),("Flowers","fa-spa"),("Ornamentals","fa-tree"),("Other","fa-circle-question")]
    plant_cat_dict = defaultdict(list) 
    for key, value in plant_categories:
        {plant_cat_dict[key].append(value)} 
        count = Plant.objects.filter(category__iexact=key).count()
        plant_cat_dict[key].extend([count])
    plant_cat_dict=dict(plant_cat_dict)
    
    return{'plant_cat_dict':plant_cat_dict}
