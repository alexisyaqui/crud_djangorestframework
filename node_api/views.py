from rest_framework.response import Response
from rest_framework import status, generics
from node_api.models import NotaModelo
from node_api.serializers import NotaSerializer

import math
from datetime import datetime

"""CREAR  METODO GET Y POST"""
class Notas(generics.GenericAPIView):
    serializer_class = NotaSerializer
    queryset = NotaModelo.objects.all()

    """paginacion"""
    def get(self, request):
        page_num = int(request.GET.get("pagina", 1))
        limit_num = int(request.GET.get("limite", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("Buscar")
        nota = NotaModelo.objects.all()
        total_notas = nota.count()

        if search_param:
            nota = nota.filter(title__icontains=search_param)
        serializer = self.serializer_class(nota[start_num:end_num], many=True)

        return Response({
            "estado": "Operacion con exito!!",
            "total": total_notas,
            "paginas": page_num,
            "ultima_pagina": math.ceil(total_notas / limit_num),
            "nota": serializer.data
        })
    
    """Crear nota con metodo post"""
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"estado": "succes", "data": {"notas":serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"estado": "fallado", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


"""EDITAR Y ACTUALIZAR CON PATCH Y DELETE"""
class NotaDetalle(generics.GenericAPIView):
    queryset = NotaModelo.objects.all()
    serializer_class = NotaSerializer


    ##obtener nota
    def get_nota(self, pk):
        try:
            return NotaModelo.objects.get(pk=pk)
        except:
            return None
        
        
    def get(self, request, pk):
        nota = self.get_nota(pk=pk)
        
        if nota == None:
            return Response({"estado": "fallado", "message": f"Nota with Id: {pk} no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(nota)
        return Response({"estado": "success", "data": {"nota": serializer.data}})
    

    ### para buscar nota
    def patch(self, request, pk):
        nota = self.get_nota(pk)

        if nota == None:
            return Response({"estado": "fallado", "message": f"Nota with Id: {pk} no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(
            nota, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.validated_data['Actualizado'] = datetime.now()
            serializer.save()
            return Response({"estado": "succes", "data": {"nota": serializer.data}})
        return Response({"estado": "fallado", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

    ##eliminar nota
    def delete(self, request, pk):
        nota = self.get_nota(pk)

        if nota == None:
            return Response({"estado": "fallado", "message": f"Nota with Id: {pk} no encontrado"}, status=status.HTTP_404_BAD_REQUEST)
        
        nota.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    