from .models import RequestLog
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from ipware import get_client_ip   # utile pour récupérer l'IP proprement

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
