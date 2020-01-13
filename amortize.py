from calendar import monthrange
from datetime import datetime
from typing import List


def amortize(amount_cents: int, start_date: datetime, end_date: datetime) -> List[int]:
    amortize_payments: List[int] = list()
    if start_date > end_date:
        return amortize_payments
    start_month, end_month = start_date.month, end_date.month
    start_day, end_day = start_date.day, end_date.day
    start_year, end_year = start_date.year, end_date.year
    _, start_month_days = monthrange(start_year, start_month)
    _, end_month_days = monthrange(end_year, end_month)
    start_month_ratio, end_month_ratio = 1, 1
    partial_months = 0
    partial_months_ratio = 0
    if start_day != 1:
        start_month_ratio, partial_months, = (start_month_days-start_day)/start_month_days, 1
        partial_months_ratio += start_month_ratio
    if end_day != end_month_days:
        end_month_ratio, partial_months = end_day/end_month_days, partial_months+1
        partial_months_ratio += end_month_ratio

    full_months = (end_year - start_year) * 12 + end_month - start_month + 1 - partial_months
    if full_months <= 1 and start_month == end_month:
        return [amount_cents]

    amount_per_month = int(amount_cents//(full_months+partial_months_ratio))
    total_months = full_months+partial_months
    remaining_amount = amount_cents
    for i in range(total_months):
        monthly_payment = amount_per_month
        if i == 0:
            monthly_payment = int(start_month_ratio * amount_per_month)
        if i == total_months-1:
            monthly_payment = int(end_month_ratio * amount_per_month)
        remaining_amount -= monthly_payment
        amortize_payments.append(monthly_payment)
    i = 0
    while remaining_amount != 0:
        if full_months != 0:
            if i == 0 and start_month_ratio != 1:
                i += 1
                continue
            if i == total_months-1 and end_month_ratio != 1:
                i += 1
                continue
        amortize_payments[i] += 1
        remaining_amount -= 1
        i += 1
        if i == total_months:
            i = 0
    return amortize_payments
