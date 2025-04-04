#from django.conf import settings
from ms_active_directory import ADDomain, ADUser, ADGroup
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
import datetime

from core.settings import ENV
#from .models import ADUser, ADGroup, AuditLog
from .forms import UserCreationForm, UserModificationForm

from directory.simple_ad import ConnectActiveDirectory, print_object, userAccountControl_is_enabled, extract_ou

env_context = {
    'ad_domain' : ENV['AD_DOMAIN'],
    'ad_server' : ENV['AD_SERVER'],
    'ad_admin_user' : ENV['AD_ADMIN_USER'],
    'ad_user_attrs' : ENV['AD_USER_ATTRS'],
    'ad_group_attrs' : ENV['AD_GROUP_ATTRS'],
    'ad_base' : ENV['AD_BASE'],
    'ad_base_user' : ENV['AD_BASE_USER'],
    'ad_base_group' : ENV['AD_BASE_GROUP'],
    'ad_group_required' : ENV['AD_GROUP_REQUIRED'],
    'ad_group_denied' : ENV['AD_GROUP_DENIED'],
    'now' : timezone.now(),
}

## Template Views
#################

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'about.html'
    extra_context = env_context
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["now"] = timezone.now()
    #     return context

class HelpPageView(TemplateView):
    template_name = 'help.html'

# class LoginView(TemplateView):
#     template_name = 'login.html'
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     return context

class LogoffView(TemplateView):
    template_name = 'logoff.html'


## List Views
##############

# User Management Views
class UserListView(ListView):
    template_name = 'users/list.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["start_date"] = timezone.now()
    #     return context

    def dispatch(self, request, *args, **kwargs):
        start_time = datetime.datetime.now()  # Begin time

        response = super().dispatch(request, *args, **kwargs)

        end_time = datetime.datetime.now()  # End time

        render_time = (end_time - start_time).total_seconds()  # Time difference

        # Add the render time to the context
        if hasattr(response, 'context_data'):
            response.context_data['render_time'] = render_time
            response.context_data['start_date'] = start_time
            response.context_data['end_date'] = end_time

        return response

    def get_queryset(self):
        
        filter = self.request.GET.get('filter')
        if not filter or '*' in filter:
            return None

        con = ConnectActiveDirectory()
        users = con.get_users(filter=filter, attrs=['sAMAccountName','givenName','sn','mail','userAccountControl',
                                                    'lastLogonTimestamp','pwdLastSet','whenCreated','whenChanged',
                                                    'company', 'department', 'l', 'st', 'o'])

        # Create list with some attributes
        user_list = [
            {
                'username':              user.get('sAMAccountName'),
                'givenName':             user.get('givenName') if user.get('givenName') else '-',
                'sn':                    user.get('sn') if user.get('sn') else '',
                'email':                 user.get('mail') if user.get('mail') else '-',
                'userAccountControl':    user.get('userAccountControl'),
                'status':                userAccountControl_is_enabled(user.get('userAccountControl')),
                'lastLogonTimestamp':    user.get('lastLogonTimestamp'),
                'pwdLastSet':            user.get('pwdLastSet'),
                'whenCreated':           user.get('whenCreated'),
                'whenChanged':           user.get('whenChanged'),
                'distinguishedName':     user.distinguished_name,
                'lastOU':                extract_ou(user.distinguished_name),
                'company':               user.get('company'),
                'department':            user.get('department'),
                'l':                     user.get('l'),
                'st':                    user.get('st'),
                'o':                     user.get('o'),
            }
            for user in users
        ]
        
        return user_list


class GroupListView(ListView):
    template_name = 'groups/list.html'
    #model = ADGroup
    # object_list -> ADGroup.objects.all()
    def get_queryset(self):
        pass

class ComputerListView(ListView):
    template_name = 'computers/list.html'
    #model = ADGroup
    # object_list -> ADGroup.objects.all()
    def get_queryset(self):
        pass

class OrganizationListView(ListView):
    template_name = 'organizations/list.html'
    #model = ADGroup
    # object_list -> ADGroup.objects.all()
    def get_queryset(self):
        pass

## Details Views
################

class UserDetailView(DetailView):
    template_name = 'users/detail.html'
    #model = ADUser
    # object -> ADUser.objects.get(pk=id)

    # def get_queryset(self):
    #     pass

    def get_object(self, queryset=None):
        filter = self.kwargs.get('username')

        con = ConnectActiveDirectory()
        users = con.get_user(filter=filter, attrs=['*'])
        #print_object(users)

        if not users: return None

        return users.all_attributes
