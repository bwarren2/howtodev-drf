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


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@pytest.mark.describe("First off, we are going to make a basic endpoint for showing employees.  ")
class TestEmployeeExplainer():  # pylint: disable=missing-class-docstring

    @pytest.mark.run(order=5)
    @pytest.mark.it('OK?  OK!')
    def test_ok(self):  # pylint: disable=missing-function-docstring
        assert True


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@pytest.mark.describe("""
################################################################################
First off, we are going to make a basic endpoint for showing employees.
The major goal here is to make the right files, and have the right variables in
them.  Use a ModelViewSet and look at the Routers documentation:
https://www.django-rest-framework.org/api-guide/viewsets/
https://www.django-rest-framework.org/api-guide/routers/
################################################################################
""")
class TestEmployeeExplainer():  # pylint: disable=missing-class-docstring

    @pytest.mark.run(order=5)
    @pytest.mark.it('OK?  OK!')
    def test_ok(self):  # pylint: disable=missing-function-docstring
        assert True


@pytest.mark.describe('Basic Employees endpoint setup')
class TestAPIExists():  # pylint: disable=missing-class-docstring

    @pytest.mark.run(order=5)
    @pytest.mark.it('has an apis.py file')
    def test_apipy_exists(self):  # pylint: disable=missing-function-docstring

        try:
            from drf_exercise import apis  # pylint: disable=unused-import, import-outside-toplevel, redefined-outer-name
        except ImportError:
            pytest.fail("You need to make an `apis.py` file.")

    @pytest.mark.run(order=6)
    @pytest.mark.it('has a ModelViewSet named EmployeeModelViewSet for Employee in apis.py')
    def test_employee_modelviewset_exists(self):  # pylint: disable=missing-function-docstring
        try:
            assert apis.EmployeeModelViewSet
            assert issubclass(apis.EmployeeModelViewSet, rest_framework.viewsets.ModelViewSet)
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
    @pytest.mark.it('has a Router named router defined in urls.py')
    def test_urls_router_exists(self):  # pylint: disable=missing-function-docstring
        try:
            assert urls.router
            assert isinstance(urls.router, rest_framework.routers.SimpleRouter)
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
@pytest.mark.describe("""
################################################################################
Now let's make sure the API works.  Everything here can be done with basic attrs
like queryset and serializer_class on ModelViewSet
################################################################################
""")
class TestEmployeeResolveExplainer():  # pylint: disable=missing-class-docstring

    @pytest.mark.run(order=10)
    @pytest.mark.it("Let's go")
    def test_ok(self):  # pylint: disable=missing-function-docstring
        assert True


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
    def test_employee_filtering(self, user, api_client):  # pylint: disable=missing-function-docstring
        models.Employee.objects.create(name='Ben')
        models.Employee.objects.create(name='John')
        api_client.force_authenticate(user)
        response = api_client.get(f"{reverse('employee-list')}?name=Ben").json()
        assert len(response['results']) == 1


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@pytest.mark.describe("""
################################################################################
Good job!  We are going to use a more complex data model with a relationship
here, so we need a Snack endpoint as well.  It's much like the Employee one for
now.
################################################################################
""")
class TestSnackResolveExplainer():  # pylint: disable=missing-class-docstring

    @pytest.mark.run(order=16)
    @pytest.mark.it("I'm ready")
    def test_ok(self):  # pylint: disable=missing-function-docstring
        assert True


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
@pytest.mark.describe("""
################################################################################
Django will helpfully run queries in the background to fill out attributes you
reference but did not pull in your original query.  This can cause scaling
problems when you pull 100 objects and they each run a couple queries.  This
part is solving those problems by optimizing querysets.
################################################################################
""")
class TestSnackResolveExplainer():  # pylint: disable=missing-class-docstring

    @pytest.mark.run(order=20)
    @pytest.mark.it("Lemme at em")
    def test_ok(self):  # pylint: disable=missing-function-docstring
        assert True


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@pytest.mark.describe('`Query Scaling ')
class TestQueryScaling():  # pylint: disable=missing-class-docstring

    @pytest.mark.run(order=20)
    @pytest.mark.it("`snacks` api doesn't add queries with additional objects")
    def test_snack_scaling(self, user, django_assert_num_queries, api_client):  # pylint: disable=missing-function-docstring
        api_client.force_authenticate(user)

        jason = models.Employee.objects.create(name='Jason')
        models.Snack.objects.create(name='Candy Cane', owner=jason)

        with django_assert_num_queries(2) as captured:
            response = api_client.get(reverse('snack-list')).json()

    @pytest.mark.run(order=21)
    @pytest.mark.it("`employees` api doesn't add queries with additional objects")
    def test_employee_scaling(self, user, django_assert_num_queries, api_client):  # pylint: disable=missing-function-docstring
        api_client.force_authenticate(user)

        jason = models.Employee.objects.create(name='Jason')
        models.Snack.objects.create(name='Candy Cane', owner=jason)

        john = models.Employee.objects.create(name='John')
        models.Snack.objects.create(name='Clementine', owner=jason)

        with django_assert_num_queries(3) as captured:
            response = api_client.get(reverse('employee-list')).json()


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@pytest.mark.describe('Count/Exist attributes ')
class TestCounts():  # pylint: disable=missing-class-docstring

    @pytest.mark.run(order=22)
    @pytest.mark.it("has_snack and num_snacks exist for `Employee` serialization")
    def test_snack_annotations(self, user, owner_with_snacks, api_client):  # pylint: disable=missing-function-docstring
        api_client.force_authenticate(user)

        response = api_client.get(reverse('employee-detail', args=(1,))).json()
        assert response['num_snacks'] == 3
        assert response['has_snacks'] == True

    @pytest.mark.run(order=23)
    @pytest.mark.it("has_snacks_serializer_approach exists on `Employee`")
    def test_snack_serializermethod(self, user, owner_with_snacks, api_client):  # pylint: disable=missing-function-docstring
        api_client.force_authenticate(user)

        response = api_client.get(reverse('employee-detail', args=(1,))).json()
        assert response['has_snacks_serializer_approach'] == True


@pytest.mark.django_db(transaction=True, reset_sequences=True)
@pytest.mark.describe('Nested Snack Router')
class TestCounts():  # pylint: disable=missing-class-docstring

    @pytest.mark.run(order=24)
    @pytest.mark.it("exists in urls with name `employee-snacks-list`")
    def test_snack_nesting(self, user, owner_with_snacks, api_client):  # pylint: disable=missing-function-docstring
        api_client.force_authenticate(user)

        response = api_client.get(reverse('employee-snacks-list', kwargs={'employee_pk': 1}))
        assert response.status_code == 200

    @pytest.mark.run(order=24)
    @pytest.mark.it("on GET, restricts results to the URL-matching owner")
    def test_snack_get(self, user, api_client):  # pylint: disable=missing-function-docstring
        api_client.force_authenticate(user)
        jason = models.Employee.objects.create(name='Jason')
        models.Snack.objects.create(name='Candy Cane', owner=jason)

        john = models.Employee.objects.create(name='John')
        models.Snack.objects.create(name='Apple', owner=john)

        response = api_client.get(reverse('employee-snacks-list', kwargs={'employee_pk': 1}))
        assert len(response.json()['results']) == 1

    @pytest.mark.run(order=25)
    @pytest.mark.it("on POST, gets the employee ID to use from the url")
    def test_snack_post(self, user, owner_with_snacks, api_client):  # pylint: disable=missing-function-docstring
        api_client.force_authenticate(user)
        models.Employee.objects.create(name='John')

        response = api_client.post(
            reverse('employee-snacks-list', kwargs={'employee_pk': 1}), {'owner': 2, 'name': 'Chocolate'})
        assert response.json()['owner'] == 1
