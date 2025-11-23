from django.contrib import admin
from .models import Plant , Review , Country




class PlantAdmin (admin.ModelAdmin):
    list_display=("name","category","created_at")

    list_filter=("category","created_at")


class ReviewAdmin(admin.ModelAdmin):
    list_display=("name","created_at")
    list_filter=("name","plant","created_at")


# Register your models here.
admin.site.register(Plant,PlantAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Country)

