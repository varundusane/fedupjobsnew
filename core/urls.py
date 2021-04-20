from django.urls import path, include
from . import views
from rest_framework import routers
from .views import filteredViewSet, filteredCompanyViewSet, filtered_for_keysViewSet, filtered_for_categoryViewSet, filtered_for_countryViewSet, blog, tos

router = routers.DefaultRouter()
router.register('filteredViewSet', filteredViewSet, 'filteredViewSet')
router.register('filteredFromCompanyViewSet', filteredCompanyViewSet, 'filteredCompanyViewSet')
router.register('filteredForKeysViewSet', filtered_for_keysViewSet, 'filteredForKeysViewSet')
router.register('filteredForCategoryViewSet', filtered_for_categoryViewSet, 'filteredForcategoryViewSet')
router.register('filteredForCountryViewSet', filtered_for_countryViewSet, 'filteredForcountryViewSet')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.index, name="index"),
    path('job/<id>/', views.jobDetails, name="job_details"),
    path('startup', views.startup, name="startup"),
    path('jobs/<company_name>', views.company_jobs, name="all_jobs_in_company"),
    path('jobkey/<job_keys>', views.filtered_keys, name="filtered_keys"),
    path('tags', views.allTags, name="all_tags"),
    path('collection', views.collection, name="collection"),
    path('location', views.locations, name="location"),
    path('country/<country>', views.countrys, name="job_in_country"),
    path('addNewPost/', views.addNewPost, name="addNewPost"),
    path('search_on_index', views.index_search, name="index_search"),
    path('category/<name>', views.category, name="category"),
    path('blog', views.blog, name="blog"),
    path('tos', views.tos, name="tos")
    # path('fetch', views.Command, name="command"),
    
]