
from django.urls import path
from . import views



app_name = "plants"


urlpatterns = [
    path('add/', views.plants_add_view, name='plants_add_view'),
    path('detail/<int:plant_id>/', views.plants_detail_view, name='plants_detail_view'),
    path('update/<int:plant_id>/', views.plants_update_view, name='plants_update_view'),
    path('delete/<int:plant_id>/', views.plants_delet_view, name='plants_delet_view'),
    path('search/', views.plants_search_view, name='plants_search_view'),
    path('allPlant/', views.plants_list_view, name='plants_list_view'),
    path('add/review/<int:plant_id>/', views.add_review_view, name='add_review_view'),
    path("country/<int:country_id>/", views.plants_country_view, name="plants_country_view"),



 ]