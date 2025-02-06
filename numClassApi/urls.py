from django.urls import path
from .views import NumberClassificationAPI

urlpatterns = [
    path('classify-number/', NumberClassificationAPI.as_view(), name='classify-number'),
]
