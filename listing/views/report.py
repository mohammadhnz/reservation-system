from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from listing.serializers import report as report_serializers
from listing.services.report_services import get_rooms_reservation_by_time


class RoomReportAPIView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = report_serializers.ReportParamsSerializer(
            data={
                **request.query_params.dict(),
            }
        )
        if not serializer.is_valid(raise_exception=True):
            return Response("query params are not valid", status=400)

        data = self._get_report_data(serializer)
        return render(request, "report.html", {"data": data})

    def _get_report_data(self, serializer):
        rooms_data = get_rooms_reservation_by_time(**serializer.validated_data)
        serializer = report_serializers.RoomReportSerializer(rooms_data, many=True)
        data = serializer.data
        return data
