from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
import random


from country_guesse import settings
from map_game.models import CountryModels


class MapGameView(TemplateView):
    template_name = 'map_game.html'
    countries = [
        "Andorra", "Armenia", "Austria", "Belgium", "Bulgaria", "Bosnia and Herzegovina",
        "Belarus", "Switzerland", "Czech Republic", "Germany", "Denmark", "Estonia",
        "Finland", "United Kingdom", "Georgia", "Greece", "Croatia", "Hungary",
        "Ireland", "Iceland", "Italy", "Liechtenstein", "Lithuania", "Luxembourg",
        "Latvia", "Moldova", "Macedonia", "Montenegro", "Norway", "Poland",
        "Portugal", "Romania", "Serbia", "Slovakia", "Slovenia", "Sweden",
        "Turkey", "Ukraine", "Kosovo", "Netherlands", "Spain", "France", "Cyprus"
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        guessed_countries = self.request.session.get('guessed_countries', [])
        target_country_index = self.request.session.get('target_country_index', 0)

        if not guessed_countries:
            random.shuffle(self.countries)

        target_country = self.countries[target_country_index]
        context['target_country'] = target_country
        return context


class HomeView(TemplateView):
    template_name = 'home.html'
    model = CountryModels

class CheckGuessView(View):
    def post(self, request):
        # Get the clicked and target countries from the POST data
        clicked_country = request.POST.get('clicked_country')
        target_country = request.POST.get('target_country')

        # Retrieve guessed countries and target country index from session
        guessed_countries = request.session.get('guessed_countries', [])
        target_country_index = request.session.get('target_country_index', 0)

        # Compare the clicked and target countries (case-insensitive)
        if clicked_country.lower() == target_country.lower():
            # Append guessed country to the list and increment target country index
            guessed_countries.append(target_country)
            target_country_index += 1

            # Update session variables
            request.session['guessed_countries'] = guessed_countries
            request.session['target_country_index'] = target_country_index

            # Check if all countries have been guessed
            if target_country_index >= len(MapGameView.countries):
                # Game completed, send JSON response indicating completion
                return JsonResponse({'completed': True})
            else:
                # Game not completed, send JSON response indicating correct guess
                return JsonResponse({'correct_guess': True})
        else:
            # Send JSON response indicating incorrect guess
            return JsonResponse({'correct_guess': False})





def signup(request):
    if request.method == 'POST':
        # Process form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')


        if User.objects.filter(username=username).exists():
            messages.error(request, 'Your username already exists')  # Use messages.error here
            return render(request, 'authentication/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Your email already exists')  # Use messages.error here
            return render(request, 'authentication/signup.html')


        if pass1 != pass2:
            messages.error(request, 'Your password does not match')  # Use messages.error here
            return render(request, 'authentication/signup.html')

        # Create user
        myuser = User.objects.create_user(username=username, email=email, password=pass1)
        myuser.is_active = False
        myuser.save()
        messages.success(request, 'An email has been sent to activate your account')

        # Welcome Email

        subject = 'Welcome to Country Guesser'
        message = "Hello" + myuser.username + "!! \n" + "Welcome to Country Guesser!! \n Thank you for visiting our website \n We have also sent you a confirmation email, please confirm your email address in order to activate your account. \n \n Thanking You \n Marmaliuc Brian"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email

        current_site = get_current_site(request)
        email_subject = 'Confirm your email @ Country Guesser '
        message2 = render_to_string('authentication/email_confirmation.html', {
            'user': myuser.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email]
        )
        email.fail_silently = True
        email.send()
        return redirect('signin')  # Redirect to signin page

    return render(request, 'authentication/signup.html')
def signin(request):

    if request.method == 'POST':

        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return render(request, 'home.html')

        else:
            messages.success(request, 'Credentials do not match')
            return redirect('home-page')

    return render(request,'authentication/signin.html')

def signout(request):
    logout(request)

    return redirect('home-page')




def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activated')
        return redirect('home-page')
    else:
        return render(request, "authentication/activation_failed.html")