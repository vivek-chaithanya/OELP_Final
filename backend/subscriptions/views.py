from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MainPlan, TopUpPlan, EnterprisePlan, UserPlan
from .serializers import MainPlanSerializer, TopUpPlanSerializer, EnterprisePlanSerializer, UserPlanSerializer


class MainPlanViewSet(viewsets.ModelViewSet):
    queryset = MainPlan.objects.filter(active=True)
    serializer_class = MainPlanSerializer
    permission_classes = [permissions.IsAuthenticated]


class TopUpPlanViewSet(viewsets.ModelViewSet):
    queryset = TopUpPlan.objects.filter(active=True)
    serializer_class = TopUpPlanSerializer
    permission_classes = [permissions.IsAuthenticated]


class EnterprisePlanViewSet(viewsets.ModelViewSet):
    queryset = EnterprisePlan.objects.filter(active=True)
    serializer_class = EnterprisePlanSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserPlanViewSet(viewsets.ModelViewSet):
    serializer_class = UserPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserPlan.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def upgrade(self, request):
        plan_type = request.data.get('plan_type')
        plan_id = request.data.get('plan_id')
        up = UserPlan.objects.create(user=request.user, plan_type=plan_type, plan_id=plan_id)
        return Response(UserPlanSerializer(up).data)

    @action(detail=False, methods=['post'])
    def downgrade(self, request):
        last = UserPlan.objects.filter(user=request.user).order_by('-id').first()
        if not last:
            return Response({"detail": "No active plan"}, status=status.HTTP_400_BAD_REQUEST)
        last.status = 'cancelled'
        last.save()
        return Response(UserPlanSerializer(last).data)
