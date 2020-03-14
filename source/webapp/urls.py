from django.urls import path
from django.views.generic import DeleteView

from webapp.views import IndexView, FileCreate, FileUpdate, DetailFile, FileDelete

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('file/create/', FileCreate.as_view(), name='create_file'),
    path('file/update/<int:pk>/', FileUpdate.as_view(), name='update_file'),
    path('file/<int:pk>/', DetailFile.as_view(), name='file_detail'),
    path('file/delete/<int:pk>/', FileDelete.as_view(), name='file_delete')
]
