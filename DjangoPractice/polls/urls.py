from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginPage, name="login" ),
    path('logout/', views.logoutUser, name="logout" ),
    path('register/', views.RegisterPage, name="register" ),

    path('', views.home, name="home"),
    path('room/<str:pk>', views.room, name="room"),

    path('createroom/', views.Createroom, name="create-room"),
    path('updateroom/<str:pk>', views.updateRoom, name="update-room"),
    path('deleteroom/<str:pk>', views.DeleteRoom, name="delete-room"),
    path('delete-msg/<str:pk>', views.DeleteMsg, name="delete-msg"),

    path('profile/<str:pk>', views.userProfile, name="user-profile"),

]