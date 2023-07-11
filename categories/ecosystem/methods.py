from categories.models import *
from categories.serializers import *
from utils.helpers import create_uid

def test_categories(): 
    Category_Instance = Category.objects.create(
        uid = create_uid('cat-'),
        title = "Men's fashion",
        description = "Shop men's fashion from the best Black Brands.",
        is_active = True
    )
    Category_Instance.save()

    Category_Product_Specification_Instance = CategoryProductSpecification.objects.create(
        category = Category_Instance
    )
    Category_Product_Specification_Instance.save()

    category_specifications = [
        { 'item': 'Color', 'is_required': True, 'options': ['Red','Blue','Green'] },
        { 'item': 'Brand', 'is_required': False, 'options': [] }
    ]

    for cat_specs in category_specifications:
        qs = CategoryProductSpecificationItem.objects.create(
            category_product_specification = Category_Product_Specification_Instance,
            item = cat_specs['item'],
            is_required = cat_specs['is_required']
        )
        qs.save()

        if len(cat_specs['options']) > 0:
            for option in cat_specs['options']:
                qs = CategoryProductSpecificationItemOption.objects.create(
                    category_product_specification_item = qs,
                    option = option
                )
                qs.save()

    Subcategory_Instance = Subcategory.objects.create(
        category = Category_Instance,
        uid = create_uid('scat-'),
        title = 'Bottoms',
        description = 'Best bottoms for men from black brands',
        is_active = True
    )
    Subcategory_Instance.save()
    
    return {
        'category_instance': Category_Instance,
        'category_data': CategorySerializer(Category_Instance).data,
        'subcategory_instance': Subcategory_Instance,
        'subcategory_data': SubcategorySerializer(Subcategory_Instance).data,
    }