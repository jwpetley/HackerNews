from django import forms
from django.forms import ModelForm

from .models import Comment


class SetUpvotedForm(forms.Form):
    upvoted = forms.BooleanField()


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
