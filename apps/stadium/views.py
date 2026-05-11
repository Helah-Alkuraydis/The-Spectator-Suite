from django.shortcuts import render , redirect
from .models import Booking, Match
from .forms import VIPRegistrationForm
from django.contrib import messages
from django.db.models import Sum, Count , Avg
from django.contrib.auth.decorators import login_required

# Create your views here.

def join_vip(request):
    submitted = False
    if request.method == 'POST':
        form = VIPRegistrationForm(request.POST)
        if form.is_valid():
            submitted = True
    else:
        form = VIPRegistrationForm()
        
    return render(request, 'stadium/join_vip.html', {'form': form, 'submitted': submitted})


def event_list(request):
    query = request.GET.get('q') 
    sport_filter = request.GET.get('sport') 
    
    matches = Match.objects.all()

    if query:
        matches = matches.filter(title__icontains=query) 
    
    if sport_filter:
        matches = matches.filter(sport=sport_filter)

    return render(request, 'stadium/event_list.html', {'matches': matches})

@login_required(login_url='/users/login/')
def book_ticket(request, match_id):
    match = Match.objects.get(id=match_id)
    if request.method == 'POST':
        tickets_requested = int(request.POST.get('tickets'))
       

        if tickets_requested > match.remaining_seats:
            # هنا الـ Wow Factor: منع الحجز برمجياً
            messages.error(request, f"Luxury involves exclusivity, but we are out of seats! Only {match.remaining_seats} left.")    
            
        else :
            Booking.objects.create(
                user=request.user,
                match=match,
                user_name=request.user.get_full_name(),
                user_email=request.POST.get('email'),
                ticket_count=int(request.POST.get('tickets'))
            )
            messages.success(request, "Ticket booked successfully!")
            return redirect('my_bookings')
    context = {
        'match': match,
        'initial_name': request.user.get_full_name(), # أو request.user.get_full_name() إذا كنتِ تستخدمينه
        'initial_email': request.user.email,
    } 
    return render(request, 'stadium/book_ticket.html', context)


@login_required(login_url='/users/login/')
def my_bookings(request):
    user_bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    
    return render(request, 'stadium/my_bookings.html', {
        'bookings': user_bookings
    })

def admin_dashboard(request):
    # 1. إحصائيات عامة (البطاقات العلوية)
    total_bookings = Booking.objects.count()
    total_tickets = Booking.objects.aggregate(Sum('ticket_count'))['ticket_count__sum'] or 0
    
    # 2. تحليل سعة كل مباراة (القديم اللي طلبته)
    matches = Match.objects.annotate(total_booked=Sum('bookings__ticket_count'))
    match_analytics = []
    for m in matches:
        booked = m.total_booked or 0
        rate = (booked / m.capacity) * 100 if m.capacity > 0 else 0
        
        if rate >= 90: status, color = "Limited", "#8B0000"
        elif rate >= 50: status, color = "High Demand", "#B8860B"
        else: status, color = "Open", "#2D5A27"
            
        match_analytics.append({
            'title': m.title, 'rate': round(rate, 1), 'status': status,
            'color': color, 'booked': booked, 'capacity': m.capacity
        })

    # 3. تحليل المواقع والأفرج (الجديد)
    location_stats = Match.objects.values('location').annotate(
        seats_sold=Sum('bookings__ticket_count')
    ).order_by('-seats_sold')
    
    avg_tickets = Booking.objects.aggregate(Avg('ticket_count'))['ticket_count__avg'] or 0

    return render(request, 'stadium/dashboard.html', {
        'total_bookings': total_bookings,
        'total_tickets': total_tickets,
        'match_analytics': match_analytics,
        'location_stats': location_stats,
        'avg_tickets': round(avg_tickets, 1),
    })