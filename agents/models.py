from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Prompt(models.Model):

    name = models.CharField(max_length=50,default='Agent')
    description = models.TextField(blank=True)
    prompt = models.TextField()
    createAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.prompt
    
    class Meta:
        verbose_name = '001 - Prompt'
        verbose_name_plural = '001 - Prompts'
    

class Agent(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    photo = models.ImageField(upload_to='agents/%Y/%m/%d/', null=True, blank=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    prompt = models.ManyToManyField(Prompt)
    createAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '002 - Agent'
        verbose_name_plural = '002 - Agents'
    

class BudgedMonth(models.Model):

    reference = models.DateField()
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    value = models.FloatField(default=0.0)
    createAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.agent.name
    
    class Meta:
        verbose_name = '002.001 - Budged Month'
        verbose_name_plural = '002.001 - Budged Months'
    
    
class Chat(models.Model):

    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    promptParams = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    createAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.agent.name
    
    class Meta:
        verbose_name = '003 - Chat'
        verbose_name_plural = '003 - Chats'
    
    
class ChatExtraInformation(models.Model):

    CHOICES = (
        ('AAA','Pontuation'),
    )

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    key = models.CharField(max_length=3, choices = CHOICES)
    data = models.TextField(blank=True)
    createAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.chat.agent.name
    
    class Meta:
        verbose_name = '003.001 - Chat Extra Information'
        verbose_name_plural = '003.001 - Chat Extra Informations'
    

class Data(models.Model):

    CHOICES = (
        ('USR','User'),
        ('AGT','Agent'),
        ('EMP','Employee')
    )

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    data = models.TextField()
    origin = models.CharField(max_length=3, choices=CHOICES, default='AGT')
    extraInformation = models.TextField(blank=True)
    createAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.chat.name
    
    class Meta:
        verbose_name = '004 - Data'
        verbose_name_plural = '004 - Datas'
    

@receiver(post_save, sender=Chat)
def post_save_chat(sender, instance, **kwargs):
    if kwargs['created']:
        querysetAgent = Agent.objects.filter(id=instance.agent.id)
        querysetPrompt = Prompt.objects.filter(agent__in=querysetAgent)
        instance.promptParams = ', '.join([str(p.prompt) for p in querysetPrompt])
        instance.save()
        print(querysetPrompt)