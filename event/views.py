from datetime import datetime

from django.http import HttpResponseRedirect
from notifications.signals import notify

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic.edit import CreateView,FormView, View
from django.views.generic import UpdateView, ListView, DetailView
from django.utils import timezone

from accounts.models import Account
from forum.models import Group
from forum.views import GroupMixin

from .calendar_api import sync_event
from .form import EventCreation
from .models import Event


class CreateEventView(GroupMixin, LoginRequiredMixin, FormView):
    model = Event
    template_name = 'event/event_create_form.html'
    form_class = EventCreation

    def form_valid(self, form):
        group = Group.objects.filter(slug=self.kwargs['slug']).first()
        form.instance.host = self.request.user
        form.instance.group = group
        form.instance.slug = form.instance.name
        form.save()

        content = f"You are invited to join {form.instance.name}"
        group_members = group.member.filter(is_suspended=False).exclude(
            user_id=self.request.user.id
        )
        members = Account.objects.filter(
            group_membership__in=group_members
        )
        sender = self.request.user

        notify.send(sender=sender,
                    recipient=members,
                    verb=content,
                    action_object=form.instance,
                    description='event invite',

                    )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('forum:event:event-list', args=[self.kwargs['slug']])


class UpcomingExpiredEventView(LoginRequiredMixin, GroupMixin,View):
    def get(self, request, *args, **kwargs):
        pass


class EditEventView(GroupMixin, LoginRequiredMixin, UpdateView):
    raise_exception = False
    permission_required = 'event.change_event'
    login_url = '/'
    redirect_field_name = 'event-detail'

    model = Event
    fields = ('Cover_image', 'name', 'location', 'start_date_time', 'end_date_time')
    template_name = 'event/event_edit.html'
    success_url = '/'


class EventListView(GroupMixin, LoginRequiredMixin, ListView):
    model = Event
    template_name = 'event/event_list.html'
    paginate_by = 5
    records = {}

    def get(self, request, **kwargs):
        group = Group.objects.filter(slug=self.kwargs['slug']).first()
        if request.user not in group.admin.all():
            # event = group.event_set.all()
            # context = super(EventListView, self).get()
            # context['event'] = event
            self.template_name = 'calendar/calendar.html'
            self.context_object_name = 'events'
            return super(EventListView, self).get(request, **kwargs)

        return super().get(request, **kwargs)

    def get_queryset(self):
        group = Group.objects.filter(slug=self.kwargs['slug']).first()
        self.records['group'] = group
        if self.request.user not in group.admin.all():
            return Event.objects.filter(
                confirmed_invitees=self.request.user
            )
        return Event.objects.filter(
            group=group
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # group = Group.objects.filter(slug=self.kwargs['slug']).first()
        context['upcoming_events'] = Event.objects.filter(
            group=self.records['group'],
            start_date_time__gt=datetime.now()
        )
        context['past_events'] = Event.objects.filter(
            group=self.records['group'],
            end_date_time__lt=datetime.now()
        )
        context['ongoing_events'] = Event.objects.filter(
            group=self.records['group'],
            start_date_time=timezone.now()
        )
        return context


class EventDetailView(GroupMixin, LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'event/event_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(EventDetailView, self).get_context_data()
        context['confirmed_invitees']=self.get_object().confirmed_invitees
        context['unconfirmed_invitees'] = self.get_object().unconfirmed_invitees
        context['invitees'] = self.get_object().group.member.all()
        return context


class EventOnCalendar(View):

    def get(self, request, *args, **kwargs):
        group = Group.objects.filter(slug=self.kwargs['slug']).first()
        events = group.event_set.all()
        context = {
            'events': events
        }
        return render(request, 'calendar/calendar.html', context)


class AcceptInviteView(GroupMixin, LoginRequiredMixin, View):

    def post(self, request, event_id, **kwargs):
        event = Event.objects.filter(
            id=event_id
        ).first()
        if 'accept' in request.get_full_path():
            event.confirmed_invitees.add(request.user)
            sync_event(event)
        elif 'reject' in request.get_full_path():
            event.rejected_invitees.add(request.user)
            event.save()
        elif 'tentative' in request.get_full_path():
            event.unconfirmed_invitees.add(request.user)
        event.save()

        next_url = request.POST.get('next_url', '')
        return HttpResponseRedirect(
            next_url
        )





