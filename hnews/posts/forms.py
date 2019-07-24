from django import forms

class SetUpvotedForm(forms.Form):
    upvoted = forms.BooleanField()
