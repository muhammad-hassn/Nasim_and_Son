from django.contrib import admin
from .models import Inquiry, InquiryItem

class InquiryItemInline(admin.TabularInline):
    model = InquiryItem
    extra = 0

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    inlines = [InquiryItemInline]
