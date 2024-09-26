from django.forms import ModelForm, CharField, TextInput
from .models import Tag, Author, Quote


class TagForm(ModelForm):

    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())
    
    class Meta:
        model = Tag
        fields = ['name']


class AuthorForm(ModelForm):

    fullname = CharField(min_length=3, max_length=255, required=True, widget=TextInput())
    born_date = CharField(min_length=7, max_length=255, required=True, widget=TextInput())
    born_location = CharField(min_length=3, max_length=50, required=True, widget=TextInput())
    description = CharField(min_length=1, max_length=2500, required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(ModelForm):

    text = CharField(min_length=1, max_length=2500, required=True, widget=TextInput())

    class Meta:
        model = Quote
        fields = ['text']
        exclude = ['author', 'tags']
