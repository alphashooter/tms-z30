from django.forms import *
from shop.models import FeedbackModel


class FeedbackForm(ModelForm):
    class Meta:
        model = FeedbackModel
        fields = '__all__'
