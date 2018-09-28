import json

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Event

@csrf_exempt
@require_POST
def create(request):
    event = Event(**json.loads(request.body))
    event.save()

    response_code = 200 if event.process() else 422

    return HttpResponse(json.dumps({'status': 'ok'}), content_type='application/json', response_code=response_code)
