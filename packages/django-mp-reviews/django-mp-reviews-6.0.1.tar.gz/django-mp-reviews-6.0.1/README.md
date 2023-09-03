# MP-Reviews

Django reviews app.

### Installation

Install with pip:

```
$ pip install django-mp-reviews
```

Add reviews to settings.py:

```
INSTALLED_APPS = [
    'reviews',
]
```

Add reviews to urls.py:
```
urlpatterns = [
    path('reviews/', include('reviews.urls'))
]
```
