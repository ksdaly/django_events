import json

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Rule

@csrf_exempt
@require_POST
def create(request):
    event = Rule(**json.loads(request.body))
    event.save()

    return HttpResponse(json.dumps({'status': 'ok'}), content_type='application/json')
