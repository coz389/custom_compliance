import django_filters
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from core.permissions import HasModulePermission
from master_data.models import Seaport
from master_data.serializers import SeaportListRequestSerializer, SeaportSerializer


class SeaportFilter(django_filters.FilterSet):
    port_name = django_filters.CharFilter(lookup_expr="icontains")
    unloc = django_filters.CharFilter(lookup_expr="icontains")
    country = django_filters.NumberFilter(field_name="country_id")
    tradelane_name = django_filters.CharFilter(lookup_expr="icontains")
    created_at = django_filters.DateFilter(field_name="created_at", lookup_expr="date")
    created_at_min = django_filters.DateFilter(
        field_name="created_at", lookup_expr="date__gte"
    )
    created_at_max = django_filters.DateFilter(
        field_name="created_at", lookup_expr="date__lte"
    )

    class Meta:
        model = Seaport
        fields = [
            "port_name",
            "unloc",
            "country",
            "tradelane_name",
            "status",
            "created_at",
        ]


class SeaportListView(generics.GenericAPIView):
    queryset = Seaport.objects.select_related(
        "country", "created_by", "updated_by"
    ).filter(status=True)
    serializer_class = SeaportSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = "seaport_management"

    def get_action_code(self):
        return "view"

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

    @extend_schema(
        request=SeaportListRequestSerializer,
        responses={200: SeaportSerializer(many=True)},
        tags=["Seaport Management"],
        description="List all active seaports with filtering, sorting and pagination.",
        summary="List Seaports",
        operation_id="v1_seaport_list_post",
    )
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        clean_data = {
            k.strip(): (v.strip() if isinstance(v, str) else v)
            for k, v in request.data.items()
        }

        filterset = SeaportFilter(clean_data, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
        else:
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        sort_column = clean_data.get("sort_column", "created_at")
        sort_order = clean_data.get("sort_order", "desc")
        allowed_columns = [f.name for f in Seaport._meta.fields]

        if sort_column in allowed_columns:
            if sort_order.lower() == "desc":
                queryset = queryset.order_by(f"-{sort_column}")
            else:
                queryset = queryset.order_by(sort_column)

        search = clean_data.get("search")
        if search:
            queryset = queryset.filter(
                Q(port_name__icontains=search)
                | Q(unloc__icontains=search)
                | Q(country__country_name__icontains=search)
                | Q(tradelane_name__icontains=search)
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


@extend_schema(tags=["Seaport Management"])
class SeaportCreateView(generics.CreateAPIView):
    queryset = Seaport.objects.all()
    serializer_class = SeaportSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = "seaport_management"
    action_code = "add"

    def check_permissions(self, request):
        super().check_permissions(request)


@extend_schema(tags=["Seaport Management"])
class SeaportDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Seaport.objects.select_related("country", "created_by", "updated_by")
    serializer_class = SeaportSerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = "seaport_management"
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
        instance = Seaport.all_objects.get(pk=instance.pk)
        serializer = self.get_serializer(instance)

        return Response(
            {
                "status": "success",
                "message": "Seaport deleted successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
