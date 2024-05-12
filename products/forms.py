from django import forms
from products.models import Comment, Zayavka


class ProductCommentForm(forms.ModelForm):

    text = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'rows': 4,
            'label': 'Напишите комментраий',
            'placeholder': 'Текст отзыва'
            }
        )
    )

    class Meta:
        model = Comment
        fields = ['text', 'user', 'zayavka']