from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from PIL import Image
import xml.etree.ElementTree as ET

def validar_imagen_o_svg(value):
    # Obtener la extensión del archivo
    extension = value.name.split('.')[-1].lower()
    extensiones_permitidas = ['png', 'jpg', 'jpeg', 'svg']

    if extension not in extensiones_permitidas:
        raise ValidationError('Solo se permiten imágenes (PNG, JPG) y archivos SVG.')

    # Validar imágenes rasterizadas con Pillow
    if extension in ['png', 'jpg', 'jpeg']:
        try:
            Image.open(value).verify()  # Verificar si es una imagen válida
        except Exception:
            raise ValidationError('El archivo no es una imagen válida.')

    # Validar archivos SVG como XML
    if extension == 'svg':
        try:
            value.seek(0)  # Restablecer el puntero del archivo al inicio
            ET.parse(value)  # Intentar analizar el contenido como XML
        except ET.ParseError:
            raise ValidationError('El archivo SVG no es válido.')
        

class Presupuesto(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre del Presupuesto")
    start_date = models.DateField(verbose_name="Fecha de Inicio", default=now)
    end_date = models.DateField(verbose_name="Fecha de Fin", null=True, blank=True)
    initial_budget = models.FloatField(verbose_name="Presupuesto Inicial")
    is_active= models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date or 'Presente'})"
    
    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = "Presupuestos"
        verbose_name = "Presupuesto"

class Categoria(models.Model):
    name = models.CharField(max_length=50,verbose_name="Categoria")
    icon = models.FileField(upload_to='archivos/', validators=[validar_imagen_o_svg], verbose_name="Icono")

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        ordering = ['id']
        verbose_name_plural = "Categorías"
        verbose_name = "Categoría" 

class Gasto (models.Model):
    expense_name = models.CharField(max_length=150, verbose_name="Nombre del Gasto")
    amount = models.FloatField(verbose_name="Cantidad en Pesos")
    category = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoria")
    date = models.DateField(default=now, verbose_name="Fecha")
    is_paid = models.BooleanField(default=False, verbose_name="Pagado")
    budget = models.ForeignKey(Presupuesto, on_delete=models.CASCADE, verbose_name="Presupuesto")

    def __str__(self):
        return f"{self.expense_name}"
    
    class Meta:
        ordering = ['amount', 'expense_name']
        verbose_name_plural = "Gastos"
        verbose_name = "Gasto"

