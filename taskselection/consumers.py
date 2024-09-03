
from channels import Group
from channels.sessions import channel_session
#from .models import Room

@channel_session
def ws_connect(message):
  print(message.content)
  # TODO: check for authentication
  Group('task_selections').add(message.reply_channel)
  message.channel_session['tasks'] = 'task_selections'
  message.reply_channel.send({'accept': True})

@channel_session
def ws_disconnect(message):
  #print('disconnect ' + message.content)
  Group('task_selections').discard(message.reply_channel)

