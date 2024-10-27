import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_tracker_project.settings")
django.setup()

from attendance_manager.models import Person

def print_face_encodings():
    persons = Person.objects.all()
    for person in persons:
        print(f"Name: {person.name}")
        print(f"Encoding: {list(person.face_encoding)}\n")

if __name__ == "__main__":
    print_face_encodings()
