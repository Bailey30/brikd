from django.db.models import QuerySet
from favourites.models import Favourite
from jobs.models import Job


class FavouriteService:
    def create(self, job_id, user) -> Favourite:
        job = Job.objects.get(id=job_id)
        favourite = Favourite.objects.create(user=user, job=job)
        return favourite

    def list(self, user) -> QuerySet[Favourite]:
        favourites = Favourite.objects.filter(user=user)
        return favourites

    def delete(self, job_id, user) -> None:
        job = Job.objects.get(id=job_id)
        favourite = Favourite.objects.get(user=user, job=job)
        favourite.delete()
