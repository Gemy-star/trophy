from django.contrib import admin
from . import models



@admin.register(models.HomeSlider)
class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ("heading", "button_text", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("heading", "subheading")

admin.site.register(models.Announcement)
