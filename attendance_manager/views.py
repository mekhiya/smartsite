from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from attendance_manager.models import UnregisteredFaces, Person, AttendanceRecord
from attendance_manager.tasks import process_attendance
from .utils import get_image_url

def handle_attendance(request):
    """
    Handles attendance by initiating the face processing task.
    Expects image_key, bucket_name, device_id, and site_id as GET parameters.
    """
    image_key = request.GET.get('image_key')
    bucket_name = request.GET.get('bucket_name')
    device_id = request.GET.get('device_id')
    site_id = request.GET.get('site_id')

    # Validate required parameters
    if not all([image_key, bucket_name, device_id, site_id]):
        return JsonResponse({'status': 'error', 'message': 'Missing required parameters'}, status=400)

    # Trigger the asynchronous task
    task = process_attendance.delay(image_key, bucket_name, device_id, site_id)
    return JsonResponse({'status': 'success', 'task_id': task.id})

def view_unregistered_faces(request):
    """
    Displays all unregistered faces for review by architects or administrators.
    Includes dynamically generated signed image URLs for each face.
    """
    unregistered_faces = UnregisteredFaces.objects.all()
    for face in unregistered_faces:
        face.image_url = get_image_url(face.image_key)  # Generate signed URL dynamically
    return render(request, 'attendance_manager/unregistered_faces.html', {'unregistered_faces': unregistered_faces})

def register_person(request):
    """
    Handles the registration of a person from unregistered faces.
    Moves the selected unregistered face to the Person table.
    """
    if request.method == 'POST':
        image_key = request.POST['image_key']
        name = request.POST['name']
        department = request.POST['department']

        try:
            # Fetch the unregistered face
            unregistered_face = UnregisteredFaces.objects.get(image_key=image_key)

            # Create a new person in the Person table
            person = Person.objects.create(
                name=name,
                face_encoding=unregistered_face.face_encoding,
                department=department
            )

            # Update AttendanceRecord entries to link to the new Person
            AttendanceRecord.objects.filter(unregistered_face=unregistered_face).update(person=person, unregistered_face=None)

            # Delete the unregistered face entry
            unregistered_face.delete()

            # Display a success message
            messages.success(request, f"Person '{name}' successfully registered.")
        except UnregisteredFaces.DoesNotExist:
            messages.error(request, "Unregistered face not found.")
        except Exception as e:
            messages.error(request, f"Error registering person: {e}")

    return redirect('view_unregistered_faces')
