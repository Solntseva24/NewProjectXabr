from django import forms
from django.forms import Textarea
from mainapp.models import Comments


class CommentForm(forms.ModelForm):
    """форма комментариев к статьям"""

    class Meta:
        model = Comments
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget = Textarea(attrs={'rows': 2})
