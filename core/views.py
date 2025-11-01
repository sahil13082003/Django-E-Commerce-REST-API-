from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from .permissions import *
from datetime import datetime

# Authentication Views
class RegisterView(views.APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.profile.role,
                'message': 'User registered successfully.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.profile.role
                }
            })
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        profile = request.user.profile
        return Response({
            'user': UserSerializer(request.user).data,
            'profile': UserProfileSerializer(profile).data
        })
    
    def put(self, request):
        profile = request.user.profile
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'user': UserSerializer(request.user).data,
                'profile': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateAdminView(views.APIView):
    permission_classes = [IsSuperAdmin]
    
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role', 'ADMIN')
        
        if role not in ['ADMIN', 'SUPER_ADMIN']:
            return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user, role=role)
        
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': role,
            'message': 'Admin account created successfully.'
        }, status=status.HTTP_201_CREATED)

class ListUsersView(views.APIView):
    permission_classes = [IsSuperAdmin]
    
    def get(self, request):
        users = User.objects.all()
        data = []
        for user in users:
            data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.profile.role if hasattr(user, 'profile') else 'N/A'
            })
        return Response(data)

# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrSuperAdmin()]
        return [AllowAny()]

# Brand ViewSet
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrSuperAdmin()]
        return [AllowAny()]

# Product ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'add_variant', 'add_image']:
            return [IsAdminOrSuperAdmin()]
        return [AllowAny()]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_variant(self, request, pk=None):
        product = self.get_object()
        serializer = ProductVariantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def add_image(self, request, pk=None):
        product = self.get_object()
        image = request.FILES.get('image')
        if image:
            ProductImage.objects.create(product=product, image_url=image)
            return Response({'message': 'Image uploaded successfully'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

# Cart Views
class CartView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddToCartView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        variant_id = request.data.get('product_variant')
        quantity = request.data.get('quantity', 1)
        
        try:
            variant = ProductVariant.objects.get(id=variant_id)
        except ProductVariant.DoesNotExist:
            return Response({'error': 'Product variant not found'}, status=status.HTTP_404_NOT_FOUND)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_variant=variant)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()
        
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UpdateCartItemView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            quantity = request.data.get('quantity')
            if quantity:
                cart_item.quantity = int(quantity)
                cart_item.save()
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

class RemoveCartItemView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.delete()
            return Response({'message': 'Item removed'}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

# Order Views
class CreateOrderView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        address_id = request.data.get('address')
        coupon_code = request.data.get('coupon_code')
        
        try:
            address = Address.objects.get(id=address_id, user=request.user)
        except Address.DoesNotExist:
            return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Calculate totals
        total_amount = sum(item.subtotal for item in cart.items.all())
        discount = 0
        
        # Apply coupon if provided
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, expiry_date__gte=datetime.now())
                if total_amount >= coupon.min_amount:
                    if coupon.discount_type == 'PERCENT':
                        discount = (total_amount * coupon.value) / 100
                    else:
                        discount = coupon.value
            except Coupon.DoesNotExist:
                pass
        
        grand_total = total_amount - discount
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_amount=total_amount,
            discount=discount,
            grand_total=grand_total
        )
        
        # Create order items and reduce stock
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product_variant=item.product_variant,
                quantity=item.quantity,
                price=item.product_variant.price
            )
            # Reduce stock
            item.product_variant.stock -= item.quantity
            item.product_variant.save()
        
        # Clear cart
        cart.items.all().delete()
        
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ListOrdersView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if hasattr(request.user, 'profile') and request.user.profile.role in ['ADMIN', 'SUPER_ADMIN']:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=request.user)
        
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderDetailView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, order_id):
        try:
            if hasattr(request.user, 'profile') and request.user.profile.role in ['ADMIN', 'SUPER_ADMIN']:
                order = Order.objects.get(id=order_id)
            else:
                order = Order.objects.get(id=order_id, user=request.user)
            
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

class UpdateOrderStatusView(views.APIView):
    permission_classes = [IsAdminOrSuperAdmin]
    
    def put(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            order_status = request.data.get('order_status')
            
            if order_status:
                order.order_status = order_status
                order.save()
            
            return Response({
                'id': order.id,
                'order_status': order.order_status,
                'updated_by': request.user.username
            })
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

class ApproveOrderView(views.APIView):
    permission_classes = [IsAdminOrSuperAdmin]
    
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            order.order_status = 'APPROVED'
            order.approved_by = request.user
            order.save()
            
            # Create notification
            Notification.objects.create(
                user=order.user,
                title='Order Approved',
                message=f'Your order #{order.id} has been approved.'
            )
            
            return Response({'message': 'Order approved successfully'})
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

# Review Views
class CreateReviewView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteReviewView(views.APIView):
    permission_classes = [IsAdminOrSuperAdmin]
    
    def delete(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
            review.delete()
            return Response({'message': 'Review deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

# Discount and Coupon Views
class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.filter(is_active=True)
    serializer_class = DiscountSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrSuperAdmin()]
        return [AllowAny()]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrSuperAdmin()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def validate_coupon(self, request):
        code = request.query_params.get('code')
        try:
            coupon = Coupon.objects.get(code=code, expiry_date__gte=datetime.now())
            serializer = CouponSerializer(coupon)
            return Response(serializer.data)
        except Coupon.DoesNotExist:
            return Response({'error': 'Invalid or expired coupon'}, status=status.HTTP_404_NOT_FOUND)

# Notification Views
class ListNotificationsView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        notifications = request.user.notifications.all().order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

class MarkNotificationReadView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return Response({'message': 'Notification marked as read'})
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)

class SendNotificationView(views.APIView):
    permission_classes = [IsSuperAdmin]
    
    def post(self, request):
        user_id = request.data.get('user')
        title = request.data.get('title')
        message = request.data.get('message')
        
        try:
            user = User.objects.get(id=user_id)
            notification = Notification.objects.create(
                user=user,
                title=title,
                message=message
            )
            serializer = NotificationSerializer(notification)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# Address ViewSet
class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)