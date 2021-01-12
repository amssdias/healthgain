# HealthGain

This is a website where a user can keep track of what nutrition values he have been eating. This is mainly good use for someone who wants to build muscle or reduce weight, as it can make it easy to see if they reach their daily goals of nutrition.

There's a section as well with recipes where they can search for a new one and try it in their diet. The goal is for them to try new foods and always come back to look for more.

I decided to do this website as I like to workout and many people as well, we all have different goals, and the main problem to achieve is our diet. With this website it will be so much easier to track what we have been eating, if we exceeded and how far are we from our personal goals. I have added the recipes section so users once in a while can check for new types of foods to eat, and if not, the website is mainly simple so a user can simple track their nutrition values.

I believe my website have the expectations for this project as I have learned new skills in Django and in Javascript by myself. I had to use Django signals where everytime I create a user, a profile model for that user is created as well, changed the admin page a little bit, used ModelForms, so whenever a user submits if will update automatically in the database. I have done the password reset, but it's not functional as I didn't want to use a personal email. But I've tested with a real email.
In Javascript I mainly used loads of APIs that I have builted with Django, and manipulated the data, send different requests and with that I could make the webpage much more user friendly.

## Getting Started

### Prerequisites

  * Python - 3.8.4 or up
  * Django
 
### Installing

  * Download latest version of [Python](https://www.python.org/downloads/)
  
  Once installed open your terminal window and type:
  ```
  pip install django
  ```

### Run
 
 - Download the project, open terminal window on folder with 'manage.py' and type:
 ```
 python manage.py runserver
 ```
 

## Built with

 * [Django](https://www.djangoproject.com/) - Framework
 
## Skills learned

 * Templates and inheritance
 * Static files and images
 * DB Models and Admin panel
 * Database relationships
 * Database querys
 * Forms and ModelForm
 * Django signals
 * Flash Messages
 * Password reset
 * APIs
 * Sass
 
 ## Files created
 
 ### health/Forms.py
  In this file I created a Register form to display on my template, and a Profile form, so whenever a user wants to update his profile, it updates automatically it's model.
  
 ### health/Urls.py
  In this file, I have putted all my urls, even the API ones.
 
 ### Media folder
  This folder was created so whenever the admin user wants to put a new recipe to display on the website, It can upload an image and it will be saved on this folder.

