from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')


def vibe_check(request):
    recommendation = None
    if request.method == 'POST':
        sport = request.POST.get('sport')
        mood = request.POST.get('mood')
        
        if sport == 'Tennis' and mood == 'Relaxed':
            recommendation = "White Linen outfit, an Iced Latte, and a quiet garden setting."
        elif sport == 'Football' and mood == 'Energetic':
            recommendation = "Your favorite jersey, chilled sparkling water, and a surround sound system."
        else:
            recommendation = "A cozy sofa, dim lights, and total focus on the game."
            
    return render(request, 'core/vibe_check.html', {'recommendation': recommendation})