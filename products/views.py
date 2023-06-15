import json
import boto3
from django.http      import JsonResponse
from django.views     import View
from django.db.models import Sum, Q
from core.utils import AuthorizeProduct, authorization
from my_settings import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY

from products.models  import Apt

class AptView(View):
    @AuthorizeProduct
    def get(self, request):
        try:
            region     = request.GET.get('region', None)
            location = request.GET.get('location', None)
            limit    = int(request.GET.get('limit', 100))
            offset   = int(request.GET.get('offset', 0))
            q = Q()
            location_mapping = None
            mapping = {
                "region"     : "location__region",
                "location" : "location"
            }

            if region:
                q &= Q(location__region__name=region)
                location_mapping = mapping["region"]
                        
            if location:
                q &= Q(location__name=location)
                location_mapping = mapping["location"]

            apts = Apt.objects.select_related(location_mapping).filter(q)

            apts_list = [{
                        'id'                  : apt.id,
                        'name'                : apt.name,
                        'address'             : apt.address,
                        'type'                : apt.type.name,
                        'thumbnail_image_url' : apt.thumbnail_image_url,
                        'location'            :{
                            'name'    : apt.location.region.name,
                            'location': apt.location.name
                        },
                        'open_date'           : apt.open_date,
                        'quantity'            : apt.quantity,
                        'area'                : apt.area,
                        'status'              : apt.status.status,
                    } for apt in apts]
            return JsonResponse({'apts_list': apts_list}, status = 200)

        except Apt.DoesNotExist:
            return JsonResponse({'message':'NOT_FOUND'}, status=404)

        except AttributeError:
            return JsonResponse({'message' : 'AttributeError'}, status=400)

        except TypeError:
            return JsonResponse({'message' : 'TypeError'}, status=400)
        
class AptDetailView(View):
    @AuthorizeProduct
    def get(self, request, apt_id):
        try:
            apt = Apt.objects.get(id=apt_id)
            images = apt.image_set.all()
            data = {
                    'name'                : apt.name,
                    'address'             : apt.address,
                    'type'                : apt.type.name,
                    'thumbnail_image_url' : apt.thumbnail_image_url,
                    'location'            : apt.location.name,
                    'region'              : apt.location.region.name,
                    'open_date'           : apt.open_date,
                    'quantity'            : apt.quantity,
                    'area'                : apt.area,
                    'status'              : apt.status.status,
                    'image_list'          : [{
                        'id' : image.id,
                        'url': image.url
                    } for image in images]
                }
            '''
            sqs = boto3.client(
                'sqs',
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name='ap-northeast-2')

            queue_url = 'https://sqs.ap-northeast-2.amazonaws.com/112382062739/page-view'

            sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=product.korean_name
            )
            '''
            return JsonResponse({'apt_list':data}, status = 201)
                
        except Apt.DoesNotExist:
            return JsonResponse({'message':'NOT_FOUND'}, status=401)
