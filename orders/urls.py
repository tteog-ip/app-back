from django.urls import path
from .views      import ApplicationListView, ApplicationView, OrderFailedView
urlpatterns = [
    path('/cart', ApplicationListView.as_view()),
    path('/checkout', ApplicationView.as_view()),
    path('/fail', OrderFailedView.as_view()),
]
