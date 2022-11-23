import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Sum
from pytz import utc

from core.celery import app
from celery.utils.log import get_task_logger
from wallet.models import Transaction

logger = get_task_logger(__name__)


@app.task
def send_email(email: str, msg: str):
    """Daily Email notification for Wallet users"""
    send_mail(
        "Daily stats from Wallet App!",
        msg,
        settings.EMAIL_HOST_USER,
        email,
        fail_silently=False
    )


@app.task
def form_statistics():
    # daily interval for collecting stats
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    day_before = now - datetime.timedelta(hours=24)

    stats_dict = dict()

    # get expenses queryset
    daily_expenses_qs = Transaction.objects.select_related("user").\
        values("user__email", "user__balance").annotate(sum=Sum("amount")).\
        filter(income=False, time__gte=day_before)
    for q in daily_expenses_qs:
        stats_dict[q['user__email']] = {"expenses": q["sum"], "income": 0, "balance": q["user__balance"]}
    # get incomes queryset
    daily_income_qs = Transaction.objects.select_related("user").\
        values("user__email", "user__balance").annotate(sum=Sum("amount")).\
        filter(income=True, time__gte=day_before)
    # form the statistics dictionary from data for every previous-day-active user
    for q in daily_income_qs:
        if q["user__email"] in stats_dict:
            stats_dict[q["user__email"]]["income"] = q["sum"]
            stats_dict[q["user__email"]]["balance"] = q["user__balance"]
        else:
            stats_dict[q["user__email"]] = {"expenses": 0, "income": q["sum"], "balance": q["user__balance"]}
    for key, value in stats_dict.items():
        stats_dict[key]["total"] = stats_dict[key]["income"] - stats_dict[key]['expenses']

    # form the individual email message and send to user's email
    for email, data in stats_dict.items():

        msg = f"""
        Hi, {email}! We have collected
        some statistics for you!
        {day_before.date()}
        ___________________
        Money spent: {data["expenses"]}
        Money earned: {data["income"]}
        Balance change: {data["total"]}
        
        Current balance: {data["balance"]}
        ___________________
        
        Have a good day using Wallet App!        
        """

        # send_email.delay(email, msg)
        print(msg)
