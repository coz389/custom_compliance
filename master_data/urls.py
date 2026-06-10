from django.urls import path
from master_data.views.city_views import CityCreateView, CityDetailView, CityListView
from master_data.views.country_views import CountryDropdownView
from master_data.views.state_views import StateDropdownView

urlpatterns = [
    path('country/list', CountryDropdownView.as_view(), name='country-list'),
    path('states/<int:country_id>', StateDropdownView.as_view(), name='state-list'),
    path('cities/list', CityListView.as_view(), name='city-list'),
    path('cities/add', CityCreateView.as_view(), name='city-create'),
    path('cities/<int:pk>', CityDetailView.as_view(), name='city-detail')
]
