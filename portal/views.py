from django.shortcuts import render, redirect
from django.views import View
import requests
from django.conf import settings

MULESOFT_URL = settings.MULESOFT_BASE_URL
API_KEY = settings.API_KEY
HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

class LoginPageView(View):
    def get(self, request):
        # If already logged in redirect to dashboard
        if request.session.get('sf_user_id'):
            return redirect('/dashboard/')
        return render(request, 'portal/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            # Call MuleSoft Experience API login endpoint
            response = requests.post(
                f"{MULESOFT_URL}/auth/login",
                json={"email": email, "password": password},
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                data = response.json()
                # Store user info in Django session
                request.session['sf_user_id'] = data['user']['sf_user_id']
                request.session['email'] = data['user']['email']
                request.session['api_key'] = data['api_key']
                return redirect('/dashboard/')
            else:
                return render(request, 'portal/login.html', 
                    {'error': 'Invalid credentials'})
        except Exception as e:
            return render(request, 'portal/login.html', 
                {'error': f'MuleSoft connection failed: {str(e)}'})

class DashboardPageView(View):
    def get(self, request):
        if not request.session.get('sf_user_id'):
            return redirect('/')
        
        sf_user_id = request.session.get('sf_user_id')
        email = request.session.get('email')
        api_key = request.session.get('api_key')
        
        headers = {
            "X-API-Key": api_key,
            "X-SF-User-Id": sf_user_id,
            "Content-Type": "application/json"
        }
        
        try:
            # Fetch records from MuleSoft
            response = requests.get(
                f"{MULESOFT_URL}/records",
                headers=headers
            )
            records = response.json() if response.status_code == 200 else []
        except:
            records = []
        
        return render(request, 'portal/dashboard.html', {
            'records': records,
            'email': email,
            'sf_user_id': sf_user_id
        })

class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect('/')

class CreateRecordView(View):
    def post(self, request):
        if not request.session.get('sf_user_id'):
            return redirect('/')
        
        sf_user_id = request.session.get('sf_user_id')
        api_key = request.session.get('api_key')
        
        headers = {
            "X-API-Key": api_key,
            "X-SF-User-Id": sf_user_id,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{MULESOFT_URL}/records",
                json={
                    "title": request.POST.get('title'),
                    "description": request.POST.get('description'),
                    "sf_user_id": sf_user_id
                },
                headers=headers
            )
            if response.status_code == 201:
                return redirect('/dashboard/')
            else:
                return redirect('/dashboard/?error=create_failed')
        except Exception as e:
            return redirect(f'/dashboard/?error={str(e)}')
