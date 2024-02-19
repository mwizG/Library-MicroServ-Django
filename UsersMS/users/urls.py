from django.urls import path
from .views import UserSignUp, UserLogin, UserList, UserDetail

app_name='users'
urlpatterns = [
    path('signup/', UserSignUp.as_view(), name='signup'),
    path('login/', UserLogin.as_view(), name='login'),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
]

'''
Endpoints:
User Sign Up:
Endpoint: POST /users/signup/
Parameters: email, password, username
Headers: None
Body (JSON): { "email": "example@example.com", "password": "your_password", "username": "your_username" }


#####
User Login:
Endpoint: POST /users/login/
Parameters: email, password
Headers: Auth
Body (JSON): { "email": "example@example.com", "password": "your_password","username":"yourusername"}

#####
View Users (Admin-Only):
Endpoint: GET /users/users/
Parameters: None
Headers: Authorization: Token your_token_here
Body: None

#####
User Detail:
Endpoint: GET /users/users/<id>/
Parameters: id
Headers: Authorization: Token your_token_here
Body: None

##########
Update User:
Endpoint: PUT /users/users/<id>/
Parameters: id
Headers: Authorization: Token your_token_here
Body (JSON): { "email": "new_email@example.com", "password": "new_password", "username": "new_username" }

######
Delete User:
Endpoint: DELETE /users/users/<id>/
Parameters: id
Headers: Authorization: Token your_token_here
Body: None

########

Additional Details:
Headers: For endpoints that require authentication,
you'll need to include the Authorization header with the value Token your_token_here, 
where your_token_here is the token obtained after user login.
Testing on Postman: Use the provided endpoints with the appropriate parameters and headers.
Make sure to replace placeholders like your_token_here, your_username, your_password, example@example.com, etc., with actual values.
'''