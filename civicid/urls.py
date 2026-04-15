"""
URL configuration for civicid project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.persons.views import PersonViewSet
from apps.birth_records.views import BirthRecordViewSet
from apps.audit.views import AuditLogViewSet
from apps.id_applications.views import IDApplicationViewSet
from apps.issued_ids.views import IssuedIDViewSet
from apps.immigration_status.views import ImmigrationStatusViewSet
from apps.naturalization.views import NaturalizationRecordViewSet
from apps.voter_registration.views import VoterRegistrationViewSet, VoterIDViewSet
from apps.passports.views import PassportViewSet
from apps.death_records.views import DeathRecordViewSet
from apps.marriage_certificates.views import MarriageCertificateViewSet
from apps.social_security.views import SocialSecurityViewSet
from apps.selective_service.views import SelectiveServiceViewSet
from apps.person_photos.views import PersonPhotoViewSet

# ── API Router ───────────────────────────────────────────────────
router = DefaultRouter()
router.register(r'persons',               PersonViewSet)
router.register(r'birth-records',         BirthRecordViewSet)
router.register(r'audit-logs',            AuditLogViewSet)
router.register(r'id-applications',       IDApplicationViewSet)
router.register(r'issued-ids',            IssuedIDViewSet)
router.register(r'immigration-status',    ImmigrationStatusViewSet)
router.register(r'naturalization',        NaturalizationRecordViewSet)
router.register(r'voter-registrations',   VoterRegistrationViewSet)
router.register(r'voter-ids',             VoterIDViewSet)
router.register(r'passports',             PassportViewSet,             basename='passport')
router.register(r'death-records',         DeathRecordViewSet,          basename='death-record')
router.register(r'marriage-certificates', MarriageCertificateViewSet,  basename='marriage-certificate')
router.register(r'social-security',       SocialSecurityViewSet,       basename='social-security')
router.register(r'selective-service',     SelectiveServiceViewSet,     basename='selective-service')
router.register(r'person-photos',         PersonPhotoViewSet,          basename='person-photo')

# ── URL Patterns ─────────────────────────────────────────────────
urlpatterns = [
    path('admin/', admin.site.urls),

    # API
    path('api/', include(router.urls)),
    path('api/token/',         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),    name='token_refresh'),
    path('api/law-enforcement/', include('apps.law_enforcement.urls')),
    path('api/voter/',           include('apps.voter_registration.urls')),

    # ── Frontend pages ────────────────────────────────────────────
    path('',                          TemplateView.as_view(template_name='index.html'),                       name='login'),
    path('pages/dashboard/',          TemplateView.as_view(template_name='pages/dashboard.html'),             name='dashboard'),
    path('pages/persons/',            TemplateView.as_view(template_name='pages/persons.html'),               name='persons'),
    path('pages/birth-records/',      TemplateView.as_view(template_name='pages/birth-records.html'),         name='birth-records'),
    path('pages/id-applications/',    TemplateView.as_view(template_name='pages/id-applications.html'),       name='id-applications'),
    path('pages/audit/',              TemplateView.as_view(template_name='pages/audit.html'),                  name='audit'),
    path('pages/law-enforcement/',    TemplateView.as_view(template_name='pages/law-enforcement.html'),       name='law-enforcement'),
    path('pages/immigration/',        TemplateView.as_view(template_name='pages/immigration.html'),           name='immigration'),
    path('pages/issued-ids/',         TemplateView.as_view(template_name='pages/issued-ids.html'),            name='issued-ids'),
    path('pages/administration/',     TemplateView.as_view(template_name='pages/administration.html'),        name='administration'),
    path('pages/voter-registration/', TemplateView.as_view(template_name='pages/voter-registration.html'),    name='voter-registration'),
    path('pages/passport/',           TemplateView.as_view(template_name='pages/passport.html'),              name='passport'),
    path('pages/death-records/',      TemplateView.as_view(template_name='pages/death-records.html'),         name='death-records'),
    path('pages/marriage/',           TemplateView.as_view(template_name='pages/marriage.html'),              name='marriage'),
    path('pages/social-security/',    TemplateView.as_view(template_name='pages/social-security.html'),       name='social-security'),
    path('pages/selective-service/',  TemplateView.as_view(template_name='pages/selective-service.html'),     name='selective-service'),
]

# Serve media in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)