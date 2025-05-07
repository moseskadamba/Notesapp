from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Note
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings

# Create your views here.

def dashboard(request):
    return render(request, "notes/dashboard.html", {'MEDIA_URL': settings.MEDIA_URL})

@login_required
def search_notes(request):
    query = request.GET.get('q', '')  # Get search query
    notes = Note.objects.filter(user=request.user)  # Show only user's notes

    if query:
        notes = notes.filter(title__icontains=query) | notes.filter(content__icontains=query)

    return render(request, 'notes/note_list.html', {'notes': notes})

@login_required
def home(request):
    """ Renders the home page with all notes initially """
    notes = Note.objects.filter(user=request.user)  # Fetch all notes for the logged-in user
    return render(request, 'notes/home.html', {'notes': notes})

@login_required
def add_note(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Note.objects.create(user=request.user, title=title, content=content)  # Link note to user

        messages.success(request, "Your note has been added successfully! ✅")

        return redirect('home')
    return render(request, 'notes/add_note.html')

@login_required
def delete_note(request, note_id):
    note = Note.objects.get(id=note_id, user=request.user)  # Ensure users can only delete their own notes
    note.delete()
    return redirect('home')

@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)  # Ensure user can only edit their own notes

    if request.method == 'POST':
        note.title = request.POST['title']
        note.content = request.POST['content']
        note.save()

    return render(request, 'notes/edit_note.html', {'note': note})

def auto_save_note(request):
    if request.method == "POST":
        note_id = request.POST.get("note_id")
        title = request.POST.get("title")
        content = request.POST.get("content")

        try:
            note = Note.objects.get(id=note_id, user=request.user)
            note.title = title
            note.content = content
            note.save()
            return JsonResponse({"status": "success"})
        except Note.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Note not found"})
    
    return JsonResponse({"status": "error", "message": "Invalid request"})

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user automatically
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'notes/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'notes/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')