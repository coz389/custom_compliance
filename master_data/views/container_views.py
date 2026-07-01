import django_filters
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from core.permissions import HasModulePermission
from master_data.models import Container
from master_data.serializers import ContainerListRequestSerializer, ContainerSerializer


class ContainerFilter(django_filters.FilterSet):
    transport_id = django_filters.NumberFilter(field_name="transport_id")
    code = django_filters.CharFilter(lookup_expr="icontains")
    iso = django_filters.CharFilter(lookup_expr="icontains")
    size = django_filters.CharFilter(lookup_expr="icontains")
    type = django_filters.CharFilter(lookup_expr="icontains")
    description = django_filters.CharFilter(lookup_expr="icontains")
    dimension = django_filters.CharFilter(lookup_expr="icontains")
    created_at = django_filters.DateFilter(field_name="created_at", lookup_expr="date")
    created_at_min = django_filters.DateFilter(
        field_name="created_at", lookup_expr="date__gte"
    )
    created_at_max = django_filters.DateFilter(
        field_name="created_at", lookup_expr="date__lte"
    )

    class Meta:
        model = Container
        fields = [
            "transport_id",
            "code",
            "iso",
            "size",
            "type",
            "description",
            "dimension",
            "status",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by",
        ]


class ContainerListView(generics.GenericAPIView):
    queryset = Container.objects.select_related(
        "transport", "created_by", "updated_by"
    ).all()
    serializer_class = ContainerSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = "container_management"

    def get_action_code(self):
        return "view"

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

    @extend_schema(
        request=ContainerListRequestSerializer,
        responses={200: ContainerSerializer(many=True)},
        tags=["Container Management"],
        description="List all active containers with filtering, sorting and pagination.",
        summary="List Containers",
        operation_id="v1_container_list_post",
    )
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        clean_data = {
            k.strip(): (v.strip() if isinstance(v, str) else v)
            for k, v in request.data.items()
        }

        filterset = ContainerFilter(clean_data, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        else:
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        sort_column = clean_data.get("sort_column", "created_at")
        sort_order = clean_data.get("sort_order", "desc")
        allowed_columns = [f.name for f in Container._meta.fields]

        if sort_column in allowed_columns:
            queryset = queryset.order_by(
                f"-{sort_column}" if sort_order.lower() == "desc" else sort_column
            )

        search = clean_data.get("search")
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search)
                | Q(iso__icontains=search)
                | Q(size__icontains=search)
                | Q(type__icontains=search)
                | Q(description__icontains=search)
                | Q(dimension__icontains=search)
            )

        paginator = self.pagination_class()
        page_num = clean_data.get("page", 1)
        page_size = clean_data.get("page_size", paginator.page_size)
        paginator.page_size = page_size

        try:
            request.query_params._mutable = True
            request.query_params["page"] = page_num
            request.query_params["page_size"] = page_size
            request.query_params._mutable = False

            page = paginator.paginate_queryset(queryset, request, view=self)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(tags=["Container Management"])
class ContainerCreateView(generics.CreateAPIView):
    queryset = Container.objects.select_related(
        "transport", "created_by", "updated_by"
    )
    serializer_class = ContainerSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = "container_management"
    action_code = "add"

    def check_permissions(self, request):
        super().check_permissions(request)


@extend_schema(tags=["Container Management"])
class ContainerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Container.objects.select_related(
        "transport", "created_by", "updated_by"
    )
    serializer_class = ContainerSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = "container_management"
    action_code = "view"

    def get_action_code(self):
        if self.request.method == "GET":
            return "view"
        if self.request.method in ["PUT", "PATCH"]:
            return "update"
        if self.request.method == "DELETE":
            return "delete"
        return None

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        acting_user = request.user if request.user.is_authenticated else None
        instance.soft_delete(user=acting_user)
        instance = Container.all_objects.get(pk=instance.pk)
        serializer = self.get_serializer(instance)

        return Response(
            {
                "status": "success",
                "message": "Container deleted successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
