from django import forms

from modules.blog.models import Article
from .models import Comment

class ArticleCreateForm(forms.ModelForm):
    """
    Форма добавления статей на сайте
    """
    class Meta:
        model = Article
        fields = ('title', 'slug', 'category', 'description', 'thumbnail', 'status')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
        self.fields['description'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['description'].required = False




class ArticleUpdateForm(ArticleCreateForm):
    """
    Форма обновления статьи на сайте
    """
    class Meta:
        model = Article
        fields = ArticleCreateForm.Meta.fields + ('updater', 'fixed')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)

        self.fields['fixed'].widget.attrs.update({
                'class': 'form-check-input'
        })
        self.fields['fixed'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['description'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
        self.fields['description'].required = False




class CommentCreateForm(forms.ModelForm):
    """
    Форма добавления комментариев к статьям
    """
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'cols': 30, 'rows': 5, 'placeholder': 'Комментарий', 'class': 'form-control'}))
    name = forms.CharField(label='Имя', max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Введите ваше имя', 'class': 'form-control'}), required=False)
    email = forms.EmailField(label='Email', max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Введите ваш email', 'class': 'form-control'}), required=False)

    class Meta:
        model = Comment
        fields = ('content', 'name', 'email')