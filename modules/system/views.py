from django.shortcuts import render
from django.views.generic import ListView, DeleteView, DetailView
from modules.blog.models import Article, Category
from django.db import models

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import FeedbackCreateForm
from .models import Feedback, About, Faq, Conf, Rules, ReklamaInfo

from ..services.utils import get_client_ip
from django.shortcuts import render
from modules.services.tasks import send_contact_email_message_task
# Create your views here.





class IndexListView(ListView):
    model = Article
    # template_name = 'blog/1articles_list.html'
    template_name = 'index.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

class FaqListView(ListView):
    model = Faq
    template_name = 'system/faq_demo.html'
    context_object_name = 'faq'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Часто задаваемые вопросы'
        return context

class RulesListView(ListView):
    model = Rules
    template_name = 'system/rules.html'
    context_object_name = 'rules'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Правила'
        return context

class ReklamaInfoListView(ListView):
    model = ReklamaInfo
    template_name = 'system/reklamainfo.html'
    context_object_name = 'reklamainfo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Реклама'
        return context


class AboutListView(DetailView):
    model = About
    template_name = 'system/about.html'
    context_object_name = 'about'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        # context['form'] = CommentCreateForm
        # context['similar_articles'] = self.get_similar_articles(self.object)
        # context['banner_header'] = Reklama.objects.all().filter(placement='header_banners_blog', status='inwork', start_time__lte=now, stop_time__gte=now)
        # context['banner_footer'] = Reklama.objects.all().filter(placement='footer_banners_blog', status='inwork', start_time__lte=now, stop_time__gte=now)
        # context['left_blog'] = Reklama.objects.all().filter(placement='left_blog', status='inwork', start_time__lte=now, stop_time__gte=now)
        # context['left_down_blog'] = Reklama.objects.all().filter(placement='left_down_blog', status='inwork', start_time__lte=now, stop_time__gte=now)

        return context



class FeedbackCreateView(SuccessMessageMixin, CreateView):
    model = Feedback
    form_class = FeedbackCreateForm
    success_message = 'Ваше письмо успешно отправлено администрации сайта'
    template_name = 'system/feedback.html'
    extra_context = {'title': 'Контактная форма'}
    success_url = reverse_lazy('system:home')

    def form_valid(self, form):
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.ip_address = get_client_ip(self.request)
            if self.request.user.is_authenticated:
                feedback.user = self.request.user
            send_contact_email_message_task.delay(feedback.subject, feedback.email, feedback.content, feedback.ip_address, feedback.user_id)
        return super().form_valid(form)


class ConfListView(ListView):
    model = Conf
    template_name = 'system/conf.html'
    context_object_name = 'conf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Политика конфедициальности'
        return context


def tr_handler404(request, exception):
    """
    Обработка ошибки 404
    """
    return render(request=request, template_name='system/errors/error_page.html', status=404, context={
        'title': 'Страница не найдена: 404',
        'error_message': 'К сожалению такая страница была не найдена, или перемещена',
    })


def tr_handler500(request):
    """
    Обработка ошибки 500
    """
    return render(request=request, template_name='system/errors/error_page.html', status=500, context={
        'title': 'Ошибка сервера: 500',
        'error_message': 'Внутренняя ошибка сайта, вернитесь на главную страницу, отчет об ошибке мы направим администрации сайта',
    })


def tr_handler403(request, exception):
    """
    Обработка ошибки 403
    """
    return render(request=request, template_name='system/errors/error_page.html', status=403, context={
        'title': 'Ошибка доступа: 403',
        'error_message': 'Доступ к этой странице ограничен',
    })