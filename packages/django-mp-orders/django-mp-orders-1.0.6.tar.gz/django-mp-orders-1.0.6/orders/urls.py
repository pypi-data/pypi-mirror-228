
from django.urls import path

from orders import views


app_name = 'orders'


urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),

    path('history/', views.get_history, name='history'),

    path('resend/<int:order_id>', views.resend_new_order_notifications,
         name='resend-notifications'),

    path('render-email/<int:order_id>', views.render_new_order_email,
         name='render-email'),

    path('<str:order_hash>/success/', views.success, name='success')
]
