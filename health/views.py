import json
from datetime import date, timedelta

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from .forms import RegisterForm, ProfileForm
from .models import Main_food, Profile_user, Daily_food, Recipes, Messages


# Main page
def main(request):

    if request.user.is_authenticated:
        # Get user logged
        user_logged = User.objects.get(pk=request.user.id)

        # Get todays day and get the day before
        tday = date.today()
        tdelta = timedelta(days=1)
        yesterday = tday - tdelta

        # Get foods from today and yesterday
        today_food = user_logged.consumed_food.filter(date_consumed=date.today())
        yesterday_food = user_logged.consumed_food.filter(date_consumed=yesterday)

        # Store results of each day into variables
        today_nutrition = {
            'date': tday,
            'calories': 0,
            'total_fat': 0,
            'carbs': 0,
            'fiber': 0,
            'protein':0
            }

        yesterday_nutrition = {
            'date': yesterday,
            'calories': 0,
            'total_fat': 0,
            'carbs': 0,
            'fiber': 0,
            'protein':0
            }

        for food in today_food:
            today_nutrition['calories'] += food.food.calories * food.weight / food.food.weight
            today_nutrition['total_fat'] += food.food.total_fat * food.weight / food.food.weight
            today_nutrition['carbs'] += food.food.carbs * food.weight / food.food.weight
            today_nutrition['fiber'] += food.food.fiber * food.weight / food.food.weight
            today_nutrition['protein'] += food.food.protein * food.weight / food.food.weight

        for food in yesterday_food:
            yesterday_nutrition['calories'] += food.food.calories * food.weight / food.food.weight
            yesterday_nutrition['total_fat'] += food.food.total_fat * food.weight / food.food.weight
            yesterday_nutrition['carbs'] += food.food.carbs * food.weight / food.food.weight
            yesterday_nutrition['fiber'] += food.food.fiber * food.weight / food.food.weight
            yesterday_nutrition['protein'] += food.food.protein * food.weight / food.food.weight

        context = {
            'today_food': today_nutrition,
            'yesterday_food': yesterday_nutrition
            }
        return render(request, "health/index.html", context)


    return render(request, "health/index.html")

# Register user
def register_user(request):

    if request.user.is_authenticated:
        return redirect('health:main')
    
    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            username    = form.cleaned_data['username']
            password    = form.cleaned_data['password']
            password_1  = form.cleaned_data['password_conf']
            email       = form.cleaned_data['email']
            weight      = form.cleaned_data['weight']
            height      = form.cleaned_data['height']

            # If passwords don't match
            if password != password_1:
                message = "Password does not match"
                context = {'form': RegisterForm(), 'message': message }
                return render(request, "health/register.html", context)
            
            # Check if username already exists
            check_user = User.objects.filter(username=username)
            check_email = User.objects.filter(email=email)

            if len(check_user) >= 1 or len(check_email) >= 1:
                message = "Username already exists, try other" if len(check_user) >= 1 else "Email already exists, try other"
                context = {'form': RegisterForm(), 'message': message }
                return render(request, "health/register.html", context)

            # Create User
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()

            profile_update = Profile_user.objects.get(user=user)
            profile_update.weight = weight
            profile_update.height = height
            profile_update.save()

            messages.success(request, 'Account was created for ' + user.email)

            return redirect('health:login')

    form = RegisterForm()
    context = {'form': form }
    return render(request, "health/register.html", context)

# Login user
def login_user(request):

    if request.user.is_authenticated:
        return redirect('health:main')

    if request.method == "POST":
        
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]

        # Check if user is in database
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect('health:main')
        else:
            return render(request, "health/login.html", {
                "message": "Invalid username and/or password."
            })

    else:
        return render(request, "health/login.html")

# Logout user
def logout_user(request):
    logout(request)
    return redirect('health:main')

# Display recipes
def recipes(request):

    if request.method == 'POST':
        search = request.POST['search']

        recipes = Recipes.objects.filter(name__startswith=search)
        print(recipes)
        context = { 'recipes': recipes }
        return render(request, "health/recipes.html", context)

    return render(request, "health/recipes.html")

# API for message
@csrf_exempt
def app_message(request, user_id):

    if request.method == 'POST':

        data = json.loads(request.body)

        user = User.objects.get(pk=user_id)
        message = Messages(user=user, message=data['message_app'])
        message.save()

        return JsonResponse({"message": "Email sent successfully."}, status=201)

# Add food to main food table
@login_required(login_url='login')
def food_list(request):

    if request.method == 'POST':
        category    = request.POST['category']
        name        = request.POST['name']
        brand       = request.POST['brand']
        calories    = request.POST['calories']
        total_fat   = request.POST['total_fat']
        carbs       = request.POST['carbs']
        fiber       = request.POST['fiber']
        protein     = request.POST['protein']

        user = User.objects.get(pk=request.user.id)
        add_ = Main_food(name=name, brand=brand, category=category, calories=calories, total_fat=total_fat, carbs=carbs, fiber=fiber, protein=protein, creator=user)
        add_.save()

        return render(request, 'health/food-list.html')


    return render(request, 'health/food-list.html')

# Show user stats
@login_required(login_url='login')
def dashboard(request):

    # Get user
    user_ = User.objects.get(pk=request.user.id)

    if request.method == 'POST':
        if 'add-food' in request.POST:

            food_user = request.POST['food']
            weight = request.POST['weight']

            food = Main_food.objects.get(pk=food_user)

            daily = Daily_food(user=user_, food=food, category=food.category, weight=weight)
            daily.save()

            messages.success(request, 'Food added to your daily intake')

            return redirect('health:dashboard')

        elif 'date_query' in request.POST:
            
            date_daily = request.POST['date']

            date_query = Daily_food.objects.filter(date_consumed=date_daily)

            date_query_nutrition = {
                'date': date_daily,
                'calories': 0,
                'total_fat': 0,
                'carbs': 0,
                'fiber': 0,
                'protein':0
            }

            for food in date_query:
                date_query_nutrition['calories'] += food.food.calories * food.weight / food.food.weight
                date_query_nutrition['total_fat'] += food.food.total_fat * food.weight / food.food.weight
                date_query_nutrition['carbs'] += food.food.carbs * food.weight / food.food.weight
                date_query_nutrition['fiber'] += food.food.fiber * food.weight / food.food.weight
                date_query_nutrition['protein'] += food.food.protein * food.weight / food.food.weight

            # print(date_query)
            
        elif 'update_food' in request.POST:

            food_id = request.POST['food-id']
            new_weight = request.POST['new_weight']

            food = Daily_food.objects.get(pk=food_id)
            food.weight = new_weight
            food.save()
            print(new_weight)


    # Get profile
    profile_user = Profile_user.objects.get(user=user_)

    # Get todays day and get the day before
    tday = date.today()

    # Get foods from today and yesterday
    today_food = user_.consumed_food.filter(date_consumed=date.today())

    # Store results of each day into variables
    today_nutrition = {
        'date': tday,
        'calories': 0,
        'total_fat': 0,
        'carbs': 0,
        'fiber': 0,
        'protein':0
        }

    for food in today_food:
        today_nutrition['calories'] += food.food.calories * food.weight / food.food.weight
        today_nutrition['total_fat'] += food.food.total_fat * food.weight / food.food.weight
        today_nutrition['carbs'] += food.food.carbs * food.weight / food.food.weight
        today_nutrition['fiber'] += food.food.fiber * food.weight / food.food.weight
        today_nutrition['protein'] += food.food.protein * food.weight / food.food.weight
        
    try:
        context = { 'today_food': today_nutrition, 'profile': profile_user, 'date_query':date_query, 'date_food': date_query_nutrition}
    except:
        context = { 'today_food': today_nutrition, 'profile': profile_user}
    
    return render(request, "health/dashboard.html", context) 

# Update Profile
@login_required(login_url='login')
def update_profile(request):

    user = Profile_user.objects.get(pk=request.user.profile.id)
    form = ProfileForm(instance=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('health:main')

    context = {'form': form}
    return render(request, 'health/update-profile.html', context)

# API Profile
@csrf_exempt
def api_profile(request, user_id):
    
    try:
        profile = Profile_user.objects.get(pk=user_id)
    except:
        return JsonResponse({"error": "User not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(profile.serialize(), safe=True)

    elif request.method == 'PUT':
        data = json.loads(request.body)
        food = Main_food.objects.get(pk=data['f_id'])

        if data['option'] == 'remove':
            profile.favourite_foods.remove(food)
        
        if data['option'] == 'add':
            profile.favourite_foods.add(food)

        return JsonResponse({'food': 'food updated!'})

    elif request.method == 'DELETE':
        data = json.loads(request.body)


        food = Main_food.objects.get(pk=data['food_id'])
        profile.favourite_foods.remove(food)
        food.delete()

        return JsonResponse({'food': 'food deleted from users list!'})
        
# API Recipes
def api_recipes(request,category):
    
    recipes = Recipes.objects.filter(category=category)

    if request.method == "GET":
        return JsonResponse([recipe.serialize() for recipe in recipes], safe=False)

# API single food
@login_required(login_url='login')
def api_food(request, food_id):

    food = Main_food.objects.get(pk=food_id)

    if request.method == 'GET':
        return JsonResponse(food.serialize(), safe=False)

# API all foods
@login_required(login_url='login')
def api_all_foods(request):

    foods = Main_food.objects.filter(Q(creator=None))

    if request.method == 'GET':
        return JsonResponse([food.serialize() for food in foods], safe=False)


# API for foods created by user
@login_required(login_url='login')
def api_food_creator(request, user_id):

    try:
        user_profile = Profile_user.objects.get(pk=user_id)
    except:
        return JsonResponse({"error": "User not found"}, status=404)

    user_ = User.objects.get(pk=user_profile.user.id)
    foods = Main_food.objects.filter(Q(creator=user_))

    if request.method == 'GET':
        return JsonResponse([food.serialize() for food in foods], safe=False)
