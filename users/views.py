import json, bcrypt, jwt

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError

from .models                import User
from core.validators        import email_validate, password_validate
from my_settings            import SECRET_KEY, ALGORITHM


class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            email_validate(data['email'])
            password_validate(data['password'])

            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message' : 'INVALID_USER'}, status=401)

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                name         = data['name'],
                email        = data['email'],
                password     = hashed_password,
            )
            return JsonResponse({'message' : 'SUCCESS'}, status=201)

        except ValidationError as e:
            return JsonResponse({'message' : e.message}, status=400)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class SigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(email = data['email'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message' : 'INVALID_USER'}, status=401)

            token=jwt.encode({'user':user.id},SECRET_KEY,algorithm=ALGORITHM)

            return JsonResponse({
                'message' : 'SUCCESS',
                'access_token':token
            },status=200)
                
        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)
        
        except ValidationError as e:
            return JsonResponse({'message' : e.message}, status = 401)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

class IdCheckingView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email_validate(data['email'])

            user = User.objects.filter(email = data['email'])
            
            if user.exists():
                return JsonResponse({'message' : 'EMAIL_EXISTS'}, status=401)
            else:
                return JsonResponse({'message' : 'FINE_TO_USE'}, status=200)

        except ValidationError as e:
            return JsonResponse({'message' : e.message}, status = 401) 