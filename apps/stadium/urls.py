from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.event_list, name='event_list'),
    path('join/', views.join_vip, name='join_vip'),
    path('book/<int:match_id>/', views.book_ticket, name='book_ticket'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
]