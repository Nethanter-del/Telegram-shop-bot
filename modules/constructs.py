class Constructs:
    async def format_products(products):
        categories = {}
        for product in products:
            category = product['category']
            if category not in categories:
                categories[category] = {}
            product_name = product['product_name']
            if product_name not in categories[category]:
                categories[category][product_name] = {'count': 0, 'description': product['product_description'], 'price': product['price']}
            categories[category][product_name]['count'] += 1

        result = "💎 Товары в наличии: \n"
        for category, items in categories.items():
            result += f"--- {category}\n"
            for product_name, details in items.items():
                count = details['count']
                description = details['description']
                price = details['price']
                result += f"{product_name} - {description} - {price} ₽ ({count} шт.)\n"
        return result
    async def format_products1(products):
        categories = {}
        for product in products:
            category = product['category']
            if category not in categories:
                categories[category] = {}
            product_name = product['product_name']
            if product_name not in categories[category]:
                categories[category][product_name] = {'count': 0, 'description': product['product_description'], 'price': product['price']}
            categories[category][product_name]['count'] += 1
        return categories