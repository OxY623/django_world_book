"""
URL configuration for WebBooks project.

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
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include, re_path
from catalog import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^author_add/$', views.author_add, name='author_add'),
    re_path(r'^edit1/(?P<id>\d+)/$', views.edit_author, name='edit1'),
    re_path(r'^create/$', views.create_author, name='create'),
    re_path(r'^delete/(?P<id>\d+)/$', views.delete_author, name='delete'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^books/$', views.BookListView.as_view(), name='books'),
    re_path(r'^books/(?P<pk>\d+)/$', views.BookDetailView.as_view(), name='book-detail'),
    re_path(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    re_path(r'^books/create/$', views.BookCreateView.as_view(), name='create_book'),
    re_path(r'^books/update/(?P<pk>\d+)/$', views.BookUpdateView.as_view(), name='update_book'),
    re_path(r'^books/delete/(?P<pk>\d+)/$', views.BookDeleteView.as_view(), name='delete_book')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
