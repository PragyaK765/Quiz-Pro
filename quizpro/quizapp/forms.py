from django import forms
from .models import Answer

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(QuizForm, self).__init__(*args, **kwargs)
        
        for question in questions:
            choices = [(answer.id, answer.text) for answer in question.answers.all()]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=choices, widget=forms.RadioSelect, required=True, label=question.text
            )