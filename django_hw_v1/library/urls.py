from django.urls import path

from .views import home_view, login_view, search_view, book_search_view, book_return_view


urlpatterns = [
    path('home/', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('search/', search_view, name='search'),
    path('book_search/', book_search_view, name='book_search'),
    path('book_return/', book_return_view, name='book_return'),
]
