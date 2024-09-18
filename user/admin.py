from django.contrib import admin
from .models import Farmer, Staff

class FarmerInline(admin.TabularInline):
    model = Farmer
    extra = 0
    fields = [
        'id','farmer_name', 'phone_number', 'H_start_date', 'location', 
        'fpo_name', 'rice_type', 'water_source', 'geoJSON'
    ]
    readonly_fields = [
        'id','farmer_name', 'phone_number', 'H_start_date', 'location', 
        'fpo_name', 'rice_type', 'water_source', 'geoJSON'
    ]

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ( 
        'id','farmer_name', 'phone_number', 'H_start_date', 'location', 
        'fpo_name', 'rice_type', 'water_source', 'staff', 'geoJSON'
    )
    search_fields = (
        'id','farmer_name', 'phone_number', 'location', 
        'fpo_name', 'rice_type'
    )
    list_filter = ('location', 'rice_type', 'water_source', 'H_start_date')
    autocomplete_fields = ['staff']
    ordering = ['farmer_name']

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'location', 'fpo_name')
    search_fields = ('name', 'phone_number', 'location', 'fpo_name')
    list_filter = ('location',)
    inlines = [FarmerInline]
    ordering = ['name']
