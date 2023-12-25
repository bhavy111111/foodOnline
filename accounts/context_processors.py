from vendor.models import Vendor
from django.conf import settings
def get_vendor_details(request):
    #It take request as param and return dictionary which is context dictionary
    try:
        vendor =Vendor.objects.get(user=request.user)
    except:
        vendor=None
    return dict(vendor=vendor)

def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}