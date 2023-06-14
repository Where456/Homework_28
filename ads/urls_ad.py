from django.urls import path

from ads import views_ad

urlpatterns = [
    path('', views_ad.AdListView.as_view()),
    path('<int:pk>/', views_ad.AdDetailView.as_view()),
    path('create/', views_ad.AdCreateView.as_view()),
    path('<int:pk>/update/', views_ad.AdUpdateView.as_view()),
    path('<int:pk>/delete/', views_ad.AdDeleteView.as_view()),
    path('<int:pk>/upload_image/', views_ad.AdUploadImageView.as_view()),
]