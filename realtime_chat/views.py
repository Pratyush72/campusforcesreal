from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from accounts.models import CustomUser
from .models import Message
import json
from django.views.decorators.csrf import csrf_exempt

@login_required
def chat_list(request):
    query = request.GET.get('q', '')
    users = []

    if query:
        users = list(CustomUser.objects.filter(username__icontains=query).exclude(id=request.user.id))

    # Users with whom current user has messages
    sent_ids = Message.objects.filter(sender=request.user).values_list('receiver_id', flat=True).distinct()
    recv_ids = Message.objects.filter(receiver=request.user).values_list('sender_id', flat=True).distinct()
    chat_user_ids = set(list(sent_ids) + list(recv_ids))

    users += list(CustomUser.objects.filter(id__in=chat_user_ids).exclude(id=request.user.id))

    # Remove duplicates
    users = list({u.id: u for u in users}.values())

    # Add unread count
    for u in users:
        u.unread_count = Message.objects.filter(sender=u, receiver=request.user, is_read=False).count()

    return render(request, 'realtime_chat/chat_list.html', {'users': users, 'query': query})

@login_required
def get_messages(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    # Mark as read
    messages.filter(receiver=request.user, is_read=False).update(is_read=True)

    messages_data = [{
        'id': m.id,
        'sender_id': m.sender.id,
        'body': m.content,
        'timestamp': m.timestamp.isoformat(),
        'is_read': m.is_read
    } for m in messages]

    return JsonResponse({'messages': messages_data, 'current_user_id': request.user.id})

@login_required
@csrf_exempt
def send_message(request, user_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        receiver = get_object_or_404(CustomUser, id=user_id)
        message = Message.objects.create(sender=request.user, receiver=receiver, content=data['message'])
        return JsonResponse({
            'id': message.id,
            'body': message.content,
            'sender_id': message.sender.id,
            'receiver_id': message.receiver.id,
            'timestamp': message.timestamp.isoformat(),
            'is_read': message.is_read
        })

@login_required
@csrf_exempt
def mark_seen(request, user_id):
    if request.method == "POST":
        messages = Message.objects.filter(sender_id=user_id, receiver=request.user, is_read=False)
        messages.update(is_read=True)
        return JsonResponse({"status": "success", "updated": messages.count()})
    return JsonResponse({"status": "failed"}, status=400)

# Typing indicator
@login_required
@csrf_exempt
def typing_status(request, user_id):
    if request.method == "POST":
        data = json.loads(request.body)
        # store typing status for receiver
        request.session[f'typing_{request.user.id}'] = data.get('typing', False)
        return JsonResponse({'status':'ok'})

@login_required
def get_typing_status(request, user_id):
    typing = request.session.get(f'typing_{user_id}', False)
    return JsonResponse({'typing': typing})
