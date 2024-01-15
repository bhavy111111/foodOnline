from django.shortcuts import render
from django.http import HttpResponse
from vendor.models import Vendor
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D  # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance

def get_or_set_current_location(request):
    # if lat and long are stored in session will take session variable
    if 'lat' in request.session:
        lat=request.session['lat']
        lng=request.session['lng']
        return lng,lat
    #if lat and long are stored in browser will take browser variable
    elif 'lat' in request.GET:
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')

        # if they are in url variable , it will make them session variables
        request.session['lat']=lat
        request.session['lng']=lng
        return lng,lat
    else:
        return None


def home(request):
    if get_or_set_current_location(request) is not None:
               #IN point lng will be first
        pnt = GEOSGeometry('POINT(%s %s)'%(get_or_set_current_location(request)))

        # Query that bring nearby restro to home page
        vendors = Vendor.objects.filter(user_profile__location__distance_lte=(pnt, D(km=1000))).annotate(distance=Distance('user_profile__location',pnt)).order_by('distance')

        for v in vendors:
            v.kms = round(v.distance.km,1)
    else:

        vendors = Vendor.objects.filter(is_approved=True,user__is_active=True)
    print('List of vendors',vendors)
    context={
        'vendors':vendors,
    }



    return render(request, 'home.html',context)
