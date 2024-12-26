from rest_framework import viewsets, permissions
from .serializers import GastoSerializer, CategoriaSerializer, PresupuestoSerializer
from .models import Gasto, Categoria, Presupuesto
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from datetime import date
# Create your views here.
class GastoViewSet(viewsets.ModelViewSet):
    queryset = Gasto.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = GastoSerializer
    @action(detail=False, methods=['get'], url_path='gastos-por-presupuesto')
    def gastos_por_presupuesto(self, request):
        presupuesto_id = request.query_params.get('presupuesto_id')
        
        if not presupuesto_id:
            return Response({"detail": "El ID del presupuesto es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Filtra los gastos por presupuesto
            gastos = Gasto.objects.filter(budget_id=presupuesto_id)
            serializer = self.get_serializer(gastos, many=True)
            return Response(serializer.data)
        except Gasto.DoesNotExist:
            return Response({"detail": "No se encontraron gastos para este presupuesto."}, status=404)
        

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CategoriaSerializer

class PresupuestoViewSet(viewsets.ModelViewSet):
    queryset = Presupuesto.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PresupuestoSerializer

    @action(detail=False, methods=['get'], url_path='active')
    def active(self, request):
        budget = Presupuesto.objects.filter(is_active=True).first()
        if budget:
            serializer = self.get_serializer(budget)
            return Response(serializer.data)
        return Response({"detail": "No hay presupuesto activo."}, status=404)

    @action(detail=False, methods=['put'], url_path='close')
    def close(self, request):
        presupuesto_id = request.data.get('presupuesto_id')  # Usamos `data` en lugar de `query_params` para POST.
        print(presupuesto_id)
        if not presupuesto_id:
            return Response({"detail": "Se requiere un ID de presupuesto."}, status=400)
        
        budget = Presupuesto.objects.filter(id=presupuesto_id, is_active=True).first()  # Buscamos solo presupuestos activos.
        print(budget, "budget")
        if not budget:
            return Response({"detail": "Presupuesto no encontrado o ya cerrado."}, status=404)
    
        budget.is_active = False
        budget.end_date = date.today()
        budget.save()  

        serializer = self.get_serializer(budget)
        return Response(serializer.data, status=200)