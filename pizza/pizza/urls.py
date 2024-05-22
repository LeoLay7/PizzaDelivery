"""
URL configuration for pizza project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django.contrib
import django.urls
import django.conf
import django.conf.urls.static

urlpatterns = [
    django.urls.path("users/", django.urls.include("users.urls")),
    django.urls.path("admin/", django.contrib.admin.site.urls),
    django.urls.path("products/", django.urls.include("products.urls")),
    django.urls.path("accounts/", django.urls.include('django.contrib.auth.urls')),
    django.urls.path("", django.urls.include("homepage.urls")),
    django.urls.path("api/", django.urls.include("api.urls")),
    django.urls.path("cart/", django.urls.include("cart.urls")),
    django.urls.path("order/", django.urls.include("order.urls")),
]

if django.conf.settings.DEBUG:
    import debug_toolbar

    urlpatterns += (django.urls.path("__debug__/", django.urls.include(debug_toolbar.urls)),)
    urlpatterns += django.conf.urls.static.static(
        django.conf.settings.MEDIA_URL,
        document_root=django.conf.settings.MEDIA_ROOT,
    )
