from django.contrib import admin
from .models import Menu, SumOrder, SumDish, Category


class SumDishInline(admin.TabularInline):
    model = SumDish
    extra = 1  # Количество пустых форм для добавления новых блюд


class SumOrderAdmin(admin.ModelAdmin):
    inlines = [SumDishInline]


admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(SumOrder, SumOrderAdmin)