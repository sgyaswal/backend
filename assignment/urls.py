from django.urls import path
from .views import ExcelDataView, GetProjects, DeleteAllDataView

urlpatterns = [
    path('excel-data', ExcelDataView.as_view(), name='excel-data'),
    path('get-projects', GetProjects.as_view(), name='get-projects'),
    path('delete-projects', DeleteAllDataView.as_view(), name='delete-projects')
]