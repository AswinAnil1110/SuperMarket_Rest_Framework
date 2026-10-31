from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from Store.models import ProductDb,OrderDb
from Store.serializers import Product_Serializer,Order_Serializer

# Create your views here.
class ProductListCreateView(APIView):
    def get(self,request):
        qs = ProductDb.objects.all()
        serializer_instance = Product_Serializer(qs,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance = Product_Serializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"Message":"Product Added Successfully"})
        else:
            return Response(data=serializer_instance.errors)

class ProductRetriveUpdateDeleteView(APIView):
    def get(self,request,pk):
        qs = get_object_or_404(ProductDb,id=pk)
        serializer_instance = Product_Serializer(qs)
        return Response(data=serializer_instance.data)

    def put(self,request,pk):
        form_data = request.data
        product_object = get_object_or_404(ProductDb,id=pk)
        serializer_instance = Product_Serializer(data=form_data,instance=product_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"Message":"Product Updated Successfully"})
        else:
            return Response(data=serializer_instance.errors)
    
    def delete(self,request,pk):
        product_object = get_object_or_404(ProductDb,id=pk)
        product_object.delete()
        return Response({"Message":"Product Deleted Successfully"})
    
class OrderListCreateView(APIView):
    def get(self,request):
        qs = OrderDb.objects.all()
        serializer_instance = Order_Serializer(qs,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        form_data = request.data
        serializer_instance = Order_Serializer(data=form_data)
        if serializer_instance.is_valid():
            actual_data = serializer_instance.validated_data
            product = actual_data.get('product_id')
            quantity = actual_data.get('quantity')
            if quantity <=0 :
                return Response({"Message":"Quantity should be greater than zero"})
            if product.stock < quantity:
                return Response({"Message":"Insufficient Stock"})
            unit_price = product.price
            total_amount = unit_price * quantity
            product.stock -= quantity
            product.save()
            serializer_instance.save(unit_price=unit_price,total_amount=total_amount)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class OrderRetriveUpdateDeleteView(APIView):
    def get(self,request,pk):
        order_object = get_object_or_404(OrderDb,id=pk)
        serializer_instance = Order_Serializer(order_object)
        return Response(data=serializer_instance.data) 
    
    def put(self,request,pk):
        form_data = request.data
        order_object = get_object_or_404(OrderDb,id=pk)
        serializer_instance = Order_Serializer(data=form_data,instance=order_object)
        if serializer_instance.is_valid():
            actual_data = serializer_instance.validated_data
            old_product = order_object.product_id
            old_quantity = order_object.quantity
            new_product = actual_data.get('product_id',old_product)
            new_quantity = actual_data.get('quantity',old_quantity)
            if new_quantity <=0:
                return Response({"Message":"Quantity should be greater than zero"})
            if old_product.id == new_product.id:
                difference = new_quantity - old_quantity
                if difference > 0:
                    if new_product.stock < difference:
                        return Response({"Message":"Insufficient Stock"})
                    new_product.stock -= difference
                    new_product.save()
                elif difference < 0:
                    new_product.stock += abs(difference)
                    new_product.save()
            else:
                if new_product.stock < new_quantity:
                    return Response({"Message":"Insufficient stock"})
                old_product.stock += old_quantity
                old_product.save()
                new_product.stock -= new_quantity
                new_product.save()
            unit_price = new_product.price
            total_amount = unit_price * new_quantity
            serializer_instance.save(unit_price=unit_price,total_amount=total_amount)
            return Response(data=serializer_instance.data)
        return Response(data=serializer_instance.errors)
    
    def delete(self,request,pk):
        order_object = get_object_or_404(OrderDb,id=pk)
        product = order_object.product_id
        quantity = order_object.quantity
        product.stock += quantity
        product.save()
        order_object.delete()
        return Response({"Message":"Order Deleted Successfully"})

class OrderEvaluate(APIView):
    def put(self,request,pk):
        order_object = get_object_or_404(OrderDb,id=pk)
        form_data = request.data
        OrderDb.objects.filter(id=pk).update(**form_data)
        return Response({"Message":"Order Updated Successfully",
                        "Order_id":order_object.id,
                        "Ststus":order_object.status})