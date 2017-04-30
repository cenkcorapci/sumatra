import pykka
from model.models import Topic


class TopicRepositoryActor(pykka.ThreadingActor):
  def __init__(self):
    super(TopicRepositoryActor, self).__init__()
    self.topics = {}  # using a set for random access on the topics so we can easily vote them.

  def on_receive(self, message):
    if message.get('command') == 'query':
      # get topics
      l = sorted(self.topics.values(), key=lambda t: t.get_votes())
      return l[int(message.get('offset')):int(message.get('step'))]
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


if __name__ == '__main__':
  actor = TopicRepositoryActor.start()
  actor.tell({'url': 'test', 'topic': 'topic', 'user': 'user'})
  actor.tell({'url': 'test2', 'topic': 'topic2', 'user': 'user'})

  print(list(map(lambda t: t.get_topic(), actor.ask({'command': 'query', 'offset': 0, 'step': 10}))))
  actor.tell({'command': 'up_vote', 'topic': 'topic', 'by': 'someone'})
  actor.tell({'command': 'down_vote', 'topic': 'topic2', 'by': 'someone'})
  print(list(map(lambda t: t.get_topic(), actor.ask({'command': 'query', 'offset': 0, 'step': 10}))))
  print(list(map(lambda t: t.get_topic(), actor.ask({'command': 'query', 'offset': 0, 'step': 1}))))

  actor.stop()
