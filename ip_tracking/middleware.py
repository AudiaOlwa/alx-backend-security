from .models import RequestLog
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from ipware import get_client_ip   # utile pour récupérer l'IP proprement
from django.http import HttpResponseForbidden
from .models import BlockedIP
from django.utils.timezone import now
from django.db import connection
from django.core.cache import cache
import ipinfo
from django.db import OperationalError

# ipinfo API (free mode can work without token)
handler = ipinfo.getHandler(access_token=None)

#class IPLoggingMiddleware(MiddlewareMixin):
#    def process_request(self, request):
#        ip, _ = get_client_ip(request)
#        if ip is None:
#            ip = "0.0.0.0"  # fallback
#
#        RequestLog.objects.create(
#            ip_address=ip,
#            timestamp=timezone.now(),
#            path=request.path
#        )

class IPLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip, _ = get_client_ip(request)
        ip = ip or "0.0.0.0"
        try:
            RequestLog.objects.create(
                ip_address=ip,
                timestamp=timezone.now(),
                path=request.path
            )
        except OperationalError:
            # Table non créée encore, ignorer pour l'instant
            pass

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request)
        ip = ip or "0.0.0.0"

        cache_key = f"geo_{ip}"
        geo = cache.get(cache_key)

        if not geo:
            try:
                details = handler.getDetails(ip)
                geo = {
                    "country": getattr(details, "country", None),
                    "city": getattr(details, "city", None),
                }
                cache.set(cache_key, geo, timeout=86400)
            except Exception:
                geo = {"country": None, "city": None}

        RequestLog.objects.create(
            ip_address=ip,
            timestamp=now(),
            path=request.path,
            country=geo["country"],
            city=geo["city"]
        )

        return self.get_response(request)