import json
import boto3
from enum               import Enum
from datetime import datetime
from django.db.utils    import IntegrityError
from django.http        import JsonResponse
from django.http.cookie import parse_cookie
from django.views       import View
from django.db          import DatabaseError, transaction
from django.db.models   import Sum, F

from users.models    import User
from products.models import Apt
from orders.models   import Application, AppStatus
from core.utils      import authorization

class ApplicationListView(View):
    @authorization
    def get(self, request):
        user  = request.user
        apps = Application.objects.select_related('apt').filter(user=user)
        print(apps[0].apt.name)
        if not Application.objects.filter(user=user).exists():
            return JsonResponse({"message" : "CART_NOT_EXIST"}, status=400)
        
        result = [{
            'app_id'              : app.id,
            'apt_id'              : app.apt.id,
            'location'            : app.apt.location.name,
            'region'              : app.apt.location.region.name,
            'name'                : app.apt.name,
            'thumbnail_image_url' : app.apt.thumbnail_image_url,
            'status'              : app.status.status
        } for app in apps ]

        return JsonResponse({"app_info" : result}, status=200)

    
class ApplicationStatusEnum(Enum):
    DONE    = 1
    SUCCESS = 2
    FAIL    = 3

class ApplicationView(View):
    @authorization
    def post(self, request):
        data     = json.loads(request.body)
        user     = request.user
        print(data)
        apt_id = int(data[0]['apt_id'])

        try: 
            with transaction.atomic():
                application = Application.objects.create(
                    apt    = Apt.objects.get(id=apt_id),
                    user   = user,
                    status = AppStatus.objects.get(id=ApplicationStatusEnum.DONE.value),
                )
                '''
                sqs = boto3.client(
                    'sqs',
                    aws_access_key_id=AWS_ACCESS_KEY,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name='ap-northeast-2')

                queue_url = 'https://sqs.ap-northeast-2.amazonaws.com/112382062739/order-result'

                sqs.send_message(
                    QueueUrl=queue_url,
                    MessageBody='ORDER_SUCCESS'
                )
                '''
            return JsonResponse({'message':application.id}, status=201)
        
        except transaction.TransactionManagementError:
            return JsonResponse({'message':'TransactionManagementError'}, status=401)                                                                                                                      
        
    @authorization
    def get(self, request):
        user        = request.user
        order       = request.GET.get('id',)
        order_items = Application.objects.get(id=order).orderitem_set.all()
        total_price = int(Application.objects.filter(id=order).annotate(total=Sum(F('orderitem__product__price')*F('orderitem__quantity')))[0].total)
    
        order_list = [{
            'order_id'     : order,
            'user'         : User.objects.get(id=user.id).name,
            'address'      : Application.objects.get(id=order).address,
            'order_items'  : [{
                'product_id'    : order_item.product.id,
                'quantity'      : order_item.quantity,
                'product_name'  : order_item.product.korean_name,
                'product_image' : order_item.product.thumbnail_image_url,
                'price'         : int((order_item.quantity) * (order_item.product.price))
            } for order_item in order_items],
            'total_price'  : total_price
        }]
        
        return JsonResponse({'order_list':order_list}, status=200)

    @authorization
    def patch(self, request):
        data     = json.loads(request.body)
        order_id = data['order_id']  
        
        try:
            Application.objects.filter(id=order_id).update(order_status=ApplicationStatusEnum.FAIL.value)
            return JsonResponse({'message':'SUCCESS'}, status=200)
        
        except KeyError: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


class OrderFailedView(View):
    @authorization
    def post(self, request):
        data = json.loads(request.body)
        user = request.user
        items = data

        try:
            with transaction.atomic():
                order = Application.objects.create(
                    address=User.objects.get(id=user.id).address,
                    user=user,
                    order_status=AppStatus.objects.get(id=ApplicationStatusEnum.ORDER_FAILED.value)
                );
            return JsonResponse({'message': order.id}, status=201)

        except transaction.TransactionManagementError:
            return JsonResponse({'message': 'TransactionManagementError'}, status=401)