"Testing API structure"

import rest_framework
import pytest
from django.contrib.auth.models import User
from django.urls import reverse

try:
    from drf_exercise import urls, apis, models
except ImportError:
    pass


@pytest.fixture()
def employee(db):
    return models.Employee.objects.create(name='John')


@pytest.fixture()
def user(db):
    return User.objects.create(username='user', email='user@domain.com', password='password')


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.mark.describe('Basic Employees endpoint setup')
class TestAPIExists():  # pylint: disable=missing-class-docstring

    @pytest.mark.run(order=5)
    @pytest.mark.it('has an api file')
    def test_apipy_exists(self):  # pylint: disable=missing-function-docstring

        try:
            from drf_exercise import apis  # pylint: disable=unused-import, import-outside-toplevel, redefined-outer-name
        except ImportError:
            pytest.fail("You need to make an api.py file.")

    @pytest.mark.run(order=6)
    @pytest.mark.it('has a ModelViewSet for Employee')
    def test_employee_modelviewset_exists(self):  # pylint: disable=missing-function-docstring
        assert apis.EmployeeModelViewSet

    @pytest.mark.run(order=7)
    @pytest.mark.it('has a urls file')
    def test_urlspy_exists(self):  # pylint: disable=missing-function-docstring

        try:
            from drf_exercise import urls  # pylint: disable=unused-import, import-outside-toplevel, redefined-outer-name
        except ImportError:
            pytest.fail("You need to make a urls.py file.")

    @pytest.mark.run(order=8)
    @pytest.mark.it('has a router defined')
    def test_urls_router_exists(self):  # pylint: disable=missing-function-docstring

        assert urls.router

    @pytest.mark.run(order=9)
    @pytest.mark.it('has router-shaped urls in the urlpatterns')
    def test_urls_from_router_exists(self):  # pylint: disable=missing-function-docstring
        assert urls.urlpatterns[0].resolve('employees/')
        assert urls.urlpatterns[0].resolve('employees/1/')

    @pytest.mark.run(order=9)
    @pytest.mark.it('uses a browsable API')
    def test_browsable_router_exists(self):  # pylint: disable=missing-function-docstring
        assert isinstance(urls.router, rest_framework.routers.DefaultRouter)


@pytest.mark.describe('Employees endpoint resolution')
class TestAPIWorks():  # pylint: disable=missing-class-docstring

    @pytest.mark.run(order=10)
    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    @pytest.mark.it('can be hit')
    def test_resolve_request(self, user, api_client, employee):  # pylint: disable=missing-function-docstring
        api_client.force_authenticate(user)
        assert api_client.get('/api/v1/employees/').status_code == 200

    @pytest.mark.run(order=11)
    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    @pytest.mark.it('returns a list of employees')
    def test_resolve_employee_list(self, user, api_client, employee):  # pylint: disable=missing-function-docstring
        api_client.force_authenticate(user)
        models.Employee.objects.create(name='Ben')
        response = api_client.get(reverse('employee-list')).json()
        expected = [{'name': 'John'}, {'name': 'Ben'}]
        assert response == expected or response['results'] == expected

    @pytest.mark.run(order=12)
    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    @pytest.mark.it('returns a specific employee')
    def test_resolve_employee_detail(self, user, api_client, employee):  # pylint: disable=missing-function-docstring
        api_client.force_authenticate(user)
        response = api_client.get(reverse('employee-detail', args=(1,))).json()
        expected = {'name': 'John'}
        assert response == expected or response['results'] == expected

    @pytest.mark.run(order=13)
    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    @pytest.mark.it('requires login')
    def test_resolve_employee_detail(self, api_client, employee):  # pylint: disable=missing-function-docstring
        assert api_client.get(reverse('employee-detail', args=(1,))).status_code == 403

    @pytest.mark.run(order=14)
    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    @pytest.mark.it('supports limit-offset pagination with page size 2')
    def test_employee_pagination(self, user, api_client):  # pylint: disable=missing-function-docstring
        models.Employee.objects.create(name='Ben')
        models.Employee.objects.create(name='Jason')
        models.Employee.objects.create(name='John')
        api_client.force_authenticate(user)
        response = api_client.get(reverse('employee-list')).json()
        assert 'count' in response and 'next' in response and 'previous' in response
