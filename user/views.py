from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Pet, AdoptionRequest,User
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

#home page
def home(request):
    approved_pets = AdoptionRequest.objects.filter(status='Approved').values_list('pet_id', flat=True)
    pets = Pet.objects.exclude(id__in=approved_pets)
    return render(request, 'user/home.html', {'pets': pets})


#user registration
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('user_login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})


#user login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and not user.is_admin:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'user/login.html')

    
#user logout
def user_logout(request):
    logout(request)
    return redirect('home')


#user_dashboard
@login_required
def dashboard(request):
    # Get IDs of pets already approved for adoption
    approved_pet_ids = AdoptionRequest.objects.filter(
        status='approved' 
    ).values_list('pet_id', flat=True)

    # Fetch available pets excluding approved ones
    pets = Pet.objects.filter(available=True).exclude(id__in=approved_pet_ids)

    # Get search filters
    name_query = request.GET.get('name', '')
    breed_query = request.GET.get('breed', '')
    type_query = request.GET.get('pet_type', '')
    age_query = request.GET.get('age', '')

    # Apply search filters
    if name_query:
        pets = pets.filter(name__icontains=name_query)
    if breed_query:
        pets = pets.filter(breed__icontains=breed_query)
    if type_query:
        pets = pets.filter(pet_type__icontains=type_query)
    if age_query:
        pets = pets.filter(age__icontains=age_query)

    # Get current user's adoption requests
    user_requests = AdoptionRequest.objects.filter(user=request.user)
    request_status = {req.pet_id: req.status for req in user_requests}

    # Prepare list with status
    pets_with_status = [
        {'pet': pet, 'status': request_status.get(pet.id)}
        for pet in pets
    ]

    context = {
        'pets_with_status': pets_with_status,
        'name_query': name_query,
        'breed_query': breed_query,
        'type_query': type_query,
        'age_query': age_query,
    }
    return render(request, 'user/dashboard.html', context)


#adoption request from user
@login_required
def request_adoption(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    AdoptionRequest.objects.create(user=request.user, pet=pet)
    messages.success(request, f'Adoption request for {pet.name} submitted!')
    return redirect('dashboard')


#cancel adoptation before approving
@login_required
def cancel_adoption(request, pet_id):
    try:
        adoption_request = AdoptionRequest.objects.get(user=request.user, pet_id=pet_id, status="Pending")
        adoption_request.delete()  # or update status to "Cancelled" if you want history
        messages.success(request, "Adoption request cancelled.")
    except AdoptionRequest.DoesNotExist:
        messages.error(request, "No pending request found to cancel.")
    return redirect('dashboard')


#adoption history
@login_required
def adoption_history(request):
    requests = AdoptionRequest.objects.filter(user=request.user).order_by('-request_date')
    context = {
        'requests': requests
    }
    return render(request, 'user/adoption_history.html', context)


#pet details from adoption history
def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'user/pet_detail.html', {'pet': pet})
