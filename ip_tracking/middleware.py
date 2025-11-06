from .models import RequestLog
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from ipware import get_client_ip   # utile pour récupérer l'IP proprement
from django.http import HttpResponseForbidden
from .models import BlockedIP
from django.utils.timezone import now
from django.db import connection

class IPLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip, _ = get_client_ip(request)
        if ip is None:
            ip = "0.0.0.0"  # fallback

        RequestLog.objects.create(
            ip_address=ip,
            timestamp=timezone.now(),
            path=request.path
        )


class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get IP
        client_ip, _ = get_client_ip(request)

        # ✅ Block request if IP is blacklisted
        if client_ip and BlockedIP.objects.filter(ip_address=client_ip).exists():
            return HttpResponseForbidden("Access denied. Your IP is blocked.")

        # ✅ Log request
        RequestLog.objects.create(
            ip_address=client_ip or "unknown",
            timestamp=now(),
            path=request.path
        )

        return self.get_response(request)