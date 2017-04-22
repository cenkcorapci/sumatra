import pykka
from model.models import Topic


class TopicRepositoryActor(pykka.ThreadingActor):
  def __init__(self):
    super(TopicRepositoryActor, self).__init__()
    self.topics = {}

  def on_receive(self, message):
    if message.get('command') == 'query':
      l = sorted(self.topics.values(), key=lambda t: t.get_votes())
      return l[int(message.get('offset')):int(message.get('step'))]
    elif message.get('command') == 'up_vote':
      t = self.topics.get(message.get('topic'))
      if (t != None):
        t.up_vote()
        self.topics[t.get_topic()] = t
    elif message.get('command') == 'down_vote':
      t = self.topics.get(message.get('topic'))
      if (t != None):
        t.down_vote()
        self.topics[t.get_topic()] = t
    else:
      t = Topic(message)
      self.topics[t.get_topic()] = t


if __name__ == '__main__':
  actor = TopicRepositoryActor.start()
  actor.tell({'url': 'test', 'topic': 'topic', 'user': 'user'})
  actor.tell({'url': 'test2', 'topic': 'topic2', 'user': 'user'})

  print(list(map(lambda t: t.get_topic(), actor.ask({'command': 'query', 'offset': 0, 'step': 10}))))
  actor.tell({'command': 'up_vote', 'topic': 'topic'})
  actor.tell({'command': 'down_vote', 'topic': 'topic2'})
  print(list(map(lambda t: t.get_topic(), actor.ask({'command': 'query', 'offset': 0, 'step': 10}))))
  print(list(map(lambda t: t.get_topic(), actor.ask({'command': 'query', 'offset': 0, 'step': 1}))))

  actor.stop()
