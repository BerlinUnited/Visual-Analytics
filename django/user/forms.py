from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import AllowedEmailDomains,EmailVerificationToken
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()  #### I included this,VERY IMPORTANT
        fields = ("username", "email","password1", "password2")


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()
            
            domain = email.split('@')[1]
            if not AllowedEmailDomains.objects.get(domain=domain):
                raise ValidationError(
                    f"Your E-Mail adress is not allowed"
                )
            
            User = get_user_model()
            if User.objects.filter(email=email).exists():
                raise ValidationError("A user with this email already exists.")
        
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['email'].lower()
        
        # Auto-assign organization
        domain = email.split('@')[1]
        qs = AllowedEmailDomains.objects.get(domain=domain)
        if qs.default_organization:
            user.organization = qs.default_organization
            
        
        # Set user as inactive until email is verified
        user.is_active = False
        
        if commit:
            user.save()
            # Create verification token and send email
            self.send_verification_email(user)
        
        return user
    
    def send_verification_email(self, user):
        # Create or get verification token
        token, created = EmailVerificationToken.objects.get_or_create(user=user)
        
        # Build verification URL
        verification_url = f"{settings.SITE_URL}{reverse('verify_email', args=[token.token])}"
        
        # Email context
        context = {
            'user': user,
            'verification_url': verification_url,
            'site_name': getattr(settings, 'SITE_NAME', 'Our Site'),
        }
        
        # Render email templates
        html_message = render_to_string('emails/verification_email.html', context)
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject='Verify your email address',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )