from django.contrib import admin

# Register your models here.
from equipments.models import *
import openpyxl
from django.contrib import messages
class BorrowingAdmin(admin.ModelAdmin):
    search_fields = ['student__registration_number', 'equipment__tag']


admin.site.register(Borrowing, BorrowingAdmin)
admin.site.register(Equipment)
admin.site.register(RFID)
admin.site.register(Student)













