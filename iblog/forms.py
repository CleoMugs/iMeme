from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name', 'email', 'body')

'''
class CommentForm(forms.Form):
	name, email, body = forms.CharField(widget=SummernoteWidget())
'''