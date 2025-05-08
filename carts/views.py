from django.shortcuts import render
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


def get_user_cart (user):
    cart , _ = Cart.objects.get_or_create(user=user)
    return cart

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart = get_user_cart(request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data ,status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_cart_item(request):
    cart = get_user_cart(request.user)
    serializer = CartItemSerializer(data = request.data)
    if serializer.is_valid():
        product = serializer.validated_data['product']
        quantity = serializer.validated_data('quantity',1)
        item , creted = CartItem.objects.get_or_create(cart=cart , product=product)
        if created:
            item.quantity = quantity
        else :
            item.quantity += quantity
        item.save()
        return Response(CartItemSerializer(item).data , status=status.HTTP_201_CREATED)
    return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_cart_item(request , item_id):
    cart = get_user_cart(request.user)
    try :
        item = cart.items.get(pk = item_id)
    except CartItem.DoesNotExist:
        return Response({'detail' : 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CartItemSerializer(item , data = request.data , partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def remove_cart_item(request , item_id):
    cart = get_user_cart(request.user)
    deleted ,_ = cart.items.filter(pk=item_id).delete()
    if deleted : 
        return Response({'detail' : 'Item deleted'} , status = status.HTTP_204_NO_CONTENT )
    else :
        return Response({'detail':'Item not found'}, status = status.HTTP_404_NOT_FOUND)
