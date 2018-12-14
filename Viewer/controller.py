import datetime

from Cinema.models import PaiDang, ORDERED_PAYED, ORDERED_NOT_PAY
from Viewer.models import ViewerOrder


def get_valid_seats(paidang_id, order_id=0):
    paidang = PaiDang.objects.get(pk=paidang_id)

    h_seats = paidang.p_hall.h_seats

    # orders_payed = paidang.viewerorder_set.filter(v_status=ORDERED_PAYED)
    orders_payed = ViewerOrder.objects.filter(v_paidang_id=paidang_id).filter(v_status=ORDERED_PAYED)

    # orders_locked = paidang.viewerorder_set.filter(v_status=ORDERED_NOT_PAY).filter(v_expire__gt=datetime.datetime.now())
    orders_locked = ViewerOrder.objects.filter(v_paidang_id=paidang_id).filter(v_status=ORDERED_NOT_PAY).filter(v_expire__gt=datetime.datetime.now())

    if order_id != 0:
        print("排除自己")
        orders_locked = orders_locked.exclude(pk=order_id)

    h_seat_list = h_seats.split("#")

    orders_payed_seats = []

    for order_payed in orders_payed:
        orders_payed_seats += order_payed.v_seats.split("#")

    orders_locked_seats = []

    for order_locked in orders_locked:
        orders_locked_seats += order_locked.v_seats.split("#")

    print(h_seat_list)
    print("付款座位",orders_payed_seats)
    print("锁定座位",orders_locked_seats)

    valid_seats = list(set(h_seat_list) - set(orders_payed_seats) - set(orders_locked_seats))

    print("可用座位",valid_seats)

    return valid_seats