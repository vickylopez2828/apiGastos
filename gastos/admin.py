from django.contrib import admin
from .models import Categoria, Gasto, Presupuesto

# Register your models here.
class GastosInline(admin.StackedInline):    
    model = Gasto
    max_num=0 
    can_delete = False
    show_change_link = False 
    fields = ('expense_name', 'amount', 'category', 'date', 'is_paid') 
    readonly_fields  = ('expense_name', 'amount', 'category', 'date', 'is_paid') 

class GastoAdmin(admin.ModelAdmin):
    list_display=['expense_name', 'amount', 'category', 'date', 'is_paid', 'budget']
    list_filter=['category__name', 'budget__name']
    

class CategoriaAdmin(admin.ModelAdmin):
    list_display=['id','name', 'icon']

class PresupuestoAdmin(admin.ModelAdmin):
    list_display=['name', 'start_date', 'end_date', 'initial_budget']
    inlines=[GastosInline]

admin.site.register(Presupuesto, PresupuestoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Gasto, GastoAdmin)