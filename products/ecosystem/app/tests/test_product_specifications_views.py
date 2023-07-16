    # spec_values = data['spec_values']
    #         product_specs = []
    #         if product['category'] and product['subcategory']:
    #             specifications = self.categories['subcategory_data']['product_specification']
    #             for spec in list(zip(specifications, spec_values)):
    #                 spec_data, spec_value = spec[0], spec[1]
    #                 product_specs.append({
    #                     'label': spec_data['item'],
    #                     'is_required': spec_data['is_required'],
    #                     'value': spec_value,
    #                 })
    #         else:
    #             specifications = self.categories['category']['product_specification']
    #             for spec in list(zip(specifications, spec_values)):
    #                 spec_data, spec_value = spec[0], spec[1]
    #                 product_specs.append({
    #                     'label': spec_data['item'],
    #                     'is_required': spec_data['is_required'],
    #                     'value': spec_value,
    #                 })

    #         product['specifications'] = product_specs
    #         product['images'] = [tmp_image() for x in range(7)]