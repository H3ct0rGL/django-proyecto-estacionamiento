"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from tasks import views

urlpatterns = [
    path('admin/',admin.site.urls),
    # home
    path('',views.home,name='home'),
    path('home/',views.home,name='home'),
    # users
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('logout/',views.signout,name='logout'),
    # tasks
    path('tasks/',views.tasks,name='tasks'),
    path('tasks/completed/',views.tasks_completed,name='tasks_completed'),
    path('tasks/create/',views.create_tasks,name='create_tasks'),
    path('tasks/<int:tasks_id>/',views.tasks_detail,name='tasks_detail'),
    path('tasks/<int:tasks_id>/complete/',views.complete_tasks,name='complete_tasks'),
    path('tasks/<int:tasks_id>/delete/',views.delete_tasks,name='delete_tasks')
]
