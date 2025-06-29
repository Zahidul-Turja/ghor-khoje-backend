import random
from django.db.models import Q, Avg, Sum
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from ghorkhoje.settings import OTP_LENGTH
from user.models import User, Notification, Review

from user.serializers import UserProfileSerializer
from utils.responses import custom_exception
from utils.services import send_custom_email

from booking.models import Booking
from place.models import Place
from datetime import date
from calendar import month_name
from collections import defaultdict


def send_otp_email(recipient_email, otp):
    subject = "Ghor Khojee - Verify OTP Code"
    from_email = settings.EMAIL_HOST_USER
    to = [recipient_email]

    text_content = f"Your OTP is: {otp}"  # fallback for non-HTML clients

    html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f9f9f9;">
            <div style="max-width: 500px; margin: auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
            <h2 style="text-align: center; color: #333333;">Verify Your Email</h2>
            <p style="font-size: 16px; color: #555;">Use the OTP below to verify your email address:</p>
            <div style="display: flex; justify-content: center; align-items: center; gap: 10px; margin: 20px 0;">
                {''.join([f'<div style="width: 40px; height: 50px; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; background-color: #eef2f7; border: 1px solid #ccc; border-radius: 5px;">{digit}</div>' for digit in otp])}
            </div>
            <p style="font-size: 14px; color: #999;">This OTP is valid for 10 minutes. Please do not share it with anyone.</p>
            </div>
        </body>
        </html>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def generate_otp():
    # return "1234"
    return "".join(random.choices("0123456789", k=OTP_LENGTH))


def user_registration_service(payload):
    otp = generate_otp()
    payload["otp"] = otp
    payload.pop("confirm_password", None)

    user = User.objects.create_user(**payload)

    Notification.objects.create(
        user=user,
        title="Account Created",
        message="Your account has been created successfully.",
        type="success",
        is_read=False,
    )

    # send_custom_email(
    #     "Ghor Khojee OTP Verification",
    #     f"Your One Time Password (OTP) is: {otp}",
    #     [user.email],
    # )

    send_otp_email(user.email, otp)
    print(f"Generated OTP: {otp}")
    return user


def resend_otp_service(payload):
    email = payload.get("email")
    user = User.objects.filter(email=email).first()

    if user is None:
        custom_exception("User does not exist.")

    otp = generate_otp()
    user.otp = otp
    user.save()

    # send_custom_email(
    #     "Ghor Khojee OTP Verification",
    #     f"Your One Time Password (OTP) is: {otp}",
    #     [user.email],
    # )

    send_otp_email(user.email, otp)
    print(f"Resent OTP: {otp}")
    return True


def otp_verification_service(payload):
    email = payload.get("email")
    otp = payload.get("otp")
    user = User.objects.filter(email=email).first()

    if user is None or user.otp != otp:
        return False

    user.is_active = True
    user.otp = ""
    user.save()

    Notification.objects.create(
        user=user,
        title="Welcome to Ghor Khojee",
        message="Your account has been verified successfully.",
        type="success",
        is_read=False,
    )

    return True


def user_login_service(payload, request):
    email = payload.get("email")
    password = payload.get("password")

    try:
        user = User.objects.get(email=email)
        if user.is_active is False:
            custom_exception("User is not active. Please verify your email first.")
    except User.DoesNotExist:
        custom_exception("User does not exist.")

    if not user.check_password(password):
        custom_exception("Invalid credentials.")

    token = RefreshToken.for_user(user)
    update_last_login(None, user)

    serializer = UserProfileSerializer(user, context={"request": request})
    user = serializer.data

    return {
        "user": user,
        "access_token": str(token.access_token),
        "refresh_token": str(token),
    }


def resend_otp_service(payload):
    email = payload.get("email")
    user = User.objects.filter(email=email).first()

    if user is None:
        custom_exception("No user found with this email. Please sign up first.")

    otp = generate_otp()
    user.otp = otp
    user.save()

    send_otp_email(user.email, otp)
    print(f"Resent OTP: {otp}")
    return True


def forget_password_service(payload):
    email = payload.get("email")
    password = payload.get("password")
    user = User.objects.filter(email=email).first()

    if user is None:
        custom_exception("User does not exist.")

    otp = generate_otp()
    user.otp = otp
    user.set_password(password)
    user.is_active = False
    user.save()

    send_otp_email(user.email, otp)

    return True


# Analytics service to fetch user statistics
def get_stats(request):
    bookings = Booking.objects.filter(
        place__owner=request.user, status="accepted"
    ).all()
    places = Place.objects.filter(owner=request.user).all()
    today = date.today()

    # Total Revenue
    total_rev = 0
    total_rev_prev = 0
    for b in bookings:
        move_in = b.move_in_date
        if move_in and move_in > today:
            continue  # skip future bookings
        months = (today.year - move_in.year) * 12 + (today.month - move_in.month)
        total_rev += months * b.rent_per_month
        total_rev_prev += (months - 1) * b.rent_per_month

    change = total_rev - total_rev_prev
    color = "green" if change > 0 else "red"

    # Total Bookings
    first_day_this_month = date(today.year, today.month, 1)

    # Filter bookings by month for current user
    bookings_this_month = Booking.objects.filter(
        place__owner=request.user,
        move_in_date__gte=first_day_this_month,
        move_in_date__lte=today,
    ).count()

    # Avg Rating
    avg_overall = Review.objects.filter(reviewee=request.user).aggregate(
        avg=Avg("overall")
    )["avg"]

    first_day_this_month = today.replace(day=1)

    # --- 1. Reviews before this month ---
    prev_reviews_qs = Review.objects.filter(
        reviewee=request.user, created_at__lt=first_day_this_month
    )
    avg_prev = prev_reviews_qs.aggregate(avg=Avg("overall"))["avg"]

    # --- 2. Reviews from this month ---
    this_month_reviews_qs = Review.objects.filter(
        reviewee=request.user, created_at__gte=first_day_this_month
    )
    avg_this_month = this_month_reviews_qs.aggregate(avg=Avg("overall"))["avg"]

    if avg_prev is not None and avg_this_month is not None:
        if avg_this_month > avg_prev:
            review_color = "green"
        elif avg_this_month < avg_prev:
            review_color = "red"
        else:
            review_color = "gray"
    elif avg_this_month is not None and avg_prev is None:
        review_color = "green"
    elif avg_this_month is None:
        review_color = "gray"
    else:
        review_color = "gray"

    # Occupancy Rate
    bookings_before_this_month = Booking.objects.filter(
        place__owner=request.user, created_at__lt=first_day_this_month
    ).count()

    rating_change = (avg_prev or 0) - (avg_overall or 0)

    stats = [
        {
            "title": "Total Revenue",
            "value": total_rev,
            "change": change,
            "icon": "DollarSign",
            "color": color,
        },
        {
            "title": "Total Bookings",
            "value": bookings.count(),
            "change": bookings_this_month,
            "icon": "Calendar",
            "color": "blue" if bookings_this_month > 0 else "gray",
        },
        {
            "title": "Avg Rating",
            "value": round(avg_overall or 0, 2),
            "change": rating_change,
            "icon": "Star",
            "color": review_color,
        },
        {
            "title": "Occupancy Rate",
            "value": f"{round((bookings.count() / places.count()) * 100, 2)}%",
            "change": bookings.count() - bookings_before_this_month,
            "icon": "Users",
            "color": "purple",
        },
    ]

    return stats


def revenue_booking_trend(request):
    today = date.today()
    year = today.year  # or use a custom year

    # Initialize result list
    monthly_data = []

    for month in range(1, 13):
        # First and last day of the month
        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year + 1, 1, 1)
        else:
            last_day = date(year, month + 1, 1)

        # Query bookings within that month
        bookings = Booking.objects.filter(
            place__owner=request.user,
            move_in_date__gte=first_day,
            move_in_date__lt=last_day,
        )

        count = bookings.count()
        total_revenue = bookings.aggregate(total=Sum("rent_per_month"))["total"] or 0
        avg_price = bookings.aggregate(avg=Avg("rent_per_month"))["avg"] or 0

        monthly_data.append(
            {
                "month": month_name[month][:3],
                "bookings": count,
                "revenue": float(total_revenue),
                "avgPrice": round(float(avg_price), 2),
            }
        )

    return monthly_data


def occupency_rate(request):
    today = date.today()
    year = today.year  # or use a custom year

    # Initialize result list
    monthly_data = []

    for month in range(1, 13):
        # First and last day of the month
        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year + 1, 1, 1)
        else:
            last_day = date(year, month + 1, 1)

        # Query bookings within that month
        bookings = Booking.objects.filter(
            place__owner=request.user,
            move_in_date__gte=first_day,
            move_in_date__lt=last_day,
        )

        count = bookings.count()
        places_count = Place.objects.filter(owner=request.user).count()

        occupancy_rate = (count / places_count) * 100 if places_count > 0 else 0

        monthly_data.append(
            {
                "month": month_name[month][:3],
                "occupancyRate": round(float(occupancy_rate), 2),
                "bookings": count,
            }
        )

    return monthly_data


def performance_matrics(request):
    places = Place.objects.filter(owner=request.user)

    # Helper accumulators
    metrics = {
        "overall": [],
        "value_for_money": [],
        "cleanliness": [],
        "description_match": [],
        "location_convenience": [],
        "neighborhood": [],
    }

    for place in places:
        overall = place.get_average_overall()
        if overall > 0:
            metrics["overall"].append(overall)

        value_for_money = place.get_average_value_for_money_rating()
        if value_for_money > 0:
            metrics["value_for_money"].append(value_for_money)

        cleanliness = place.get_average_cleanliness_rating()
        if cleanliness > 0:
            metrics["cleanliness"].append(cleanliness)

        description_match = place.get_avarage_description_match_rating()
        if description_match > 0:
            metrics["description_match"].append(description_match)

        location_convenience = place.get_average_location_convenience_rating()
        if location_convenience > 0:
            metrics["location_convenience"].append(location_convenience)

        neighborhood = place.get_average_neighborhood_rating()
        if neighborhood > 0:
            metrics["neighborhood"].append(neighborhood)

    # Average each metric across all the user's places
    def avg(values):
        return round(sum(values) / len(values), 2) if values else 0

    res = [
        {
            "metric": "Over All",
            "value": avg(metrics["overall"]),
            # "target": 90,
            "color": "#10b981",
        },
        {
            "metric": "Value for Money",
            "value": avg(metrics["value_for_money"]),
            # "target": 4.5,
            "color": "#3b82f6",
        },
        {
            "metric": "Cleanliness",
            "value": avg(metrics["cleanliness"]),
            # "target": 4.5,
            "color": "#f59e0b",
        },
        {
            "metric": "Description Match",
            "value": avg(metrics["description_match"]),
            # "target": 4.3,
            "color": "#6366f1",
        },
        {
            "metric": "Location Convenience",
            "value": avg(metrics["location_convenience"]),
            # "target": 4.4,
            "color": "#ec4899",
        },
        {
            "metric": "Neighborhood",
            "value": avg(metrics["neighborhood"]),
            # "target": 4.3,
            "color": "#eab308",
        },
    ]

    return res


def top_listings_data(request):
    today = date.today()
    places = Place.objects.filter(owner=request.user)
    listings = []

    for place in places:
        bookings = place.bookings.filter(move_in_date__lt=today)

        total_revenue = 0
        for b in bookings:
            # Months between move_in and today
            months = (today.year - b.move_in_date.year) * 12 + (
                today.month - b.move_in_date.month
            )
            if months < 1:
                months = 1  # Ensure at least 1 month of revenue
            total_revenue += float(b.rent_per_month or 0) * months

        listings.append(
            {"name": place.title[:10] + "...", "revenue": round(total_revenue, 2)}
        )

    # Sort by revenue, descending
    top_listings = sorted(listings, key=lambda x: x["revenue"], reverse=True)[:5]

    return top_listings


def price_optimization_data(request):
    today = date.today()
    bookings = Booking.objects.filter(place__owner=request.user, move_in_date__lt=today)

    price_groups = defaultdict(float)

    for b in bookings:
        if not b.rent_per_month:
            continue

        price = float(b.rent_per_month)

        # Calculate months active
        months = (today.year - b.move_in_date.year) * 12 + (
            today.month - b.move_in_date.month
        )
        months = max(months, 1)

        revenue = price * months
        price_groups[price] += revenue

    # Convert to desired list format
    data = [
        {"price": int(price), "revenue": round(rev, 2)}
        for price, rev in price_groups.items()
    ]

    # Sort by price (ascending)
    data.sort(key=lambda x: x["price"])

    return data
