from django.contrib import admin
from .models import Address, Category, Product, Cart, Order, ProductImage, Size, Color
from django.utils.safestring import mark_safe


class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "locality", "city", "state")
    list_filter = ("city", "state")
    list_per_page = 10
    search_fields = ("locality", "city", "state")


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "image_tag",
        "is_active",
        "is_featured",
        "updated_at",
    )
    list_editable = ("slug", "is_active", "is_featured")
    list_filter = ("is_active", "is_featured")
    list_per_page = 10
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = (
        "title",
        "slug",
        "image_tag",
        "category",
        "is_active",
        "is_featured",
        "updated_at",
    )
    list_editable = ("slug", "category", "is_active", "is_featured")
    list_filter = ("category", "is_active", "is_featured")
    list_per_page = 10
    search_fields = ("title", "category", "short_description")
    prepopulated_fields = {"slug": ("title",)}


class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "product",
        "quantity",
        "created_at",
        "product_color",
        "product_size",
    )
    list_editable = ("quantity",)
    list_filter = ("created_at",)
    list_per_page = 20
    search_fields = ("user", "product")


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "product",
        "quantity",
        "get_color",
        "get_size",
        "ordered_date",
        "status",
    )
    list_editable = ("quantity", "status")
    list_filter = ("status", "ordered_date")
    list_per_page = 20
    search_fields = ("user", "product")

    def get_color(self, obj):
        return obj.color.title if obj.color else "N/A"

    get_color.short_description = "Color"

    def get_size(self, obj):
        return obj.size.title if obj.size else "N/A"

    get_size.short_description = "Size"

    def product_image(self, obj):
        product_images = ProductImage.objects.filter(product=obj.product)
        if product_images.exists():
            first_image = product_images.first()
            return mark_safe(
                '<img src="%s" width="50" height="50" />' % first_image.image.url
            )
        return "No Image Available"

    product_image.short_description = "Product Image"


class ColorAdmin(admin.ModelAdmin):
    list_display = ("title", "color_bg")


class SizeAdmin(admin.ModelAdmin):
    list_display = ("id", "title")


admin.site.register(Address, AddressAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(ProductImage)
