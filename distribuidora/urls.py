from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    # path("getProductos", hello.views.get_productos, name="productos_view"),
    path("index", hello.views.index, name="index"),
    path("getEmpleados", hello.views.getEmpleados, name="getEmpleados"),
    # path("admin/", admin.site.urls),
]
