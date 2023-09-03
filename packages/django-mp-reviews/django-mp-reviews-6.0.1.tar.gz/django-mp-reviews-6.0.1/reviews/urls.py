
from django.urls import path

from reviews import views


app_name = 'reviews'


urlpatterns = [

    path('', views.ReviewListView.as_view(), name='list'),

    path('modal/', views.CreateReviewView.as_view(), name='modal')

]
