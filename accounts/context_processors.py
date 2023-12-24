from vendor.models import Vendor

def get_vendor_details(request):
    #It take request as param and return dictionary which is context dictionary
    try:
        vendor =Vendor.objects.get(user=request.user)
    except:
        vendor=None
    return dict(vendor=vendor)
