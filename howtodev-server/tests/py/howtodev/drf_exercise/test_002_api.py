"Testing API structure"

import rest_framework
import pytest
try:
    from drf_exercise import urls, apis, models
except ImportError:
    pass


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
    @pytest.mark.django_db()
    @pytest.mark.it('can be hit')
    def test_resolve_request(self, client):  # pylint: disable=missing-function-docstring
        assert client.get('/api/v1/employees/').status_code == 200

    @pytest.mark.run(order=11)
    @pytest.mark.django_db()
    @pytest.mark.it('returns a list of employees')
    def test_resolve_employee_list(self, client):  # pylint: disable=missing-function-docstring
        models.Employee.objects.create(name='John')
        models.Employee.objects.create(name='Ben')
        assert client.get('/api/v1/employees/').json() == [{'name': 'John'}, {'name': 'Ben'}]

    @pytest.mark.run(order=12)
    @pytest.mark.django_db()
    @pytest.mark.it('returns a specific employee')
    def test_resolve_employee_list(self, client):  # pylint: disable=missing-function-docstring
        models.Employee.objects.create(name='Jason')
        assert client.get('/api/v1/employees/1/').json() == [{'name': 'John'}]
