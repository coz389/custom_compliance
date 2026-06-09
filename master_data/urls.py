from django.urls import path
from master_data.views import StatusListView,StatusDetailView,StatusCreateView

urlpatterns = [
    # Status
    path('status', StatusListView.as_view(), name='status_list_filter'),
    path('status/add', StatusCreateView.as_view(), name='status_create'),
    path('status/<int:pk>', StatusDetailView.as_view(), name='status_detail'),
]