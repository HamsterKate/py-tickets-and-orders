from django.db import transaction
from db.models import Order, Ticket, MovieSession
from django.db.models import QuerySet

from django.contrib.auth import get_user_model

User = get_user_model()


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> Order:
    """
    tickets: list of dicts with keys: row, seat, movie_session
    username: str, user who creates the order
    date: optional str, sets created_at
    """
    user = User.objects.get(username=username)

    with transaction.atomic():
        order_data = {"user": user}
        if date:
            order_data["created_at"] = date
        order = Order.objects.create(**order_data)

        for ticket in tickets:
            movie_session = MovieSession.objects.get(id=ticket["movie_session"])
            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )

    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
