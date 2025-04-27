from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import subprocess, os, re

SCRIPTS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

def index(request):
    return render(request, 'index.html')

@require_POST
@csrf_exempt
def network_scanner(request):
    network = request.POST.get('network')
    if not network:
        return JsonResponse({"message": "No network provided"}, status=400)
    
    if not re.match(r'^(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}$', network):
        return JsonResponse({"message": "Invalid network format"}, status=400)

    try:
        result = subprocess.run(
            ['python3', os.path.join(SCRIPTS_PATH, 'network-scanner.py'), '-n', network],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print(result.stdout)
            return JsonResponse({"message": result.stdout}, status=200)
        else:
            print(result.stderr)
            return JsonResponse({"message": result.stderr}, status=500)

    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)