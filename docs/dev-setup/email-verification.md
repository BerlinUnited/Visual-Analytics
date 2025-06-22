## Setup
- Connect your domain with your mailgun account and install the required dns records.
- Create a sending key and store it in the MAILGUN_API_KEY enviroment variable.
- Set the MAILGUN_FROM_EMAIL enviroment variable to the email adress you want to send the verification emails from.
- change SITE_URL and SITE_NAME in settings.py to your actual URL and NAME
- add all email domains you want to allow to Allowed Email Domains in the django admin panel

