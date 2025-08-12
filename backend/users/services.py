from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from common.service_utils import update_model
from common.utils import get_postcode_coordinates
from users.models import User


BaseUser = get_user_model()


class UserService:
    def create(
        self,
        email: str,
        password: str,
        name: str,
        search_postcode=None,
        phone_number=None,
        distance_alerts=False,
        alert_radius=0,
    ) -> User:
        coordinates = (
            get_postcode_coordinates(search_postcode) if search_postcode else None
        )

        profile = BaseUser.objects.create_user(  # pyright: ignore
            email=email,
            password=password,
            is_active=True,
            is_admin=False,
            account_type="jobseeker",
        )

        coordinates_point = Point(0, 0)
        if coordinates:
            coordinates_point = Point(
                coordinates["longitude"],
                coordinates["latitude"] if coordinates else None,
            )

        user = User.objects.create(
            profile=profile,
            name=name,
            search_postcode=search_postcode,
            search_postcode_coordinates=coordinates_point,
            phone_number=phone_number,
            distance_alerts=distance_alerts,
            alert_radius=alert_radius,
        )

        return user

    def get(self, id: str) -> User:
        user = User.objects.get(profile_id=id)
        return user

    def update(self, user: User, data: dict) -> User:
        user, _ = update_model(user, data)
        return user
