from django.urls import path

from products.views import AptView, AptDetailView


urlpatterns = [
    path('', AptView.as_view()),
    path('/<int:apt_id>', AptDetailView.as_view()),
]
