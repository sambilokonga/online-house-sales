from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from item.models import Item

from .forms import ConversationMessageForm
from .models import Conversation

@login_required
def new_conversation(request, item_pk):
    """
    Create a new conversation between the current user and another user regarding a specific item.
    """
 
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('dashboard:index')
    
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id)

    if request.method == 'POST':
        # Retrieve the recipient user and message content from the form
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
             # Create a new conversation with the current user and the recipient user
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()
            
            # Create a new message in the conversation with the provided content
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            
            # Redirect the user to the conversation detail page
            return redirect('item:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()
   
    return render(request, 'conversation/new.html', {
        'form': form
    })

@login_required
def inbox(request):
        """
    Display the list of conversations for the current user.
    """

    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })

@login_required
def detail(request, pk):
    """
    Display the details of a conversation, including the messages exchanged.
    """

    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        # Retrieve the message content from the form
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            # Create a new message in the conversation with the provided content
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()
            # Redirect the user back to the conversation detail page
            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })
