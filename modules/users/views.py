from modules.users.models import Profile
from django.views.generic import DetailView, UpdateView, CreateView, View, TemplateView

class ProfileDetailView(DetailView):
    """
    Представление для просмотра профиля
    """
    model = Profile
    context_object_name = 'profile'
    template_name = 'users/profile_detail.html'

    queryset = model.objects.all().select_related('user').prefetch_related('followers', 'followers__user', 'following', 'following__user')
    # queryset = model.objects.all().select_related('user').prefetch_related('followers', 'followers__user', 'following', 'following__user')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница пользователя: {self.object.user.username}'
        return context