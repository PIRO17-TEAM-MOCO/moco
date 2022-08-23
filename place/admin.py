from django.contrib import admin
from .models import Place, PlaceImage

# PlaceImage 클래스를 inline으로 나타낸다.
class PhotoInline(admin.TabularInline):
    model = PlaceImage

# Place 클래스는 해당하는 PlaceImage 객체를 리스트로 관리한다. 
class PlaceAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, ]

# Register your models here.
admin.site.register(Place, PlaceAdmin)