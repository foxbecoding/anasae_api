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
        { 'item': 'Color', 'is_required': True },
        { 'item': 'Size', 'is_required': True },
        { 'item': 'Brand', 'is_required': False }
    ]

    for cat_spec in category_specifications:
        qs = CategoryProductSpecificationItem.objects.create(
            category_product_specification = Category_Product_Specification_Instance,
            item = cat_spec['item'],
            is_required = cat_spec['is_required']
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

    Subcategory_Product_Specification_Instance = SubcategoryProductSpecification.objects.create(
        subcategory = Subcategory_Instance
    )
    Subcategory_Product_Specification_Instance.save()

    subcategory_specifications = [
        { 'item': 'Color', 'is_required': True },
        { 'item': 'Size', 'is_required': True },
        { 'item': 'Brand', 'is_required': False }
    ]

    for scat_spec in subcategory_specifications:
        qs = SubcategoryProductSpecificationItem.objects.create(
            subcategory_product_specification = Subcategory_Product_Specification_Instance,
            item = scat_spec['item'],
            is_required = scat_spec['is_required']
        )
        qs.save()

    category_data = CategorySerializer(Category_Instance).data
    cat_pro_spec_items_instances = CategoryProductSpecificationItem.objects.filter(category_product_specification_id=category_data['product_specification'])
    cat_pro_spec_data = CategoryProductSpecificationItemSerializer(cat_pro_spec_items_instances, many=True).data
    category_data['product_specification_id'] = category_data['product_specification']
    category_data['product_specification'] = cat_pro_spec_data
    
    subcategory_data = SubcategorySerializer(Category_Instance).data
    subcat_pro_spec_items_instances = SubcategoryProductSpecificationItem.objects.filter(subcategory_product_specification_id=subcategory_data['product_specification'])
    subcat_pro_spec_data = SubcategoryProductSpecificationItemSerializer(subcat_pro_spec_items_instances, many=True).data
    subcategory_data['product_specification_id'] = subcategory_data['product_specification']
    subcategory_data['product_specification'] = subcat_pro_spec_data

    return {
        'category_instance': Category_Instance,
        'category_data': category_data,
        'subcategory_instance': Subcategory_Instance,
        'subcategory_data': subcategory_data
    }