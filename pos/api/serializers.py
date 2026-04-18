from rest_framework import serializers
from pos_app.models import ( TableResto )

class TableRestoSerializers(serializers.ModelSerializer):
    class Meta:
        model = TableResto
        fields = ('id', 'code', 'name', 'capacity', 'table_status', 'status',)