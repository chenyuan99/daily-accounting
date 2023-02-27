from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

admin.site.register(ImageModel)

@admin.register(Currency)
class CurrencyAdmin(ImportExportModelAdmin):
    model = Currency

@admin.register(Account)
class AccountAdmin(ImportExportModelAdmin):
    model = Account

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    model = Category

@admin.register(SubCategory)
class SubCategoryAdmin(ImportExportModelAdmin):
    model = SubCategory

# @admin.register(HistoryRecord)
class HistoryRecordAdmin(ImportExportModelAdmin):
    model = HistoryRecord
    list_display = ('id','amount')

# admin.site.register(Currency)
# admin.site.register(Account)
# admin.site.register(Category)
# admin.site.register(SubCategory)
admin.site.register(HistoryRecord, HistoryRecordAdmin)
