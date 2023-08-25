from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import UserProfile, DateInfo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserProfileCreationForm, UserProfileUpdateForm
from django.utils.http import url_has_allowed_host_and_scheme

class UserProfileLogoutView(LogoutView):
    next_page = 'userprofile_login'

class UserProfileCreateView(CreateView):
    model = UserProfile
    form_class = UserProfileCreationForm
    template_name = 'userprofile_form.html'
    success_url = reverse_lazy('userprofile_list')

class UserProfileLoginView(LoginView):
    template_name = 'userprofile_login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        response = super().form_valid(form)
        # Add any custom logic or prints here
        return response

    def get_success_url(self):
        # Try to get the next parameter from the request
        next_url = self.request.GET.get('next')

        # If the next parameter exists and is safe, return it
        if next_url and url_has_allowed_host_and_scheme(next_url, self.request.get_host()):
            return next_url

        # If not, or if there's no next parameter, redirect to the user's profile detail page
        try:
            user_profile = UserProfile.objects.get(username=self.request.user.username)
            return reverse('userprofile_detail', kwargs={'pk': user_profile.pk})
        except UserProfile.DoesNotExist:
            # Handle the scenario where the UserProfile doesn't exist.
            # Here, I'm just redirecting to home, but you can decide on what's suitable.
            return reverse('home')

class HomePageView(TemplateView):
    template_name = 'home.html'

# UserProfile views
class UserProfileListView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'userprofile_list.html'
    context_object_name = 'userprofiles'
    
class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'userprofile_detail.html'
    context_object_name = 'userprofile'

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileUpdateForm
    template_name = 'userprofile_form.html'

class UserProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = UserProfile
    template_name = 'userprofile_confirm_delete.html'
    success_url = reverse_lazy('userprofile_list')

# DateInfo views
class DateInfoListView(LoginRequiredMixin, ListView):
    model = DateInfo
    template_name = 'dateinfo_list.html'
    context_object_name = 'dateinfos'

class DateInfoDetailView(LoginRequiredMixin, DetailView):
    model = DateInfo
    template_name = 'dateinfo_detail.html'
    context_object_name = 'dateinfo'

class DateInfoCreateView(LoginRequiredMixin, CreateView):
    model = DateInfo
    template_name = 'dateinfo_form.html'
    fields = ['user', 'sleep', 'calories', 'stress', 'steps', 'weight', 'wellness_score', 'date']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DateInfoUpdateView(LoginRequiredMixin, UpdateView):
    model = DateInfo
    template_name = 'dateinfo_form.html'
    fields = ['user', 'sleep', 'calories', 'stress', 'steps', 'weight', 'wellness_score', 'date']

class DateInfoDeleteView(LoginRequiredMixin, DeleteView):
    model = DateInfo
    template_name = 'dateinfo_confirm_delete.html'
    success_url = reverse_lazy('dateinfo_list')
