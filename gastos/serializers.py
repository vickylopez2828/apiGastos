from rest_framework import serializers
from .models import Gasto, Categoria, validar_imagen_o_svg, Presupuesto

#va a convertir un  modelo en datos q pueden ser consultados
class GastoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gasto
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('id', 'name', 'icon')
    
    def validate_archivo(self, value):
        validar_imagen_o_svg(value)  
        return value


class PresupuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presupuesto
        fields = '__all__'
