from .status_view import StatusListView, StatusCreateView,StatusDetailView
from .carrier_type_view import CarrierTypeListView, CarrierTypeCreateView,CarrierTypeDetailView
from .city_views import CityCreateView, CityDetailView, CityListView
from .container_views import ContainerCreateView, ContainerDetailView, ContainerListView
from .equipment_views import EquipmentCreateView, EquipmentDetailView, EquipmentListView
from .dropdown_views import CountryDropdownView, EquipmentDropdownView, StateDropdownView, CustomerDropdownView, TransportModeDropdownView,CustomerCompaniesDropdownView
from .seaport_views import SeaportCreateView, SeaportDetailView, SeaportListView
from .customer_views import CustomerCreateView, CustomerDetailView, CustomerListView
from .company_views import CompanyCreateView, CompanyDetailView, CompanyListView
from .customer_doc_assoc_views import CustomerDocAssocCreateView, CustomerDocAssocDetailView, CustomerDocAssocListView
from .document_type_view import DocumentTypeListView,DocumentTypeCreateView,DocumentTypeDetailView,DocumentTypeDropdownView
from .transport_mode_view import TransportModeListView
from .carrier_views import CarrierCreateView, CarrierDetailView, CarrierListView
from .customer_lsp_assoc_views import CustomerLspAssocCreateView, CustomerLspAssocDetailView, CustomerLspAssocListView
from .carrier_contact_views import CarrierContactCreateView, CarrierContactDetailView, CarrierContactListView
from .inspection_area_views import InspectionAreaListView,InspectionAreaCreateView,InspectionAreaDetailView
from .custom_officer_shift_views import CustomsOfficerShiftListView,CustomsOfficerShiftCreateView,CustomsOfficerShiftDetailView

__all__=[
    #Status Views
    'StatusListView','StatusCreateView','StatusDetailView',
    #carrier type view
    'CarrierTypeListView','CarrierTypeCreateView','CarrierTypeDetailView',
    #Country City States Views
    'CityCreateView','CityDetailView','CityListView',
    'CountryDropdownView','StateDropdownView','EquipmentDropdownView','CustomerDropdownView','TransportModeDropdownView',
    #Container Views
    'ContainerCreateView','ContainerDetailView','ContainerListView',
    #Equipment Views
    'EquipmentCreateView','EquipmentDetailView','EquipmentListView','CustomerCompaniesDropdownView',
    #Seaport Views
    'SeaportCreateView','SeaportDetailView','SeaportListView',
    #Customer Views
    'CustomerCreateView','CustomerDetailView','CustomerListView',
    #Company Views
    'CompanyCreateView','CompanyDetailView','CompanyListView',
    #Customer Document Association Views
    'CustomerDocAssocCreateView','CustomerDocAssocDetailView','CustomerDocAssocListView',
    #Document Management
    'DocumentTypeListView','DocumentTypeCreateView','DocumentTypeDetailView','DocumentTypeDropdownView',
    #Transport Mode Views
    'TransportModeListView',
    #Carrier Views
    'CarrierCreateView','CarrierDetailView','CarrierListView',
    #Customer LSP Association Views
    'CustomerLspAssocCreateView','CustomerLspAssocDetailView','CustomerLspAssocListView',
    #Carrier Contact Views
    'CarrierContactCreateView','CarrierContactDetailView','CarrierContactListView',
    #Inspection Area Views
    'InspectionAreaListView','InspectionAreaCreateView','InspectionAreaDetailView',
    #Custom Officer Shift views
    'CustomsOfficerShiftListView','CustomsOfficerShiftCreateView','CustomsOfficerShiftDetailView',
]
