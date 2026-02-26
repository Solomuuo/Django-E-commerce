# admin.py

from django.contrib import admin
from mpesa.models import MpesaTransaction
from .models import OrderItem, Product, Customer, Cart, Order

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality', 'city', 'state', 'zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(MpesaTransaction)
class MpesaTransactionAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'amount', 'mpesa_receipt_number', 'status', 'transaction_date')
    search_fields = ('phone_number', 'mpesa_receipt_number')
    list_filter = ('status', 'transaction_date')
    date_hierarchy = 'transaction_date'
    ordering = ['-transaction_date']
    readonly_fields = ('mpesa_receipt_number', 'transaction_date')
    actions = ['mark_completed', 'mark_failed']

    def mark_completed(self, request, queryset):
        queryset.update(status="Completed")
        self.message_user(request, "Selected transactions marked as Completed.")
    mark_completed.short_description = "Mark selected transactions as Completed"

    def mark_failed(self, request, queryset):
        queryset.update(status="Failed")
        self.message_user(request, "Selected transactions marked as Failed.")
    mark_failed.short_description = "Mark selected transactions as Failed"

# Inline for Order Items inside Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_amount", "status", "created_at")
    list_filter = ("status", "created_at")
    inlines = [OrderItemInline]
    actions = ["mark_as_processing", "mark_as_shipped", "mark_as_delivered", "mark_as_cancelled"]

    def mark_as_processing(self, request, queryset):
        queryset.update(status="Processing")
        self.message_user(request, "Selected orders marked as Processing.")
    mark_as_processing.short_description = "Mark selected orders as Processing"

    def mark_as_shipped(self, request, queryset):
        queryset.update(status="Shipped")
        self.message_user(request, "Selected orders marked as Shipped.")
    mark_as_shipped.short_description = "Mark selected orders as Shipped"

    def mark_as_delivered(self, request, queryset):
        queryset.update(status="Delivered")
        self.message_user(request, "Selected orders marked as Delivered.")
    mark_as_delivered.short_description = "Mark selected orders as Delivered"

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status="Cancelled")
        self.message_user(request, "Selected orders marked as Cancelled.")
    mark_as_cancelled.short_description = "Mark selected orders as Cancelled"

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
