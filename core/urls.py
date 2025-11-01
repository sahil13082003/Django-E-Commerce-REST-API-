from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r"categories", views.CategoryViewSet)
router.register(r"brands", views.BrandViewSet)
router.register(r"products", views.ProductViewSet)
router.register(r"discounts", views.DiscountViewSet)
router.register(r"coupons", views.CouponViewSet)
router.register(r"addresses", views.AddressViewSet, basename="address")

urlpatterns = [
    path("", include(router.urls)),

    path("auth/register/", views.RegisterView.as_view(), name="register"),
    path("auth/login/", views.LoginView.as_view(), name="login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/profile/", views.ProfileView.as_view(), name="profile"),
    path("auth/create-admin/", views.CreateAdminView.as_view(), name="create-admin"),
    path("auth/users/", views.ListUsersView.as_view(), name="list-users"),

    # Cart
    path("cart/", views.CartView.as_view(), name="view-cart"),
    path("cart/add/", views.AddToCartView.as_view(), name="add-to-cart"),
    path("cart/update/<int:item_id>/", views.UpdateCartItemView.as_view(), name="update-cart-item"),
    path("cart/remove/<int:item_id>/", views.RemoveCartItemView.as_view(), name="remove-cart-item"),
    
    # Orders
    path("orders/create/", views.CreateOrderView.as_view(), name="create-order"),
    path("orders/", views.ListOrdersView.as_view(), name="list-orders"),
    path("orders/<int:order_id>/", views.OrderDetailView.as_view(), name="order-detail"),
    path("orders/<int:order_id>/update-status/", views.UpdateOrderStatusView.as_view(), name="update-order-status"),
    path("orders/<int:order_id>/approve/", views.ApproveOrderView.as_view(), name="approve-order"),

    # Reviews
    path("products/<int:product_id>/reviews/", views.CreateReviewView.as_view(), name="create-review"),
    path("reviews/<int:review_id>/", views.DeleteReviewView.as_view(), name="delete-review"),

    # Notifications
    path("notifications/", views.ListNotificationsView.as_view(), name="list-notifications"),
    path("notifications/<int:notification_id>/mark-read/", views.MarkNotificationReadView.as_view(), name="mark-notification-read"),
    path("notifications/send/", views.SendNotificationView.as_view(), name="send-notification"),
]
