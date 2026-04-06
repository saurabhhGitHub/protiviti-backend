from django.http import JsonResponse
from decouple import config

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.api_key = config('API_KEY', default='')
        self.exact_exempt_paths = [
            '/health',
            '/portal/health',
            '/auth/login',
            '/portal/auth/login',
            '/portal/',
            '/portal/dashboard/',
            '/',
            '/favicon.ico'
        ]

    def __call__(self, request):
        path = request.path_info
        
        if path in self.exact_exempt_paths or path.startswith('/admin/'):
            return self.get_response(request)
            
        api_key_header = request.headers.get('X-API-Key')
        
        if not api_key_header or api_key_header != self.api_key:
            return JsonResponse({"code": 401, "message": "Invalid or missing API Key"}, status=401)
            
        return self.get_response(request)
