# urls.py
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
app_name = "art_generator"
urlpatterns = [

    path('imageGenerate/', views.image_generate_view, name='imageGenerate'),
    #path('imageGenerate/<int:pk>/', views.image_generate_view, name='imageGenerate'),
    path('projectList/', views.project_list_view, name='projectList'),
    path('chooseType/', views.choose_type_view, name='chooseType'),
    path('export/',views.export_view,name='export'),
    path('deleteImage/',views.delete_image_view,name='deleteImage')


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)