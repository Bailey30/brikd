from django.contrib.auth import get_user_model
from users.models import User


BaseUser = get_user_model()


class UserService:
    def create(
        self, email: str, password: str, name: str, search_postcode=None
    ) -> User:
        profile = BaseUser.objects.create_user(  # pyright: ignore
            email=email,
            password=password,
            is_active=True,
            is_admin=False,
            account_type="jobseeker",
        )

        user = User.objects.create(
            profile=profile, name=name, search_postcode=search_postcode
        )

        return user

    def get(self, id: str) -> User:
        user = User.objects.get(profile_id=id)
        return user
