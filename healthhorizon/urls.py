from django.contrib import admin
from django.urls import path
from health_app.views import (
    UserProfileListView, UserProfileDetailView, UserProfileCreateView, UserProfileUpdateView, UserProfileDeleteView,
    DateInfoListView, DateInfoDetailView, DateInfoCreateView, UserProfileLogoutView, DateInfoUpdateView, DateInfoDeleteView, HomePageView, UserProfileLoginView
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls),

    # UserProfile URLs
    path('userprofile/logout/', UserProfileLogoutView.as_view(), name='userprofile_logout'),
    path('userprofile/login/', UserProfileLoginView.as_view(), name='userprofile_login'),
    path('userprofile/create/', UserProfileCreateView.as_view(), name='userprofile_create'),
    path('userprofile/', UserProfileListView.as_view(), name='userprofile_list'),
    path('userprofile/<int:pk>/', UserProfileDetailView.as_view(), name='userprofile_detail'),
    path('userprofile/<int:pk>/update/', UserProfileUpdateView.as_view(), name='userprofile_update'),
    path('userprofile/<int:pk>/delete/', UserProfileDeleteView.as_view(), name='userprofile_delete'),

    # DateInfo URLs
    path('dateinfo/', DateInfoListView.as_view(), name='dateinfo_list'),
    path('dateinfo/<int:pk>/', DateInfoDetailView.as_view(), name='dateinfo_detail'),
    path('dateinfo/create/', DateInfoCreateView.as_view(), name='dateinfo_create'),
    path('dateinfo/<int:pk>/update/', DateInfoUpdateView.as_view(), name='dateinfo_update'),
    path('dateinfo/<int:pk>/delete/', DateInfoDeleteView.as_view(), name='dateinfo_delete'),
]
