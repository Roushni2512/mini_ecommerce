from app import app, db, Product

def seed_products():
    with app.app_context():
        # List of aesthetic/minimalist sample products
        products = [
            {
                "name": "Minimalist Watch",
                "price": 120.00,
                "image_url": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?auto=format&fit=crop&w=400&q=80"
            },
            {
                "name": "Ceramic Vase",
                "price": 45.00,
                "image_url": "https://images.unsplash.com/photo-1581539250439-c96689b516dd?auto=format&fit=crop&w=400&q=80"
            },
            {
                "name": "Leather Tote",
                "price": 180.00,
                "image_url": "https://images.unsplash.com/photo-1590874102752-cecfce64e559?auto=format&fit=crop&w=400&q=80"
            },
            {
                "name": "Bamboo Plant",
                "price": 25.00,
                "image_url": "https://images.unsplash.com/photo-1599598425947-738d99c35b6c?auto=format&fit=crop&w=400&q=80"
            },
            {
                "name": "Analog Camera",
                "price": 350.00,
                "image_url": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=400&q=80"
            },
            {
                "name": "Linen Notebook",
                "price": 18.00,
                "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=400&q=80"
            },
             {
                "name": "Desk Lamp",
                "price": 60.00,
                "image_url": "https://images.unsplash.com/photo-1507473888900-52e1adad5481?auto=format&fit=crop&w=400&q=80"
            },
            {
                "name": "Modern Chair",
                "price": 150.00,
                "image_url": "https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?auto=format&fit=crop&w=400&q=80"
            },
            {
                "name": "Bamboo Chair",
                "price": 120.00,
                "image_url": "https://images.unsplash.com/photo-1551216393-27038e932b12?auto=format&fit=crop&w=400&q=80"
            }
        ]

        print("Seeding products...")
        
        for product_data in products:
            # Check if product exists
            existing = Product.query.filter_by(name=product_data['name']).first()
            if not existing:
                new_product = Product(**product_data)
                db.session.add(new_product)
                print(f"Added: {product_data['name']}")
            else:
                # Update image_url if exists to ensure they are fixed
                existing.image_url = product_data['image_url']
                # existing.price = product_data['price'] # Optional: update price too
                print(f"Updated image for: {product_data['name']}")
        
        db.session.commit()
        print("Seeding complete!")

if __name__ == '__main__':
    seed_products()

