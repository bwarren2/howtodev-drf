"Tests that the admin is set up"

import pytest
from django.contrib import admin
from drf_exercise import models


@pytest.mark.describe("The admin")
class TestAdminSetup():
    "Admin checks."

    @pytest.mark.run(order=2)
    @pytest.mark.it("has an employee admin")
    def test_employee_admin_exists(self):
        "Do you have an employee admin?"
        assert admin.site.is_registered(models.Employee)

    @pytest.mark.run(order=3)
    @pytest.mark.it("has a team admin")
    def test_team_admin_exists(self):
        "Do you have a team admin?"
        assert admin.site.is_registered(models.Team)

    @pytest.mark.run(order=4)
    @pytest.mark.it("has a snack admin")
    def test_snack_admin_exists(self):
        "Do you have a snack admin?"
        assert admin.site.is_registered(models.Snack)
