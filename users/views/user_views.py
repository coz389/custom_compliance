import django_filters
from rest_framework import generics, permissions, status,serializers as drf_serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from yaml import serializer
from core.pagination import StandardResultsSetPagination
from users.serializers import UserSerializer, UserCreateSerializer,UserListRequestSerializer,UserUpdateSerializer
from core.permissions import HasModulePermission
from rest_framework.views import APIView
from django.db.models import Q
from drf_spectacular.utils import extend_schema,inline_serializer, OpenApiExample,extend_schema_view
from django.db import transaction
from users.models import UserCompanyAssoc
from master_data.models import Company
User = get_user_model()

class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    # Date filter: match specific date
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='date')
    # Range filter: match between two dates (optional but useful)
    created_at_min = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    created_at_max = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username','email','phone_number', 'created_at', 'created_at_min', 'created_at_max']


class UserListView(APIView):
    """
    POST method
    """
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'user_management'
    action_code = 'view'  # default to view, will adjust in check_permissions

    pagination_class = StandardResultsSetPagination 
    @extend_schema(
        request=UserListRequestSerializer,
        responses={200: UserSerializer(many=True)},
        tags=['Users Management'], # Grouping in Swagger UI
        description="List all users with optional filtering, sorting, and pagination. Use POST method to send filter criteria in the request body.", # Detailed description for Swagger UI
        summary="List Users (With Filter)",
        operation_id="user_list_post"
    )
    def post(self, request):        
        # Clean request data: strip spaces from keys and values
        clean_data = {k.strip(): (v.strip() if isinstance(v, str) else v) 
                      for k, v in request.data.items()}
        
        # Sirf active records (Soft Delete handling) [History]
        queryset = User.objects.filter(deleted_at__isnull=True)

        # 1. Apply filters
        filterset = UserFilter(clean_data, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        else:
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # 2. Global Search
        global_search = clean_data.get('search')
        if global_search:
            queryset = queryset.filter(
                Q(first_name__icontains=global_search) | Q(last_name__icontains=global_search) | Q(username__icontains=global_search) | Q(email__icontains=global_search) | Q(phone_number__icontains=global_search)
            )


        # 3. Ordering
        sort_column = clean_data.get('sort_column', 'created_at')
        sort_order = clean_data.get('sort_order', 'desc') # default to newest first
        
        # Validate sort_column exists in model
        allowed_columns = [f.name for f in User._meta.fields]
        if sort_column in allowed_columns:
            if sort_order.lower() == 'desc':
                queryset = queryset.order_by(f'-{sort_column}')
            else:
                queryset = queryset.order_by(f'{sort_column}')

        # 4. Pagination [1]
        paginator = self.pagination_class()
        page_num = clean_data.get('page', 1)
        page_size = clean_data.get('page_size', paginator.page_size)
        paginator.page_size = page_size
        # We need to trick DRF paginator to read page from our clean_data instead of query_params
        # Or we can manually paginate
        try:
            # Standard paginator uses query_params, so we override the request's query_params temporarily
            # But a cleaner way is to set the page number manually if possible.
            # For simplicity, let's inject into request.query_params for the paginator to find it
            request.query_params._mutable = True
            request.query_params['page'] = page_num
            request.query_params['page_size'] = page_size
            request.query_params._mutable = False
            page = paginator.paginate_queryset(queryset, request, view=self)
            
            if page is not None:
                serializer = UserSerializer(page, many=True) 
                return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            return Response({"success": False, "detail": str(e)}, status=400)

        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'user_management'
    action_code = 'view'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        return UserUpdateSerializer

    def get_action_code(self):
        if self.request.method == 'GET':
            return 'view'
        elif self.request.method in ['PUT', 'PATCH']:
            return 'update'
        return None

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

    @extend_schema(
        tags=['Users Management'],
        summary='Retrieve a user',
        description='Get full details of a specific user including assigned companies.',
        responses={200: UserSerializer},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=['Users Management'],
        summary='Update user with company assignments',
        description='Updates user fields and replaces all existing company assignments.',
        request=inline_serializer(
            name='UserUpdateWithCompaniesRequest',
            fields={
                'first_name':   drf_serializers.CharField(required=False),
                'last_name':    drf_serializers.CharField(required=False),
                'email':        drf_serializers.EmailField(required=False),
                'role':         drf_serializers.IntegerField(required=False),
                'is_active':    drf_serializers.BooleanField(required=False),
                'company_ids':  drf_serializers.ListField(
                    child=drf_serializers.IntegerField(min_value=1),
                    required=False,
                    help_text='List of Company IDs. Replaces existing assignments.',
                ),
            }
        ),
        examples=[
            OpenApiExample(
                name='Update user and assign companies',
                value={
                    'first_name': 'Abhishek',
                    'last_name':  'Sahu',
                    'role':       1,
                    'is_active':  True,
                    'company_ids': [1, 2, 3],
                },
                request_only=True,
            )
        ],
        responses={200: UserSerializer},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        tags=['Users Management'],
        summary='Partially update user',
        request=inline_serializer(
            name='UserPartialUpdateRequest',
            fields={
                'first_name':  drf_serializers.CharField(required=False),
                'last_name':   drf_serializers.CharField(required=False),
                'email':       drf_serializers.EmailField(required=False),
                'role':        drf_serializers.IntegerField(required=False),
                'is_active':   drf_serializers.BooleanField(required=False),
                'company_ids': drf_serializers.ListField(
                    child=drf_serializers.IntegerField(min_value=1),
                    required=False,
                    help_text='List of Company IDs. Replaces existing assignments.',
                ),
            }
        ),
        responses={200: UserSerializer},
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @transaction.atomic
    def perform_update(self, serializer):
        instance = serializer.save()
        company_ids = self.request.data.get('company_ids')

        if not company_ids:
            return

        instance.user_company_assoc.all().delete()

        UserCompanyAssoc.objects.bulk_create([
            UserCompanyAssoc(user=instance, company_id=int(cid), created_by=instance)
            for cid in company_ids
        ])

class UserDetailView123(generics.RetrieveUpdateAPIView):#RetrieveUpdateDestroyAPIView
    """
    Retrieve, update or delete a specific user (admin only)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'user_management'
    action_code = 'view'  # default to view, will adjust in check_permissions

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        return UserUpdateSerializer

    def get_action_code(self):
        if self.request.method == 'GET':
            return 'view'
        elif self.request.method in ['PUT', 'PATCH']:
            return 'update'
        return None

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)
        

    @transaction.atomic
    def perform_update(self, serializer):
        # Get Primary table (User) Instance and Save to other table
        instance = serializer.save()  
        company_ids = self.request.data.get('company_ids')
        if not company_ids:
            return
        
        # Delete all existing associations
        UserCompanyAssoc.objects.filter(user=instance).delete()
        
        if not company_ids:
            return
        
        # Fresh insert
        UserCompanyAssoc.objects.bulk_create([
            UserCompanyAssoc(user=instance, company_id=int(cid), created_by=instance)
            for cid in company_ids
        ])

        
       
    """
    def destroy(self, request, *args, **kwargs):
        # 1. Look up object inside default active manager scope
        instance = self.get_object()
        
        # 3. Execution of the mutation tracking layer
        acting_user = request.user if request.user.is_authenticated else None
        
        # Soft-delete execution boundary
        instance.soft_delete(user=acting_user)
        
        # CRITICAL FIX: Base manager dynamically targeted bypassing soft-delete filtration block
        # explicit backend reload executing base manager
        instance = User.all_objects.get(pk=instance.pk)

        # 5. Pipeline Serialization mapping out exact object state representation
        serializer = self.get_serializer(instance)
        
        return Response({
            "status": "success",
            "message": "User soft-deleted successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    """

@extend_schema(tags=['Users Management']) 
class UserActiveInactiveView(APIView):
    """
    Activate or deactivate a user (admin only)
    """
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'user_management'
    action_code = 'update'

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk, deleted_at__isnull=True)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Toggle active status
        user.is_active = not user.is_active
        user.save()

        status_str = "activated" if user.is_active else "deactivated"
        return Response({"detail": f"User has been {status_str}."}, status=status.HTTP_200_OK)