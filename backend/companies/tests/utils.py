from companies.models import Company
from companies.services import CompanyService


def create_test_company(
    email="test@email.com", password="password", name="name"
) -> Company:
    recuiter = CompanyService().create(email, password, name)
    return recuiter


test_credentials = {
    "email": "test@email.com",
    "password": "password",
    "name": "org",
}
