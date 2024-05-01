app_name = 'index'
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('searchview/',views.searchview,name="search"),
    # path('index/', views.elcetronic, name='electronic'),
    path('buypage/<int:item_id>/', views.buypage, name='buypage'),
     path('category/<str:name>/', views.category_view, name='categoryview'),
    path('uploaditem/', views.uploaditem, name='uploaditem'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('chat/<int:id>/', views.chat_view, name='chat'),
    path('myprofile/', views.my_profile, name='my_profile'),
    path('delete/<int:id>/', views.deleteitem, name='delete_item'),
    path('wishlist/<int:id>/', views.wishlist_item, name='wishlist_item'),
    path('items/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('new-message/',views.new_message,name="new_message"),
    path('wishlist/',views.wishlist_view,name="wishlist_view"),
    path('w_delete/<int:id>/', views.w_deleteitem, name='w_delete_item'),
    path('buy-now/',views.buynow,name='buy'),
    path('buynow/',views.buynow,name='buy'),

    
    # path('razorpayView/',views.razorpayView,name='razorpayView'),
    # path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('orderSuccessView/',views.successview,name='orderSuccessView'),
    path('my-order/',views.myorder,name='myorder'),
    path('paypal-payment/', views.paypal_payment, name='paypal_payment'),
    path('paypal-payment/success/', views.paypal_payment_success, name='paypal_payment_success'),
    path('paypal-payment/cancel/', views.paypal_payment_cancel, name='paypal_payment_cancel'),
 


]
