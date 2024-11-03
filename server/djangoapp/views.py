# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime
from .populate import initiate  # Import the initiate function to populate data

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            # Parse JSON body to extract username and password
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            
            # Authenticate user credentials
            user = authenticate(username=username, password=password)
            if user is not None:
                # Log the user in if credentials are valid
                login(request, user)
                response_data = {"userName": username, "status": "Authenticated"}
            else:
                # If credentials are invalid
                response_data = {"userName": username, "status": "Authentication Failed"}
                
        except json.JSONDecodeError:
            # Handle JSON parsing error
            response_data = {"error": "Invalid JSON data"}
            logger.error("Invalid JSON received in login request.")
            
    else:
        # Respond with an error if the method is not POST
        response_data = {"error": "POST method required"}
    
    return JsonResponse(response_data)
   

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Log out the user if they are authenticated
    if request.user.is_authenticated:
        logout(request)
        response_data = {"status": "Logged out successfully"}
        logger.info("User logged out successfully.")
    else:
        # User was not authenticated
        response_data = {"status": "User is not logged in"}
        logger.warning("Logout request made by a non-authenticated user.")
    
    return JsonResponse(response_data)


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    # Only proceed if the request method is POST
    if request.method == "POST":
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            email = data.get('email')

            # Check if the username or email already exists
            username_exist = User.objects.filter(username=username).exists()
            email_exist = User.objects.filter(email=email).exists()

            if username_exist:
                return JsonResponse({"userName": username, "error": "Username already taken"})
            elif email_exist:
                return JsonResponse({"email": email, "error": "Email already registered"})

            # Create and save the new user
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )

            # Log in the newly created user
            login(request, user)

            # Return a JSON response confirming successful registration and login
            return JsonResponse({"userName": username, "status": "Authenticated"})

        except json.JSONDecodeError:
            # Handle JSON parsing error
            logger.error("Invalid JSON received in registration request.")
            return JsonResponse({"error": "Invalid JSON data"})
        
    # If the request method is not POST
    return JsonResponse({"error": "POST method required"})


# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
def get_dealer_reviews(request, dealer_id):
    # If dealer ID has been provided
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{str(dealer_id)}"
        reviews = get_request(endpoint)

        # Analyze sentiments for each review
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)  # Optional: print response for debugging
            review_detail['sentiment'] = response['sentiment']  # Add sentiment to review details
        
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{str(dealer_id)}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Create a `add_review` view to submit a review
# def add_review(request):
def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})
# ...
# list of cars
def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if (count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })
    return JsonResponse({"CarModels": cars})
