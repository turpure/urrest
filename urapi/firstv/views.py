from django.shortcuts import render,HttpResponse
from firstv.models import FeedBack
from django.http import JsonResponse
import json
# from  firstv.tasks import get_ebay_json
from firstv.dbtools.ebaydata import get_feedback_json
from firstv.dbtools.purchaser import filter_sku
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@csrf_exempt
def ebay_account_feedback(request):
    if request.method == 'POST' :
        sellername = request.POST.get('ebayid')
        # response = get_ebay_json.delay(sellername)
        response = get_feedback_json(sellername)
        return HttpResponse(response,content_type='application/json; charset=utf8')


@csrf_exempt
def sku_generator(request):
    response = filter_sku()
    return HttpResponse(response,content_type='application/json; charset=utf8')


