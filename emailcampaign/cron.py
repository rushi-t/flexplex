import socket

from django.core.mail import EmailMessage

import emailcampaign
from emailcampaign import models
from emailcampaign.models import User, Campaign, CampaignUser
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.models import Site
from flexplex import settings

def email_scheduled_job():
    campaign = Campaign()
    campaign.save()
    users = User.objects.all()
    for user in users:
        campaign_user = CampaignUser(user=user, campaign=campaign)
        campaign_user.save()

        subject, from_email, to = 'Flexplex: Digital OOH Network', 'admin@flexplex.in ', 'rushikesh.talokar@gmail.com'
        html_content = render_to_string('email/cerberus-responsive.html',
                                        {'host': settings.HOST_NAME,
                                         'campaign_user': campaign_user}
                                        )  # ...
        text_content = strip_tags(html_content)  # this strips the html, so people will have the text as well.


        # create the email, and attach the HTML version as well.
        msg = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email,
                                     to=[campaign_user.user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # email = EmailMessage('Subject', 'Body', to=[user.email])
        # email.send()

    pass