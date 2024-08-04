from django.views.generic import DetailView, UpdateView, CreateView, View, TemplateView
from django.db import transaction
from django.urls import reverse_lazy
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm
# from .forms import UserUpdateForm, ProfileUpdateForm, UserPasswordChangeForm
# from django.contrib.messages.views import SuccessMessageMixin
# from .forms import UserRegisterForm, UserLoginForm, UserForgotPasswordForm, UserSetNewPasswordForm
# from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
# from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_decode
# from django.shortcuts import redirect
# from ..services.mixins import UserIsNotAuthenticated
# from django.contrib.auth import login
from django.contrib.auth import get_user_model
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.http import JsonResponse
# from django.views.generic import ListView
# from django.contrib.auth.mixins import LoginRequiredMixin
# from modules.blog.models import Article
# from modules.services.tasks import send_activate_email_message_task

User = get_user_model()


class ProfileDetailView(DetailView):
    """
    Представление для просмотра профиля
    """
    model = Profile
    context_object_name = 'profile'
    template_name = 'users/profile_detail.html'

    queryset = model.objects.all().select_related('user').prefetch_related('followers', 'followers__user', 'following', 'following__user')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница пользователя: {self.object.user.username}'
        return context

class ProfileUpdateView(UpdateView):
    """
    Представление для редактирования профиля
    """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'users/profile_edit.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:profile_detail', kwargs={'slug': self.object.slug})
