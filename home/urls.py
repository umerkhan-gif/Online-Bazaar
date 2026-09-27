from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'products/',
        views.products,
        name='products'
    ),

    path(
        'product/<int:id>/',
        views.product_detail,
        name='product_detail'
    ),

    path(
        'add-product/',
        views.showformdata,
        name='add_product'
    ),

    path(
        'search/',
        views.search,
        name='search'
    ),

    path(
        'categories/',
        views.categories,
        name='categories'
    ),

    path(
        'category/<str:category>/',
        views.category_products,
        name='category_products'
    ),

    path(
        'cart/',
        views.cart,
        name='cart'
    ),

    path(
        'cart/add/<int:id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/remove/<int:id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'cart/increase/<int:id>/',
        views.increase_quantity,
        name='increase_quantity'
    ),

    path(
        'cart/decrease/<int:id>/',
        views.decrease_quantity,
        name='decrease_quantity'
    ),

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
        'order-success/<int:order_id>/',
        views.order_success,
        name='order_success'
    ),

    path(
        'my-orders/',
        views.my_orders,
        name='my_orders'
    ),

    path(
        'signup/',
        views.signup,
        name='signup'
    ),

    path(
        'login/',
        views.user_login,
        name='login'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),

    path('contact/', views.contact, name='contact'),
    path('buy-now/<int:id>/', views.buy_now, name='buy_now'),
    path('buy-now-checkout/', views.buy_now_checkout, name='buy_now_checkout'),
]
