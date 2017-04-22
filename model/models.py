class Topic:
  def __init__(self, dict):
    self.topic = dict.get('topic')
    self.url = dict.get('url')
    self.user = dict.get('user')
    self.votes = 0

  def get_votes(self):
    return self.votes

  def __dict__(self):
    return {
      'topic': self.topic,
      'url': self.url,
      'votes': self.votes
    }

  def get_url(self):
    return self.url

  def get_topic(self):
    return self.topic

  def get_user(self):
    return self.user

  def up_vote(self):
    self.votes += 1

  def down_vote(self):
    self.votes -= 1
