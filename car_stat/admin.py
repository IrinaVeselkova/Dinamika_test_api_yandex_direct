from django.contrib import admin
from .models import *

@admin.register(QueryResult)
class QueryAdmin(admin.ModelAdmin):
    list_display = ['car_brand', 'region', 'query_text', 'count', 'timestamp']
    ordering = ['timestamp','region' ]


admin.site.register(Region)
admin.site.register(QueryType)
admin.site.register(CarBrand)

# Register your models here.
