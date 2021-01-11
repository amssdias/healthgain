from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'health'

urlpatterns = [
    path('', views.main, name="main"),
    path('register', views.register_user, name="register"),
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),

    path('update-profile', views.update_profile, name='update_profile'),
    path('recipes', views.recipes, name="recipes"),
    path('dashboard', views.dashboard, name='dashboard'),
    path('add-food', views.food_list, name='food_list'),

    path('user/api/<str:user_id>', views.api_profile, name="api_profile"),
    path('recipes/api/<str:category>', views.api_recipes, name="api_recipes"),
    path('send_message/<str:user_id>', views.app_message, name="app_message"),
    path('food/<str:food_id>', views.api_food, name='api_food'),
    path('all-foods', views.api_all_foods, name='api_all_foods'),
    path('food/user/created/<str:user_id>', views.api_food_creator, name='food_creator'),

    # path('password_reset',
    #  auth_views.PasswordResetView.as_view(template_name='health/password_reset.html', 
    #                                         email_template_name='health/password_reset_email.html'),
    #   name='reset_password'),

    # path('reset_password_sent/', 
    # auth_views.PasswordResetDoneView.as_view(template_name='health/passoword_reset_sent.html'), 
    # name='password_reset_done'),

    # path('reset/<uidb64>/<token>/', 
    # auth_views.PasswordResetConfirmView.as_view(template_name='health/passoword_reset_form.html'), 
    # name='password_reset_confirm'),

    # path('reset_password_complete/', 
    # auth_views.PasswordResetCompleteView.as_view(template_name='health/passoword_reset_done.html'), 
    # name='password_reset_complete'),
]
