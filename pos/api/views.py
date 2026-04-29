from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pos_app.models import TableResto
from api.serializers import (RegisterUserSerializers, TableRestoSerializers)
from rest_framework import generics


class RegisterUserApiView(APIView):
    serializer_class = RegisterUserSerializers

    def post(self, request, format = None):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'selamat anda telah terdatar',
                'data' : serializer.data,
            }
            return Response(response_data, status = status.HTTP_201_CREATED)
        
        return Response({
            'status' : status.HTTP_400_BAD_REQUEST,
            'data' : serializer.errors
        }, status = status.HTTP_400_BAD_REQUEST)
    
class TableRestoListApiView(APIView):

    def get(self, request, *args, **kwargs):
        table_resto = TableResto.objects.all()
        serializer = TableRestoSerializers(table_resto, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'code': request.data.get('code'),
            'name': request.data.get('name'),
            'capacity': request.data.get('capacity'),
        }

        serializer = TableRestoSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Data sukses dibuat',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TableRestoDetailApiView(APIView):

    def get_object(self, id):
        try:
            return TableResto.objects.get(id=id)
        except TableResto.DoesNotExist:
            return None

    def get(self, request, id, *args, **kwargs):
        instance = self.get_object(id)
        if not instance:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Data DOES NOT EXIST',
                'data': {}
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = TableRestoSerializers(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        instance = self.get_object(id)
        if not instance:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Data DOES NOT EXIST',
                'data': {}
            }, status=status.HTTP_404_NOT_FOUND)

        data = {
            'code': request.data.get('code'),
            'name': request.data.get('name'),
            'capacity': request.data.get('capacity'),
            'table_status': request.data.get('table_status'),
            'status': request.data.get('status'),
        }

        serializer = TableRestoSerializers(instance=instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Data sukses diupdate',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        instance = self.get_object(id)
        if not instance:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Data DOES NOT EXIST',
                'data': {}
            }, status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Data sukses dihapus'
        }, status=status.HTTP_200_OK)