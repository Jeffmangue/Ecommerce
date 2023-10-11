from django.http import JsonResponse
import json
from django.shortcuts import render
from django.contrib.auth.models import User,Group
from .models import NotificationsModel
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def notifications(request):
    name = "Notifications"
    a = User.objects.get(username=request.user.username)
    notifs = NotificationsModel.objects.filter(receiver=a).exclude(admin_feedback__isnull=False).all()
    context = {
        'name': name,
        'notifs':notifs,
    }
    return render(request, 'notifications/notifications.html', context)


def add_user_to_the_group(request):
    group_name = "lbbc-cainta"
    id = request.POST['id']
    ids = id.split('-')
    username = ids[0]
    id_ = ids[1]
    user = User.objects.filter(username=username).count()
    if user == 0:
        pass
    elif user == 1:
        user = User.objects.get(username=username)
        group = Group.objects.get(name=group_name)
        group.user_set.add(user)
        NotificationsModel.objects.filter(id=id_).update(admin_feedback='added_to_the_group')
        user = 'success'
    else:
        pass
    classes = user
    response = {
        'classes':classes,
        'id':id,
    }
    return JsonResponse(response)
