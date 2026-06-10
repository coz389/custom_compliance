from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions

from core.permissions import HasModulePermission
from master_data.models.country import Country
from master_data.serializers.country_serializers import CountryDropdownSerializer


@extend_schema(
    responses={200: CountryDropdownSerializer(many=True)},
    tags=["Country Management"],
    description="Dropdown list of countries.",
    summary="Country Dropdown",
    operation_id="v1_country_list",
)
class CountryDropdownView(generics.ListAPIView):
    queryset = Country.objects.all().order_by("country_name")
    serializer_class = CountryDropdownSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated, HasModulePermission]

    module_code = "country"
    action_code = "view"
