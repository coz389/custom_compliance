from django.urls import path
from master_data.views import (
    StatusListView,StatusDetailView,StatusCreateView, CarrierTypeListView,CarrierTypeCreateView,CarrierTypeDetailView,
    CountryDropdownView, StateDropdownView,CityCreateView, CityDetailView, CityListView,TransportModeDropdownView,
    ContainerCreateView, ContainerDetailView, ContainerListView,
    EquipmentCreateView, EquipmentDetailView, EquipmentListView,
    EquipmentDropdownView,
    SeaportCreateView, SeaportDetailView, SeaportListView,
    CustomerCreateView, CustomerDetailView, CustomerListView, CustomerDropdownView,
    CompanyCreateView, CompanyDetailView, CompanyListView,
    CustomerDocAssocCreateView, CustomerDocAssocDetailView, CustomerDocAssocListView,
    DocumentTypeListView,DocumentTypeCreateView,DocumentTypeDetailView,DocumentTypeDropdownView
)

urlpatterns = [
    # Country City States
    path('country/list', CountryDropdownView.as_view(), name='country-list'),
    path('states/<int:country_id>', StateDropdownView.as_view(), name='state-list'),
    path('cities/list', CityListView.as_view(), name='city-list'),
    path('cities/add', CityCreateView.as_view(), name='city-create'),
    path('cities/<int:pk>', CityDetailView.as_view(), name='city-detail'),
    # Containers
    path('containers/list', ContainerListView.as_view(), name='container-list'),
    path('containers/add', ContainerCreateView.as_view(), name='container-create'),
    path('containers/<int:pk>', ContainerDetailView.as_view(), name='container-detail'),
    # Equipment
    path('equipment/list', EquipmentListView.as_view(), name='equipment-list'),
    path('equipment/add', EquipmentCreateView.as_view(), name='equipment-create'),
    path('equipment/<int:pk>', EquipmentDetailView.as_view(), name='equipment-detail'),
    path('equipment/dropdown', EquipmentDropdownView.as_view(), name='equipment-dropdown'),
    # Seaports
    path('seaports/list', SeaportListView.as_view(), name='seaport-list'),
    path('seaports/add', SeaportCreateView.as_view(), name='seaport-create'),
    path('seaports/<int:pk>', SeaportDetailView.as_view(), name='seaport-detail'),
    # Status
    path('status', StatusListView.as_view(), name='status_list_filter'),
    # path('status/add', StatusCreateView.as_view(), name='status_create'),
    path('status/<int:pk>', StatusDetailView.as_view(), name='status_detail'),
    # Carrier Types
    # path('carrier-types', CarrierTypeListView.as_view(), name='carrier_types_list_filter'),
    # path('carrier-types/add', CarrierTypeCreateView.as_view(), name='carrier_types_create'),
    # path('carrier-types/<int:pk>', CarrierTypeDetailView.as_view(), name='carrier_types_detail'),
    # Customers
    path('customers', CustomerListView.as_view(), name='customer_list_filter'),
    path('customers/add', CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>', CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/dropdown', CustomerDropdownView.as_view(), name='customer_dropdown'),
    # Companies
    path('companies', CompanyListView.as_view(), name='company_list_filter'),
    path('companies/add', CompanyCreateView.as_view(), name='company_create'),
    path('companies/<int:pk>', CompanyDetailView.as_view(), name='company_detail'),
    path('customer-companies', CustomerDropdownView.as_view(), name='customer_company_list'),
    # Customer Document Associations
    path('customer-document', CustomerDocAssocListView.as_view(), name='customer_doc_assoc_list'),
    path('customer-document/add', CustomerDocAssocCreateView.as_view(), name='customer_doc_assoc_create'),
    path('customer-document/<int:pk>', CustomerDocAssocDetailView.as_view(), name='customer_doc_assoc_detail'),
    #Document Management
    path('transport-modes/dropdown', TransportModeDropdownView.as_view(), name='transport_mode_list_filter'),
    path('document-types/dropdown', DocumentTypeDropdownView.as_view(), name='document_type_list_filter'),
    path('document-types', DocumentTypeListView.as_view(), name='document_type_list_filter'),
    path('document-types/add', DocumentTypeCreateView.as_view(), name='document_type_create'),
    path('document-types/<int:pk>', DocumentTypeDetailView.as_view(), name='document_type_detail'),
]

