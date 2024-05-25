from django.utils import timezone
import datetime


def order_time():
    now = timezone.localtime(timezone.now()) + datetime.timedelta(hours=1, minutes=30)
    with_cook_time = datetime.datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=now.hour,
        minute=(15 * (now.minute // 15) + 15) % 60,
    )
    times = [("fast", "Как можно быстрее")]
    for i in range(10):
        new_time = with_cook_time + datetime.timedelta(minutes=15 * i)
        if new_time.hour > 8 or new_time.hour < 3:
            times.append((new_time.strftime("%H:%M"), new_time.strftime("%H:%M")))
    return times
