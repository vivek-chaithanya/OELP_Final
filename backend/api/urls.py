from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import RegisterView, MeView, GoogleLoginView, PhoneStartView, PhoneVerifyView, AssignRoleView, RoleViewSet, RegionViewSet
from core.views import (
    FarmViewSet,
    FieldViewSet,
    CropViewSet,
    CropVarietyViewSet,
    IrrigationMethodViewSet,
    AssetViewSet,
    CropLifecycleDatesViewSet,
    SoilReportViewSet,
)
from payments.views import CreateOrderView, CapturePaymentView, RefundPaymentView
from notifications.views import NotificationTemplateViewSet, NotificationViewSet
from analytics.views import RevenueView, ActiveUsersView, SoilReportsExportView, CropsExportView
from subscriptions.views import MainPlanViewSet, TopUpPlanViewSet, EnterprisePlanViewSet, UserPlanViewSet

router = DefaultRouter()
router.register(r'farms', FarmViewSet, basename='farms')
router.register(r'fields', FieldViewSet, basename='fields')
router.register(r'crops', CropViewSet, basename='crops')
router.register(r'varieties', CropVarietyViewSet, basename='varieties')
router.register(r'irrigation-methods', IrrigationMethodViewSet, basename='irrigation-methods')
router.register(r'assets', AssetViewSet, basename='assets')
router.register(r'lifecycles', CropLifecycleDatesViewSet, basename='lifecycles')
router.register(r'soil-reports', SoilReportViewSet, basename='soil-reports')
router.register(r'notification-templates', NotificationTemplateViewSet, basename='notification-templates')
router.register(r'notifications', NotificationViewSet, basename='notifications')
router.register(r'roles', RoleViewSet, basename='roles')
router.register(r'regions', RegionViewSet, basename='regions')
router.register(r'plans/main', MainPlanViewSet, basename='plans-main')
router.register(r'plans/topup', TopUpPlanViewSet, basename='plans-topup')
router.register(r'plans/enterprise', EnterprisePlanViewSet, basename='plans-enterprise')
router.register(r'user/plans', UserPlanViewSet, basename='user-plans')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view()),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', MeView.as_view()),
    path('auth/google/', GoogleLoginView.as_view()),
    path('auth/phone/start/', PhoneStartView.as_view()),
    path('auth/phone/verify/', PhoneVerifyView.as_view()),
    path('roles/assign', AssignRoleView.as_view()),
    path('payments/order', CreateOrderView.as_view()),
    path('payments/capture', CapturePaymentView.as_view()),
    path('payments/refund', RefundPaymentView.as_view()),
    path('analytics/revenue', RevenueView.as_view()),
    path('analytics/active-users', ActiveUsersView.as_view()),
    path('reports/export/soil', SoilReportsExportView.as_view()),
    path('reports/export/crops', CropsExportView.as_view()),
]

