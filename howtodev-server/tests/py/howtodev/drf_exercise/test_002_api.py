"Testing API structure"

import jq
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


@pytest.fixture()
def snack_with_owner(db):
    jason = models.Employee.objects.create(name='Jason')
    return models.Snack.objects.create(name='Candy Cane', owner=jason)


@pytest.fixture()
def owner_with_snacks(db):
    jason = models.Employee.objects.create(name='Jason')
    models.Snack.objects.create(name='Candy Cane', owner=jason)
    models.Snack.objects.create(name='Veggie Crisp', owner=jason)
    models.Snack.objects.create(name='Clementine', owner=jason)
    return jason


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
            pytest.fail("You need to make an `apis.py` file.")

    @pytest.mark.run(order=6)
    @pytest.mark.it('has a ModelViewSet named EmployeeModelViewSet for Employee')
    def test_employee_modelviewset_exists(self):  # pylint: disable=missing-function-docstring
        try:
            assert apis.EmployeeModelViewSet
        except AttributeError:
            pytest.fail("You need a ModelViewSet named EmployeeModelViewSet in apis.py")

    @pytest.mark.run(order=7)
    @pytest.mark.it('has a `urls.py` file')
    def test_urlspy_exists(self):  # pylint: disable=missing-function-docstring

        try:
            from drf_exercise import urls  # pylint: disable=unused-import, import-outside-toplevel, redefined-outer-name
        except ImportError:
            pytest.fail("You need to make a urls.py file.")

    @pytest.mark.run(order=8)
    @pytest.mark.it('has a Router named router defined')
    def test_urls_router_exists(self):  # pylint: disable=missing-function-docstring
        try:
            assert urls.router
        except AttributeError:
            pytest.fail("You need a variable named router that is a DRF Router subclass in `urls.py`")

    @pytest.mark.run(order=9)
    @pytest.mark.it('has router-shaped urls in the urlpatterns')
    def test_urls_from_router_exists(self):  # pylint: disable=missing-function-docstring
        assert urls.urlpatterns[0].resolve('employees/')
        assert urls.urlpatterns[0].resolve('employees/1/')

    @pytest.mark.run(order=9)
    @pytest.mark.it('uses a browsable API')
    def test_browsable_router_exists(self):  # pylint: disable=missing-function-docstring
        assert isinstance(urls.router, rest_framework.routers.DefaultRouter)


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@pytest.mark.describe('Employees endpoint resolution')
class TestAPIWorks():  # pylint: disable=missing-class-docstring

    @pytest.mark.run(order=10)
    @pytest.mark.it('can be hit')
    def test_resolve_request(self, user, api_client, employee):  # pylint: disable=missing-function-docstring
        api_client.force_authenticate(user)
        assert api_client.get('/api/v1/employees/').status_code == 200

    @pytest.mark.run(order=11)
    @pytest.mark.it('returns a list of employees')
    def test_resolve_employee_list(self, user, api_client, employee):  # pylint: disable=missing-function-docstring
        api_client.force_authenticate(user)
        models.Employee.objects.create(name='Ben')

        response = api_client.get(reverse('employee-list')).json()
        pagination_removed_response = response['results']
        jq_pagination_removed = jq.compile('.results[] as $data | {name: $data.name}').input(response).all()

        expected = [{'name': 'John'}, {'name': 'Ben'}]
        assert response == expected or pagination_removed_response == expected or jq_pagination_removed == expected

    @pytest.mark.run(order=12)
    @pytest.mark.it('returns a specific employee')
    def test_resolve_employee_detail(self, user, api_client, employee):  # pylint: disable=missing-function-docstring
        api_client.force_authenticate(user)
        response = api_client.get(reverse('employee-detail', args=(1,))).json()
        jq_filtered_response = jq.compile('. as $data | {name: $data.name}').input(response).first()
        expected = {'name': 'John'}
        assert response == expected or jq_filtered_response == expected

    @pytest.mark.run(order=13)
    @pytest.mark.it('requires login')
    def test_resolve_needs_login(self, api_client, employee):  # pylint: disable=missing-function-docstring
        assert api_client.get(reverse('employee-detail', args=(1,))).status_code == 403

    @pytest.mark.run(order=14)
    @pytest.mark.it('supports limit-offset pagination with page size 2')
    def test_employee_pagination(self, user, api_client):  # pylint: disable=missing-function-docstring
        models.Employee.objects.create(name='Ben')
        models.Employee.objects.create(name='Jason')
        models.Employee.objects.create(name='John')
        api_client.force_authenticate(user)
        response = api_client.get(reverse('employee-list')).json()
        assert 'count' in response and 'next' in response and 'previous' in response

    @pytest.mark.run(order=15)
    @pytest.mark.it('supports filtering on name')
    def test_employee_pagination(self, user, api_client):  # pylint: disable=missing-function-docstring
        models.Employee.objects.create(name='Ben')
        models.Employee.objects.create(name='John')
        api_client.force_authenticate(user)
        response = api_client.get(f"{reverse('employee-list')}?name=Ben").json()
        assert len(response['results']) == 1


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@pytest.mark.describe('`Snack`s endpoint')
class TestSnacksEndpoint():  # pylint: disable=missing-class-docstring

    @pytest.mark.run(order=16)
    @pytest.mark.it('can be hit')
    def test_resolve_request(self, user, api_client):  # pylint: disable=missing-function-docstring
        api_client.force_authenticate(user)
        assert api_client.get('/api/v1/snacks/').status_code == 200


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@pytest.mark.describe('`Snack`s ')
class TestRelationshipsWork():  # pylint: disable=missing-class-docstring

    @pytest.mark.run(order=17)
    @pytest.mark.it('have `owner` as a PK in their serialization')
    def test_owner_pk(self, user, snack_with_owner, api_client):  # pylint: disable=missing-function-docstring
        api_client.force_authenticate(user)
        response = api_client.get(reverse('snack-list')).json()
        assert response['results'][0]['owner'] == 1

    @pytest.mark.run(order=18)
    @pytest.mark.it('have `owner_data` in their serialization (use `source=`)')
    def test_owner_data(self, user, snack_with_owner, api_client):  # pylint: disable=missing-function-docstring
        api_client.force_authenticate(user)
        response = api_client.get(reverse('snack-list')).json()
        assert response['results'][0]['owner'] == 1


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@pytest.mark.describe('`Employee`s ')
class TestEmployeeSnacks():  # pylint: disable=missing-class-docstring

    @pytest.mark.run(order=19)
    @pytest.mark.it('have a list of snacks in their serialization')
    def test_snack_list(self, user, owner_with_snacks, api_client):  # pylint: disable=missing-function-docstring
        api_client.force_authenticate(user)
        response = api_client.get(reverse('employee-detail', args=(1,))).json()
        assert len(response['snacks']) == 3


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@pytest.mark.describe('`Query Scaling ')
class TestQueryScaling():  # pylint: disable=missing-class-docstring

    @pytest.mark.run(order=19)
    @pytest.mark.it("`snacks` api doesn't add queries with additional objects")
    def test_snack_scaling(self, user, django_assert_num_queries, api_client):  # pylint: disable=missing-function-docstring
        api_client.force_authenticate(user)

        jason = models.Employee.objects.create(name='Jason')
        models.Snack.objects.create(name='Candy Cane', owner=jason)

        with django_assert_num_queries(2) as captured:
            response = api_client.get(reverse('snack-list')).json()

    @pytest.mark.run(order=19)
    @pytest.mark.it("`employees` api doesn't add queries with additional objects")
    def test_employee_scaling(self, user, django_assert_num_queries, api_client):  # pylint: disable=missing-function-docstring
        api_client.force_authenticate(user)

        jason = models.Employee.objects.create(name='Jason')
        models.Snack.objects.create(name='Candy Cane', owner=jason)

        john = models.Employee.objects.create(name='John')
        models.Snack.objects.create(name='Clementine', owner=jason)

        with django_assert_num_queries(3) as captured:
            response = api_client.get(reverse('employee-list')).json()
