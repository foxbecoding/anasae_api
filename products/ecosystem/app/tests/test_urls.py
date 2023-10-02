from django.test import SimpleTestCase
from django.urls import reverse, resolve

class TestProductListingUrls(SimpleTestCase):
    
    def test_product_listing_list_url_resolves(self):
        url = reverse('product-listing-list')
        self.assertEqual(resolve(url).view_name, 'product-listing-list')
    
    def test_product_listing_detail_url_resolves(self):
        url = reverse('product-listing-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'product-listing-detail')

class TestProductListingBaseVariantUrls(SimpleTestCase):
    
    def test_product_listing_base_variant_list_url_resolves(self):
        url = reverse('product-listing-base-variant-list')
        self.assertEqual(resolve(url).view_name, 'product-listing-base-variant-list')
    
    def test_product_listing_base_variant_detail_url_resolves(self):
        url = reverse('product-listing-base-variant-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'product-listing-base-variant-detail')

class TestProductUrls(SimpleTestCase):
    
    def test_product_list_url_resolves(self):
        url = reverse('product-list')
        self.assertEqual(resolve(url).view_name, 'product-list')
    
    def test_product_detail_url_resolves(self):
        url = reverse('product-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'product-detail')

class TestProductPriceUrls(SimpleTestCase):
    
    def test_product_price_list_url_resolves(self):
        url = reverse('product-price-list')
        self.assertEqual(resolve(url).view_name, 'product-price-list')
    
    def test_product_price_detail_url_resolves(self):
        url = reverse('product-price-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'product-price-detail')

class TestProductDimensionUrls(SimpleTestCase):
    
    def test_product_dimension_list_url_resolves(self):
        url = reverse('product-dimension-list')
        self.assertEqual(resolve(url).view_name, 'product-dimension-list')
    
    def test_product_dimension_detail_url_resolves(self):
        url = reverse('product-dimension-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'product-dimension-detail')

class TestProductSpecificationUrls(SimpleTestCase):
    
    def test_product_specification_list_url_resolves(self):
        url = reverse('product-specification-list')
        self.assertEqual(resolve(url).view_name, 'product-specification-list')
    
    def test_product_specification_detail_url_resolves(self):
        url = reverse('product-specification-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'product-specification-detail')

class TestProductImageUrls(SimpleTestCase):
    
    def test_product_image_list_url_resolves(self):
        url = reverse('product-image-list')
        self.assertEqual(resolve(url).view_name, 'product-image-list')
    
    def test_product_specification_image_url_resolves(self):
        url = reverse('product-image-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).view_name, 'product-image-detail')