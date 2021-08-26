from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict

from rest_api.json import AuthorizedJsonRequest
from users.auth import authenticate_request
from .models import Employee


@require_http_methods(['GET', 'POST'])
@authenticate_request
def index(request: AuthorizedJsonRequest) -> HttpResponse:
    if request.method == 'GET':
        return __list_employees(request)
    else:
        return __create_employee(request)


@require_http_methods(['GET', 'PUT', 'DELETE'])
@authenticate_request
def resource(request: AuthorizedJsonRequest, pk: int) -> HttpResponse:
    if request.method == 'GET':
        return __show(request, pk)
    elif request.method == 'PUT':
        return __update(request, pk)
    else:
        return __delete(request, pk)


def __show(request: AuthorizedJsonRequest, pk: int) -> HttpResponse:
    employee = Employee.objects.get(pk=pk)
    return JsonResponse({
        'data': model_to_dict(employee)
    })


def __update(request: AuthorizedJsonRequest, pk: int) -> HttpResponse:
    employee_params = request.json.get('employee', {})
    employee_queryset = Employee.objects.filter(pk=pk)
    employee_queryset.update(**employee_params)
    return JsonResponse({
        'data': model_to_dict(employee_queryset[0])
    })


def __delete(request: AuthorizedJsonRequest, pk: int) -> HttpResponse:
    Employee.objects.get(pk=pk).delete()
    return HttpResponse(status=204)


def __list_employees(request: AuthorizedJsonRequest) -> HttpResponse:
    all_employees = list(Employee.objects.values())
    return JsonResponse({
        'data': all_employees,
    })


def __create_employee(request: AuthorizedJsonRequest) -> HttpResponse:
    employee_params = request.json.get('employee', {})
    employee = Employee(**employee_params)
    employee.save()
    return JsonResponse(
        data={
            'data': model_to_dict(employee)
        },
        status=201,
    )
