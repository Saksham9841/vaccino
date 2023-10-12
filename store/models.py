from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    locality = models.CharField(max_length=150, verbose_name="Nearest Location")
    city = models.CharField(max_length=150, verbose_name="City")
    state = models.CharField(max_length=150, verbose_name="State")

    def __str__(self):
        return self.locality


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Category Title")
    slug = models.SlugField(max_length=55, verbose_name="Category Slug")
    description = models.TextField(blank=True, verbose_name="Category Description")
    category_image = models.ImageField(
        upload_to="category", blank=True, null=True, verbose_name="Category Image"
    )
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("-created_at",)

    def image_tag(self):
        if self.category_image:
            return mark_safe(
                '<img src="%s" width="50" height="50" />' % (self.category_image.url)
            )
        else:
            return "No Image Available"

    def __str__(self):
        return self.title


# Color
class Color(models.Model):
    title = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Colors"

    def color_bg(self):
        return mark_safe(
            f'<div style="width:30px; height:30px; background-color:{self.color_code}"></div>'
        )

    def __str__(self):
        return self.title


# Size
class Size(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="Size Id")
    title = models.CharField(max_length=100, verbose_name="Title")

    class Meta:
        verbose_name_plural = "Sizes"

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="product", verbose_name="Product Image")

    def __str__(self):
        return self.image.name


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name="Product Title")
    slug = models.SlugField(max_length=160, verbose_name="Product Slug")
    sku = models.CharField(
        max_length=255, unique=True, verbose_name="Unique Product ID (SKU)"
    )
    short_description = models.TextField(verbose_name="Short Description")
    detail_description = models.TextField(
        blank=True, null=True, verbose_name="Detail Description"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.ForeignKey(
        Category, verbose_name="Product Category", on_delete=models.CASCADE
    )
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    color = models.ManyToManyField(Color, verbose_name="Product Color", blank=True)
    size = models.ManyToManyField(Size, verbose_name="Product Size", blank=True)

    class Meta:
        verbose_name_plural = "Products"
        ordering = ("-created_at",)

    def image_tag(self):
        if first_image := self.images.first():
            return mark_safe(
                f'<img src="{first_image.image.url}" width="50" height="50" />'
            )
        else:
            return "No Image Available"

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, verbose_name="Product", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")
    product_color = models.TextField(default="Red", verbose_name="Color")
    product_size = models.TextField(default="Medium", verbose_name="Size")

    def __str__(self):
        return str(self.user)

    @property
    def total_price(self):
        return self.quantity * self.product.price


STATUS_CHOICES = (
    ("Pending", "Pending"),
    ("Accepted", "Accepted"),
    ("Packed", "Packed"),
    ("On The Way", "On The Way"),
    ("Delivered", "Delivered"),
    ("Cancelled", "Cancelled"),
)


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    address = models.ForeignKey(
        Address, verbose_name="Shipping Address", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, verbose_name="Product", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    color = models.ForeignKey(
        Color, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Color "
    )
    size = models.ForeignKey(
        Size, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Size "
    )

    def __str__(self):
        return f"{self.quantity} x {self.product.title} (Size: {self.size}, Color: {self.color})"

    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name="Ordered Date")
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default="Pending")
