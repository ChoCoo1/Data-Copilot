from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('test_database_connection/', test_database_connection, name='test_database_connection'),
    path('save_database_connection/', save_database_connection, name='save_database_connection'),
    path('get_database_connections/', get_database_connections, name='get_database_connections'),
    path('delete_database_connection/',delete_database_connection, name='delete_database_connection'),
    path('generate_sql_query/', generate_sql_query, name='generate_sql_query'),
    path('get_database_name/', get_database_name, name='get_database_name'),
]