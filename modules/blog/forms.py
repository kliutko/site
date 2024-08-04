from django import forms

from modules.blog.models import Article


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

