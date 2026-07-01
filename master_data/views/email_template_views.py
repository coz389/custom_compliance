from rest_framework import generics, permissions, status
from rest_framework.response import Response
from core.permissions import HasModulePermission
import django_filters
from django.db.models import Q
from django.contrib.auth import get_user_model

from master_data.models import EmailTemplate, EmailTemplateHash
from master_data.serializers import (
    EmailTemplateListSerializer,
    EmailTemplateListRequestSerializer,
    EmailTemplateCreateSerializer,
    EmailTemplateUpdateSerializer,
    EmailTemplateHashDropdownSerializer,
)

from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view

User = get_user_model()


class EmailTemplateFilter(django_filters.FilterSet):
    template_title = django_filters.CharFilter(lookup_expr='icontains')
    subject = django_filters.CharFilter(lookup_expr='icontains')
    customer_id = django_filters.NumberFilter(field_name='customer_id')
    company_id = django_filters.NumberFilter(field_name='company_id')
    status_id = django_filters.NumberFilter(field_name='status_ref_id')
    template_type = django_filters.NumberFilter(field_name='template_type_id')
    status = django_filters.BooleanFilter()
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='date')
    created_at_min = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    created_at_max = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')

    class Meta:
        model = EmailTemplate
        fields = ['template_title', 'subject', 'status', 'created_by', 'created_at']


class EmailTemplateListView(generics.GenericAPIView):
    """
    List all email templates with filtering using POST method
    """
    queryset = EmailTemplate.objects.select_related('created_by', 'updated_by', 'customer', 'status_ref', 'template_type')
    serializer_class = EmailTemplateListSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'email_templates'

    def get_action_code(self):
        return 'view'

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

    @extend_schema(
        request=EmailTemplateListRequestSerializer,
        responses={200: EmailTemplateListSerializer(many=True)},
        tags=['Email Template'],
        description="List all active email templates with optional filtering, sorting, and pagination. Use POST method to send filter criteria in the request body.",
        summary="List Email Templates (with filtering)",
        operation_id="v1_email_template_list_post"
    )
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        clean_data = {k.strip(): (v.strip() if isinstance(v, str) else v)
                      for k, v in request.data.items()}

        filterset = EmailTemplateFilter(clean_data, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        else:
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        sort_column = clean_data.get('sort_column', 'created_at')
        sort_order = clean_data.get('sort_order', 'desc')

        allowed_columns = [f.name for f in EmailTemplate._meta.fields]
        if sort_column in allowed_columns:
            if sort_order.lower() == 'desc':
                queryset = queryset.order_by(f'-{sort_column}')
            else:
                queryset = queryset.order_by(f'{sort_column}')

        search = clean_data.get('search')
        if search:
            queryset = queryset.filter(
                Q(template_title__icontains=search) |
                Q(subject__icontains=search)
            )

        paginator = self.pagination_class()
        page_num = clean_data.get('page', 1)
        page_size = clean_data.get('page_size', paginator.page_size)

        paginator.page_size = page_size
        try:
            request.query_params._mutable = True
            request.query_params['page'] = page_num
            request.query_params['page_size'] = page_size
            request.query_params._mutable = False
            page = paginator.paginate_queryset(queryset, request, view=self)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Email Template'])
class EmailTemplateCreateView(generics.CreateAPIView):
    """
    Create a new email template
    """
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateCreateSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'email_templates'
    action_code = 'add'

    def check_permissions(self, request):
        super().check_permissions(request)


@extend_schema(tags=['Email Template'])
class EmailTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a specific email template
    """
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateListSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'email_templates'
    action_code = 'view'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EmailTemplateListSerializer
        return EmailTemplateUpdateSerializer

    def get_action_code(self):
        if self.request.method == 'GET':
            return 'view'
        elif self.request.method in ['PUT', 'PATCH']:
            return 'update'
        elif self.request.method == 'DELETE':
            return 'delete'
        return None

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        acting_user = request.user if request.user.is_authenticated else None
        instance.soft_delete(user=acting_user)
        instance = EmailTemplate.all_objects.get(pk=instance.pk)
        serializer = self.get_serializer(instance)
        return Response({
            "status": "success",
            "message": "Email template deleted successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


@extend_schema_view(get=extend_schema(
    parameters=[
        OpenApiParameter(
            name="template_type",
            description="Template type id used to filter hashes.",
            required=True,
            type=int,
            location=OpenApiParameter.PATH,
        ),
    ],
    responses={200: EmailTemplateHashDropdownSerializer(many=True)},
    tags=["Dropdown lists"],
    description="Dropdown list of email template hashes filtered by template type.",
    summary="Email Template Hash Dropdown",
    operation_id="v1_email_template_hash_dropdown",
))
class EmailTemplateHashDropdownView(generics.ListAPIView):
    serializer_class = EmailTemplateHashDropdownSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = 'email_templates'
    action_code = 'view'

    def get_queryset(self):
        return EmailTemplateHash.objects.filter(
            template_type_id=self.kwargs.get('template_type')
        ).order_by('hash_title')
