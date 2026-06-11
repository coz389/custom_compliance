from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
import django_filters

from drf_spectacular.utils import extend_schema

from core.permissions import HasModulePermission

from master_data.models import City
from master_data.serializers import CitySerializer, CityListRequestSerializer


class CityFilter(django_filters.FilterSet):
    city_name = django_filters.CharFilter(lookup_expr="icontains")
    state = django_filters.NumberFilter(field_name="state_id")
    country = django_filters.NumberFilter(field_name="country_id")
    created_at = django_filters.DateFilter(field_name="created_at", lookup_expr="date")
    created_at_min = django_filters.DateFilter(
        field_name="created_at", lookup_expr="date__gte"
    )
    created_at_max = django_filters.DateFilter(
        field_name="created_at", lookup_expr="date__lte"
    )

    class Meta:
        model = City
        fields = ["city_name", "state", "country", "status", "created_at"]


class CityListView(generics.GenericAPIView):
    """
    List all cities with filtering using POST method
    """

    queryset = City.objects.select_related(
        "state", "country", "created_by", "updated_by"
    ).filter(status=True)

    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]

    module_code = "country"

    def get_action_code(self):
        return "view"

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

    @extend_schema(
        request=CityListRequestSerializer,
        responses={200: CitySerializer(many=True)},
        tags=["City Management"],
        description="List all active cities with filtering, sorting and pagination.",
        summary="List Cities",
        operation_id="v1_city_list_post",
    )
    def post(self, request, *args, **kwargs):

        queryset = self.get_queryset()

        clean_data = {
            k.strip(): (v.strip() if isinstance(v, str) else v)
            for k, v in request.data.items()
        }

        # Filtering
        filterset = CityFilter(clean_data, queryset=queryset)

        if filterset.is_valid():
            queryset = filterset.qs
        else:
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        # Sorting
        sort_column = clean_data.get("sort_column", "created_at")
        sort_order = clean_data.get("sort_order", "desc")

        allowed_columns = [f.name for f in City._meta.fields]

        if sort_column in allowed_columns:
            if sort_order.lower() == "desc":
                queryset = queryset.order_by(f"-{sort_column}")
            else:
                queryset = queryset.order_by(sort_column)

        # Global Search
        search = clean_data.get("search")

        if search:
            queryset = queryset.filter(
                Q(city_name__icontains=search)
                | Q(unloc__icontains=search)
                | Q(state__state_name__icontains=search)
                | Q(country__country_name__icontains=search)
            )

        # Pagination
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


@extend_schema(tags=["City Management"])
class CityCreateView(generics.CreateAPIView):
    """
    Create a new city
    """

    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = "country"
    action_code = "add"

    def check_permissions(self, request):
        super().check_permissions(request)


@extend_schema(tags=["City Management"])
class CityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a city
    """

    queryset = City.objects.select_related(
        "state", "country", "created_by", "updated_by"
    )

    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]
    module_code = "country"
    action_code = "view"

    def get_action_code(self):

        if self.request.method == "GET":
            return "view"

        elif self.request.method in ["PUT", "PATCH"]:
            return "update"

        elif self.request.method == "DELETE":
            return "delete"

        return None

    def check_permissions(self, request):
        self.action_code = self.get_action_code()
        super().check_permissions(request)

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        acting_user = request.user if request.user.is_authenticated else None

        instance.soft_delete(user=acting_user)

        instance = City.all_objects.get(pk=instance.pk)

        serializer = self.get_serializer(instance)

        return Response(
            {
                "status": "success",
                "message": "City deleted successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
