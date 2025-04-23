from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from django.core.paginator import Paginator
from decimal import Decimal, InvalidOperation


@api_view(['POST'])
def add_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getAll(request):
    title = request.GET.get('title')
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    ordering = request.GET.get('ordering', 'id')  # default: order by ID
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))

    products = Product.objects.all()

    if title:
        products = products.filter(title__icontains=title)

    if category_id:
        products = products.filter(category_id=category_id)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if ordering in ['price', '-price', 'title', '-title', 'id', '-id']:
        products = products.order_by(ordering)

    paginator = Paginator(products, per_page)
    paginated_products = paginator.get_page(page)
    serializer = ProductSerializer(paginated_products, many=True)

    return Response({
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': page,
        'results': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_product_by_id(request, id):
    try:
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def edit_product(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_product(request, id):
    try:
        product = Product.objects.get(id=id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
