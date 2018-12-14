from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.views import APIView

from Common.models import Movie


class TicketTopAPIView(APIView):

    def get(self, request, *args, **kwargs):

        movies = Movie.objects.annotate(price_total=Sum("paidang__viewerorder__v_price")).order_by("-price_total")

        print(movies)

        print(movies.query)

        for movie in movies:
            print(movie.m_name, movie.price_total)

        data = {
            "msg": "ok",
            "status": 200
        }

        return Response(data)
