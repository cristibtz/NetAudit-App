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
    
@require_POST
@csrf_exempt
def port_scanner(request):
    ip = request.POST.get("ip")
    mode = request.POST.get("mode")
    if not ip:
        return JsonResponse({"message": "No IP provided"}, status=400)
    elif not re.match(r'^(?:\d{1,3}\.){3}\d{1,3}$', ip):
        return JsonResponse({"message": "Invalid IP format"}, status=400)
    if not mode:
        return JsonResponse({"message": "No mode provided"}, status=400)
    elif mode not in ["1", "2", "3"]:
        return JsonResponse({"message": "Invalid mode"}, status=400)
    
    try:
        result = subprocess.run(
            ['python3', os.path.join(SCRIPTS_PATH, 'port-scanner.py'), '-u', ip, '-t 48', '-m', mode],
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
    
@require_POST
@csrf_exempt
def web_fuzzer(request):
    url = request.POST.get("url")
    if not url:
        return JsonResponse({"message": "No URL provided"}, status=400)
    
    if not re.match(r'^(http|https)://[a-zA-Z0-9.-]+(:\d+)?$', url):
        return JsonResponse({"message": "Invalid URL format"}, status=400)

    try:
        result = subprocess.run(
            ['python3', 
            os.path.join(SCRIPTS_PATH, 'web-fuzzer.py'), 
            '-u', url, 
            '-t', '48', 
            '-w', os.path.join(SCRIPTS_PATH, 'default-wordlist.txt'), 
            '--web-script'],
            capture_output=True, 
            text=True,
        )
        
        if result.returncode == 0:
            return JsonResponse({"message": result.stdout}, status=200)
        else:
            return JsonResponse({"message": result.stderr}, status=500)
    
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)