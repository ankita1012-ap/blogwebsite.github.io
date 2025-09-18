from django.core.mail import send_mail
from django.conf import settings

def send_test_email(email):
    subject = "Welcome to EduGlobe – Your Gateway to Knowledge!"
    message = """
    Hi there!

Welcome to EduGlobe! We’re thrilled you’ve joined our community of curious minds and lifelong learners.

Get ready to explore a wide range of blogs covering exciting topics, helpful tips, and insightful ideas—all crafted to help you learn, grow, and think smarter every day.

Stay tuned for the latest articles, recommendations, and much more that will fuel your passion for knowledge.

If you have any questions or suggestions, feel free to reach out—we’d love to hear from you!

Happy reading!

Warm wishes,
The EduGlobe Team
    """
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]  # Change to your test email

    try:
        send_mail(subject, message, from_email, recipient_list)
        print("Email sent successfully!")
    except Exception as e:
        print(e)

