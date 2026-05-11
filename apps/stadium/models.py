from django.db import models
from django.conf import settings

# Create your models here.


class Match(models.Model):
    SPORT_CHOICES = [
        ('Tennis', 'Tennis'),
        ('Football', 'Football'),
    ]

    title = models.CharField(max_length=200) 
    sport = models.CharField(max_length=20, choices=SPORT_CHOICES)
    description = models.TextField(help_text="Why is this match a must-watch?")
    date = models.DateTimeField()
    location = models.CharField(max_length=100, default="London, UK")
    image_url = models.URLField(blank=True, help_text="Paste an elegant stadium image URL")
    
    capacity = models.PositiveIntegerField(default=50) # سعة الملعب
    
    @property
    def remaining_seats(self):
        # عملية حسابية في الباك آند تحسب المقاعد المتبقية
        total_booked = sum(b.ticket_count for b in self.bookings.all())
        return self.capacity - total_booked
    
    def __str__(self):
        return self.title
    


class Booking(models.Model):
   
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='bookings')
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    ticket_count = models.PositiveIntegerField(default=1)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.match.title}"