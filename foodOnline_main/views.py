from django.shortcuts import render
from django.http import HttpResponse
from vendor.models import Vendor
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D  # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance

def home(request):
    if 'lat' in request.GET:
        print('if test start from here ')
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')

        print(lat,lng)


                #IN point lng will be first
        pnt = GEOSGeometry('POINT(%s %s)'%(lng,lat))

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
