from django.urls import path
from . import views

app_name = 'planner'

urlpatterns = [
    # READ
    path('', views.index, name='index'),
    # CREATE
    path('add/', views.add_event, name='add_event'),
    # EDIT
    path('edit/<int:pk>', views.edit_event, name="edit_event"),
    # DELETE
    path('delete/<int:pk>', views.delete_view, name='delete'),
    # Conditions
    path('conditions/', views.conditions_view, name="conditions"),
    # Contact
    path('contact/', views.contact_view, name='contact'),
    # Messages
    path('message/<int:pk>', views.display_message, name="display_message"),
    # Manage Event Engineers
    # path('event/<int:event_pk>/edit-engineer/',
    #      views.manage_event_engineer, name='manage_event_engineer')
]
