from django.urls import path

from ads import views_cat

urlpatterns = [
    path('', views_cat.CategoryListView.as_view()),
    path('<int:pk>/', views_cat.CategoriesDetailView.as_view()),
    path('create/', views_cat.CategoryCreateView.as_view()),
    path('<int:pk>/update/', views_cat.CategoryUpdateView.as_view()),
    path('<int:pk>/delete/', views_cat.CategoryDeleteView.as_view()),
]