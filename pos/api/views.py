from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pos_app.models import TableResto
from api.serializers import TableRestoSerializers

class TableRestoListApiView(APIView):

    def get(self, request, id=None, *args, **kwargs):
        if id is not None:
            table_resto_instance = self.get_object(id)
            if not table_resto_instance:
                return Response(
                    {
                        'status': status.HTTP_404_NOT_FOUND,
                        'message': 'Data DOES NOT EXIST....',
                        'data': {}
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = TableRestoSerializers(table_resto_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        table_resto = TableResto.objects.all()
        serializer = TableRestoSerializers(table_resto, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self, id):
        try:
            return TableResto.objects.get(id =id)
        except TableResto.DoesNotExist:
            return None
    
    def post(self, request, *args, **kwargs):
        data = {
            'code' : request.data.get('code'),
            'name' : request.data.get('name'),
            'capacity' : request.data.get('capacity'),
        }
        serializer = TableRestoSerializers(data = data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_201_CREATED,
                'message' : 'Data sukses di buat....',
                'data' : serializer.data
            }
            return Response(response, status= status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id, *args, **kwargs):
        table_resto_instance = self.get_object(id)
        if not table_resto_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data DOES NOT EXIST....',
                    'data' : {}
                }, status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'code' : request.data.get('code'),
            'name' : request.data.get('name'),
            'capacity' : request.data.get('capacity'),
            'table_status' : request.data.get('table_status'),
            'status' : request.data.get('status'),
        }
        serializer = TableRestoSerializers(instance=table_resto_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status' : status.HTTP_200_OK,
                'message' : 'Data sukses di update....',
                'data' :  serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, *args, **kwargs):
        table_resto_instance = self.get_object(id)
        if not table_resto_instance:
            return Response(
                {
                    'status' : status.HTTP_400_BAD_REQUEST,
                    'message' : 'Data DOES NOT EXIST....',
                    'data' : {}
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
        table_resto_instance.delete()            
        self.response = {
            'status' : status.HTTP_200_OK,
            'message' : 'Data sukse di hapus..'
        }
        return Response(self.response, status=status.HTTP_200_OK)
