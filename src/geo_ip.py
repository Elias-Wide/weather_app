import urllib.request as urllib2
import ipinfo


def get_location():
    access_token = "31c05071943498"
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails()
    print(details.city, details.loc)
    return details.city
