from django import forms
from django.core.exceptions import ValidationError
from taggit.forms import TagField

from .models import Comment, CommentUser, PornoStar


class SharePornoStarForm(forms.Form):
    name = forms.CharField(
        max_length=64, widget=forms.TextInput(attrs={"placeholder": "Name"})
    )
    email_to = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "Email to"})
    )
    content = forms.CharField(widget=forms.Textarea)


class CommentUserForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Name"})
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Email"})
    )

    class Meta:
        model = CommentUser
        fields = ('name', 'email')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


def clean_tags(*args):
    args = args[0].split(',')
    if len(args) > 5:
        raise ValidationError(
            message='Tags amount must be more than 5',
            code='invalid',
        )


class PornoStarAdminForm(forms.ModelForm):
    tags = TagField(validators=[clean_tags])

    class Meta:
        model = PornoStar
        fields = '__all__'
