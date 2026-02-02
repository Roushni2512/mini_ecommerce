from app import app, db, Product

def seed_products():
    with app.app_context():
        # List of aesthetic/minimalist sample products categorized
        products = [
            # MEN
            {
                "name": "Men's Minimalist Tee",
                "price": 25.00,
                "image_url": "https://images.unsplash.com/photo-1521572101914-14798a6f0b74?auto=format&fit=crop&w=800&q=80",
                "category": "Men"
            },
            {
                "name": "Men's Classic Blazer",
                "price": 120.00,
                "image_url": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=800&q=80",
                "category": "Men"
            },
            {
                "name": "Men's Urban Sneakers",
                "price": 85.00,
                "image_url": "https://images.unsplash.com/photo-1549298916-b41d501d3772?auto=format&fit=crop&w=800&q=80",
                "category": "Men"
            },
            # WOMEN
            {
                "name": "Women's Silk Blouse",
                "price": 45.00,
                "image_url": "https://images.unsplash.com/photo-1564584217132-2271feaeb3c5?auto=format&fit=crop&w=800&q=80",
                "category": "Women"
            },
            {
                "name": "Women's Summer Dress",
                "price": 65.00,
                "image_url": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?auto=format&fit=crop&w=800&q=80",
                "category": "Women"
            },
            {
                "name": "Women's Leather Tote",
                "price": 180.00,
                "image_url": "https://images.unsplash.com/photo-1590874102752-cecfce64e559?auto=format&fit=crop&w=800&q=80",
                "category": "Women"
            },
            # KIDS
            {
                "name": "Kids' Cotton Hoodie",
                "price": 35.00,
                "image_url": "https://images.unsplash.com/photo-1519233073524-7935c363988c?auto=format&fit=crop&w=800&q=80",
                "category": "Kids"
            },
            {
                "name": "Kids' Denim Jacket",
                "price": 55.00,
                "image_url": "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?auto=format&fit=crop&w=800&q=80",
                "category": "Kids"
            },
            {
                "name": "Kids' Canvas Shoes",
                "price": 28.00,
                "image_url": "https://images.unsplash.com/photo-1514989940723-e8e51635b782?auto=format&fit=crop&w=800&q=80",
                "category": "Kids"
            }
        ]

        print("Seeding categorized products...")
        
        # Clear existing products to avoid duplicates/confusion with old non-categorized ones
        # Use with caution in real apps, but for this exercise it helps see the change clearly
        # db.session.query(Product).delete() 
        
        for product_data in products:
            existing = Product.query.filter_by(name=product_data['name']).first()
            if not existing:
                new_product = Product(**product_data)
                db.session.add(new_product)
                print(f"Added: {product_data['name']} ({product_data['category']})")
            else:
                existing.image_url = product_data['image_url']
                existing.category = product_data['category']
                existing.price = product_data['price']
                print(f"Updated: {product_data['name']}")
        
        db.session.commit()
        print("Seeding complete!")

if __name__ == '__main__':
    seed_products()

