from django.utils import timezone
import datetime


def order_time():
    delta = 30
    now = timezone.localtime(timezone.now()) + datetime.timedelta(hours=1, minutes=30)
    with_cook_time = datetime.datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=now.hour,
        minute=(delta * (now.minute // delta) + delta) % 60,
    )
    times = [("fast", "Как можно быстрее")]
    i = 0
    while True:
        new_time1 = with_cook_time + datetime.timedelta(minutes=delta * i)
        new_time2 = with_cook_time + datetime.timedelta(minutes=delta * i + delta)
        if new_time1.hour > 8 or new_time1.hour < 3 and new_time2.hour > 8 or new_time2.hour < 3:
            times.append((new_time2.strftime("%H:%M"), f"{new_time1.strftime('%H:%M')} - {new_time2.strftime('%H:%M')}"))
        else:
            break

        i += 1
    return times
