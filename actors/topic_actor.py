import pykka
from models.models import Topic


class TopicActor(pykka.ThreadingActor):
  def __init__(self):
    super(TopicActor, self).__init__()
    self.topics = {}  # using a set for random access on the topics so we can easily vote them.

  def on_receive(self, message):
    if message.get('command') == 'query':
      # get topics
      l = sorted(self.topics.values(), key=lambda t: -t.get_votes())
      return l[int(message.get('offset')):int(message.get('limit'))]
    elif message.get('command') == 'up_vote':
      # up vote a certain topic
      t = self.topics.get(message.get('topic'))
      if (t != None):
        t.up_vote(message.get('by'))
        self.topics[t.get_topic()] = t
    elif message.get('command') == 'down_vote':
      # down vote a certain topic
      t = self.topics.get(message.get('topic'))
      if (t != None):
        t.down_vote(message.get('by'))
        self.topics[t.get_topic()] = t
    else:
      # add a new topic
      t = Topic(message)
      self.topics[t.get_topic()] = t
