from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from rest_api.json import AuthorizedJsonRequest
from users.auth import authenticate_request
from .models import Employee


@require_http_methods(['GET', 'POST'])
@authenticate_request
def index(request: AuthorizedJsonRequest) -> HttpResponse:
    if request.method == 'GET':
        return list_employees(request)
    else:
        return create_employee(request)


def list_employees(request: AuthorizedJsonRequest) -> HttpResponse:
    all_employees = list(Employee.objects.values())
    return JsonResponse({
        'data': all_employees,
    })


def create_employee(request: AuthorizedJsonRequest) -> HttpResponse:
    employee = request.json.get('employee', {})
    Employee(**employee).save()
    return JsonResponse(
        data={
            'data': employee
        },
        status=201,
    )
