from django.http import JsonResponse


# Liveness check: used by the frontend status badge and (later) docker healthcheck.
# Plain function-based view — no DRF machinery needed here.
def health(request):
    return JsonResponse({"status": "ok"})
