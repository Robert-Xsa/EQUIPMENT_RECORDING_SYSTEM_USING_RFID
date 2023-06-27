from django.shortcuts import render, redirect, get_object_or_404, redirect

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .models import Equipment, Borrowing, RFID,Arduino_COM
import serial
from .models import Equipment, Student, RFID
from .forms import EquipmentForm, BorrowingForm, StudentForm
from datetime import date
from django.contrib import messages
import serial
from serial import SerialException
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm



def user_login(request):
    message = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin-dashboard')
        else:
            message = "Invalid username or password."
    return render(request, 'login.html', {'message': message})

def user_logout(request):
    logout(request)
    return redirect('login')

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})





@login_required
def admin_dashboard(request):
    students = Student.objects.all()
    context = {'students': students}
    return render(request, 'admin_dashboard.html', context)

def rfid_detection(request):
    try:
        # Set up the serial connection with the Arduino
        com = Arduino_COM.objects.latest('id').COM
        ser = serial.Serial(com, 9600)
        

        # Start listening for data from the Arduino
        while True:
            if ser.in_waiting > 0:
                # Read the data from the Arduino
                data = ser.readline().decode().strip()

                # Process the received RFID tag data
                RFID.objects.create(tag=data)

                # Print the received RFID tag
                print("Received RFID tag:", data)

    except SerialException:
        # Handle the exception when the Arduino connection fails
        print("Arduino connection failed. Make sure the Arduino is connected.")
        # You can add additional error handling or redirect to an error page

    # The code above will run indefinitely or handle the exception, so this line is unreachable
    return render(request, 'rfid.html')


##
def view_tag(request):
    # Retrieve the most recently scanned RFID tag
    recent_rfid = RFID.objects.latest('time') if RFID.objects.exists() else None

    return render(request, 'view_tag.html', {'recent_rfid': recent_rfid})

def add_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
    else:
        form = EquipmentForm()
    
    return render(request, 'add_equipment.html', {'form': form})



def equipment_list(request):
    equipment = Equipment.objects.all()
    return render(request, 'equipment_list.html', {'equipment': equipment})


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-dashboard')
    else:
        form = StudentForm()
    
    return render(request, 'add_student.html', {'form': form})



def borrow_equipment(request):
    if request.method == 'POST':
        # Get the selected equipment and student from the form
        equipment_id = request.POST['equipment']
        student_id = request.POST['student']

        # Create a new borrowing instance
        borrowing = Borrowing.objects.create(
            student_id=student_id,
            borrowed_date=date.today()
        )

        # Add the selected equipment to the borrowing instance
        borrowing.equipment.add(equipment_id)

        return redirect('borrowing_list')  # Redirect to the borrowing list page

    # Retrieve all equipment and students
    equipment = Equipment.objects.all()
    students = Student.objects.all()

    return render(request, 'borrow_equipment.html', {'equipment': equipment, 'students': students})


def borrowing_list(request):
    borrowings = Borrowing.objects.all()
    return render(request, 'borrowing_list.html', {'borrowings': borrowings})

def return_equipment(request, borrowing_id):
    borrowing = Borrowing.objects.get(id=borrowing_id)
    borrowing.returned_date = date.today()
    borrowing.save()
    return redirect('borrowing_list')

def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('admin-dashboard')

def delete_equipment(request, equipment_id):
    try:
        equipment = Equipment.objects.get(id=equipment_id)
        equipment.delete()
        messages.success(request, 'Equipment deleted successfully.')
    except Equipment.DoesNotExist:
        messages.error(request, 'Equipment not found.')
    
    return redirect('equipment_list')
def delete_rfid(request, rfid_id):
    rfid = get_object_or_404(RFID, id=rfid_id)
    if request.method == 'POST':
        rfid.delete()
        # Redirect to a success page or another relevant URL
        return redirect('view-tag')
    # Handle other HTTP methods if needed
    # Render a template or return a response for other cases
    return render(request, 'view_tag.html')


