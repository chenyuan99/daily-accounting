from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from .models import (
    ImageModel,
    Currency,
    Account,
    Category,
    SubCategory,
    HistoryRecord,
    TransferRecord,
    Statement
)


@admin.register(ImageModel)
class ImageModelAdmin(ImportExportModelAdmin):
    """Admin interface for ImageModel."""
    list_display = ('id', 'display_image')
    search_fields = ('id',)

    def display_image(self, obj):
        """Display image thumbnail in admin."""
        if obj.img:
            return format_html('<img src="{}" width="50" height="50" />', obj.img.url)
        return "No Image"
    display_image.short_description = 'Image'


@admin.register(Currency)
class CurrencyAdmin(ImportExportModelAdmin):
    """Admin interface for Currency."""
    list_display = ('name', 'icon', 'display_icon')
    search_fields = ('name',)
    ordering = ('name',)

    def display_icon(self, obj):
        """Display currency icon."""
        return format_html('<span style="font-size: 20px;">{}</span>', obj.icon)
    display_icon.short_description = 'Icon Preview'


@admin.register(Account)
class AccountAdmin(ImportExportModelAdmin):
    """Admin interface for Account."""
    list_display = ('name', 'amount', 'currency', 'owner', 'created_date', 'updated_date')
    list_filter = ('currency', 'owner', 'created_date')
    search_fields = ('name', 'owner__username')
    ordering = ('-created_date',)
    readonly_fields = ('created_date', 'updated_date')
    raw_id_fields = ('owner',)
    list_editable = ('currency',)


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    """Admin interface for Category."""
    list_display = ('name', 'icon', 'category_type', 'display_icon')
    list_filter = ('category_type',)
    search_fields = ('name',)
    ordering = ('name',)

    def display_icon(self, obj):
        """Display category icon."""
        return format_html('<span style="font-size: 20px;">{}</span>', obj.icon)
    display_icon.short_description = 'Icon Preview'


@admin.register(SubCategory)
class SubCategoryAdmin(ImportExportModelAdmin):
    """Admin interface for SubCategory."""
    list_display = ('name', 'icon', 'parent', 'display_icon')
    list_filter = ('parent',)
    search_fields = ('name', 'parent__name')
    ordering = ('parent', 'name')
    raw_id_fields = ('parent',)

    def display_icon(self, obj):
        """Display subcategory icon."""
        return format_html('<span style="font-size: 20px;">{}</span>', obj.icon)
    display_icon.short_description = 'Icon Preview'


@admin.register(HistoryRecord)
class HistoryRecordAdmin(ImportExportModelAdmin):
    """Admin interface for HistoryRecord."""
    list_display = ('id', 'account', 'amount', 'currency', 'category', 'sub_category', 
                   'time_of_occurrence', 'owner', 'comment')
    list_filter = ('account', 'currency', 'category', 'time_of_occurrence', 'owner')
    search_fields = ('comment', 'account__name', 'category__name', 'owner__username')
    ordering = ('-time_of_occurrence',)
    raw_id_fields = ('account', 'category', 'sub_category', 'owner')
    date_hierarchy = 'time_of_occurrence'
    readonly_fields = ('created_date', 'updated_date')
    list_per_page = 50


@admin.register(TransferRecord)
class TransferRecordAdmin(ImportExportModelAdmin):
    """Admin interface for TransferRecord."""
    list_display = ('id', 'from_account', 'to_account', 'amount', 'currency', 
                   'time_of_occurrence', 'owner', 'comment')
    list_filter = ('from_account', 'to_account', 'currency', 'time_of_occurrence', 'owner')
    search_fields = ('comment', 'from_account__name', 'to_account__name', 'owner__username')
    ordering = ('-time_of_occurrence',)
    raw_id_fields = ('from_account', 'to_account', 'owner')
    date_hierarchy = 'time_of_occurrence'
    readonly_fields = ('created_date', 'updated_date')
    list_per_page = 50


@admin.register(Statement)
class StatementAdmin(ImportExportModelAdmin):
    """Admin interface for Statement."""
    list_display = ('id', 'created_date')
    ordering = ('-created_date',)
    date_hierarchy = 'created_date'
    readonly_fields = ('created_date',)
