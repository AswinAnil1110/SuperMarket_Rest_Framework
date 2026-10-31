from rest_framework import serializers
from Store.models import ProductDb,OrderDb

class Product_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDb
        fields = "__all__"

class Order_Serializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDb
        fields = "__all__"
        read_only_fields = ["unit_price","order_date","total_amount"]