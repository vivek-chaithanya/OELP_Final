import csv
from datetime import datetime
from django.http import HttpResponse
from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from subscriptions.models import Payment
from accounts.permissions import IsAdminOrSuperAdmin
from core.models import SoilReport, Farm, Crop


class RevenueView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        qs_all = Payment.objects.filter(status__in=["captured", "refunded"]) 
        if start:
            qs_all = qs_all.filter(created_at__date__gte=start)
        if end:
            qs_all = qs_all.filter(created_at__date__lte=end)
        qs = qs_all.values("status").annotate(total=Sum("amount"))
        data = {row["status"]: row["total"] for row in qs}
        return Response({"captured": data.get("captured", 0), "refunded": data.get("refunded", 0)})


class ActiveUsersView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperAdmin]

    def get(self, request):
        farms = Farm.objects.count()
        return Response({"active_users": farms})


class SoilReportsExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="soil_reports_{datetime.utcnow().date()}.csv"'
        writer = csv.writer(response)
        writer.writerow(["field_id", "report_date", "ph", "nitrogen", "phosphorus", "potassium", "organic_matter", "notes"])
        for sr in SoilReport.objects.all()[:10000]:
            writer.writerow([sr.field_id, sr.report_date, sr.ph, sr.nitrogen, sr.phosphorus, sr.potassium, sr.organic_matter, sr.notes])
        return response


class CropsExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="crops_{datetime.utcnow().date()}.csv"'
        writer = csv.writer(response)
        writer.writerow(["id", "name", "description"])
        for c in Crop.objects.all().order_by('id'):
            writer.writerow([c.id, c.name, c.description])
        return response
