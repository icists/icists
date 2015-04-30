from django.db import models

# Create your models here.

class Application(models.Model):
    EARLY = 'E'
    REGULAR = 'R'
    LATE = 'L'
    APPLICATION_CATEGORY = (
        (EARLY, 'Early'),
        (REGULAR, 'Regular'),
        (LATE, 'Late'),
    )
    ACCEPTED = 'A'
    DISMISSED = 'D'
    PENDING = 'P'
    SCREENING_RESULT = (
        (ACCEPTED, 'Accepted'),
        (DISMISSED, 'Dismissed'),
        (PENDING, 'Pending'),
    )

    submit_status = models.BooleanField(default=False)
    application_category = models.CharField(max_length=1,
                                            choices=APPLICATION_CATEGORY, default=REGULAR)
    screening_result = models.CharField(max_length=1,
                                        choices=SCREENING_RESULT, default=PENDING)
    results_embargo = models.BooleanField(default=True)
    project_topic = models.CharField(max_length=45)
    essay_topic = models.TextField(max_length=200)
    essay = models.TextField()
    visa_support_letter_required = models.BooleanField(default=False)
    financial_aid_apply = models.BooleanField(default=False)


class Participant(models.Model):
    NOT_PAID = 'N'
    PAID = 'P'
    LESS_PAID = 'L'
    OVER_PAID = 'O'
    PAYMENT_STATUS = (
        (NOT_PAID, 'Not Paid'),
        (PAID, 'Paid'),
        (LESS_PAID, 'Less Paid'),
        (OVER_PAID, 'Over Paid'),
    )

    accommodation = models.ForeignKey('Accommodation', related_name="participant")
    application = models.OneToOneField('Application', related_name="participant")
    discount = models.ForeignKey('Discount', related_name="participant")

    project_team_no = models.PositiveSmallIntegerField()
    payment_status = models.CharField(max_length=1,
                                      choices=PAYMENT_STATUS, default=NOT_PAID)
    required_payment = models.IntegerField()
    breakfast_option = models.BooleanField(default=False)
    dietary_option = models.CharField(max_length=45) # Vegetarian, Halal, Others (Optional text input)
    pretour = models.BooleanField(default=False)
    posttour = models.BooleanField(default=False)


class Accommodation(models.Model):
    hotel_name = models.CharField(max_length=45)
    hotel_room = models.CharField(max_length=45)
    accommodation_payment = models.IntegerField()
    gender = models.CharField(max_length=45)
    availability = models.IntegerField()

    
class Discount(models.Model):
    discount_code = models.CharField(max_length=10, primary_key=True)
    discount_value = models.IntegerField()
    disocunt_percent = models.FloatField()

