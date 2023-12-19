from django.shortcuts import render

from agents.models import Agent, Prompt, Data, BudgedMonth, Chat

# Create your views here.

def agentsView(request):

    querysetAgents = Agent.objects.filter(active=True)
    querysetChats = Chat.objects.filter(agent__in=querysetAgents, active=True)

    obj = {}
    obj['agents'] = querysetAgents
    obj['chats'] = querysetChats

    return render(request, 'agents/agents.html', obj)

def chatView(request, id):

    querysetChat = Chat.objects.get(id=id)
    querysetData = Data.objects.filter(chat=querysetChat)

    obj = {}
    obj['chat'] = querysetChat
    obj['data'] = querysetData
    return render(request, 'agents/chat.html', obj)