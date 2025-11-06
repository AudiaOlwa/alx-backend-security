from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

SENSITIVE_PATHS = ['/admin', '/login']

@shared_task
def detect_suspicious_ips():
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # Trouver IPs avec +100 requêtes en 1h
    heavy_ips = (
        RequestLog.objects
        .filter(timestamp__gte=one_hour_ago)
        .values('ip_address')
        .annotate(count=models.Count('ip_address'))
        .filter(count__gt=100)
    )

    for entry in heavy_ips:
        SuspiciousIP.objects.get_or_create(
            ip_address=entry['ip_address'],
            reason="Exceeded 100 requests per hour"
        )

    # Trouver IPs qui touchent des pages sensibles
    suspicious_logs = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=SENSITIVE_PATHS
    ).values_list('ip_address', flat=True)

    for ip in set(suspicious_logs):
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            reason="Accessed sensitive paths"
        )
