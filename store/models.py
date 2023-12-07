"""
Store app for managing e-commerce products, categories, orders, and sellers.
"""

from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """
    Represents a category for products.

    Attributes:
        name (str): The name of the category.
        parent (Category): The parent category (optional).
    """

    name = models.CharField(max_length=255, db_index=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE)


class Product(models.Model):
    """
    Represents a product for sale.

    Attributes:
        category (Category): The category to which the product belongs.
        created_by (User): The user who created the product.
        title (str): The title of the product.
        author (str): The author of the product (default: "admin").
        description (str): A description of the product.
        image (ImageField): The image of the product.
        price (DecimalField): The price of the product.
        in_stock (bool): Whether the product is in stock.
        is_active (bool): Whether the product is active.
        created (DateTimeField):
        The date and time when the product was created.
        updated (DateTimeField):
        The date and time when the product was last updated.
    """

    category = models.ForeignKey(
        Category, related_name="product", on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default="admin")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="images/")
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Order(models.Model):
    """
    Represents an order for a product.

    Attributes:
        customer_name (str): The customer's name.
        customer_email (EmailField): The customer's email address.
        order_date (DateTimeField):
        The date and time when the order was placed.
        shipping_address (ShippingAddress):
        The shipping address for the order.
    """

    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    order_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey(
        "ShippingAddress", on_delete=models.CASCADE
    )


class ShippingAddress(models.Model):
    """
    Represents a shipping address for an order.

    Attributes:
        name (str): The recipient's name.
        address (str): The shipping address.
        city (str): The city.
    """

    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=255)


class Seller(models.Model):
    """
    Represents a seller of products.

    Attributes:
        name (str): The seller's name.
        email (EmailField): The seller's email address.
        phone_number (str): The seller's phone number.
        products (ManyToManyField[Product]):
        The products sold by the seller.
    """

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)


class SellerProduct(models.Model):
    """
    Represents the relationship between a seller and a product.

    Attributes:
        seller (Seller): The seller.
        product (Product): The product.
    """

    seller = models.ForeignKey("Seller", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
