from django.urls import path
from equipments import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user_signup/', views.user_signup, name='signup'),
    path('admin-dashboard', views.admin_dashboard, name='admin-dashboard'),
    path('return_equipment/', views.return_equipment, name='return_equipment'),
    path('rfid_detection/', views.rfid_detection, name='rfid_detection'),
    path('view-tag/', views.view_tag, name='view-tag'),
    path('borrow/', views.borrow_equipment, name='borrow-equipment'),
    path('add-equipment/', views.add_equipment, name='add-equipment'),
    path('add-student/', views.add_student, name='add-student'),
    path('equipment-list/', views.equipment_list, name='equipment_list'),
    path('borrow_equipment/', views.borrow_equipment, name='borrow_equipment'),
    path('borrowings/', views.borrowing_list, name='borrowing_list'),
    path('equipments/return_equipment/<int:borrowing_id>/', views.return_equipment, name='return_equipment'),
    path('add_student/', views.add_student, name='add_student'),
    path('students/<int:student_id>/delete/', views.delete_student, name='delete_student'),
    path('equipment/delete/<int:equipment_id>/', views.delete_equipment, name='delete_equipment'),
    path('delete_rfid/<int:rfid_id>/', views.delete_rfid, name='delete_rfid'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






