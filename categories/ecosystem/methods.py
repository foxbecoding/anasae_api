from categories.models import *
from utils.helpers import create_uid

def test_categories(): 
    Category_Instance = Category.objects.create(
        uid = create_uid('cat-'),
        title = "Men's fashion",
        description = "Shop men's fashion from the best Black Brands.",
        is_active = True
    )
    Category_Instance.save()

    Subcategory_Instance = Subcategory.objects.create(
        category = Category_Instance,
        uid = create_uid('scat-'),
        title = 'Bottoms',
        description = 'Best bottoms for men from black brands',
        is_active = True
    )
    Subcategory_Instance.save()
    