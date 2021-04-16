from django.urls import path
from.import views

urlpatterns = [
    path('',views.index),
    path('register',views.register),

    path('login',views.login),


    path('success',views.output),
    path('logout',views.logout),

    path('<url>',views.catch_all),

]
