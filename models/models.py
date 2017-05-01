class Topic:
  def __init__(self, dict):
    self.topic = dict.get('topic')
    self.url = dict.get('url')
    self.user = dict.get('user')
    self.votes = 0
    self.up_voted_by = set()
    self.down_voted_by = set()

  def __recalculate_votes(self):
    self.votes = len(self.up_voted_by) - len(self.down_voted_by)

  def get_votes(self):
    return self.votes

  def as_dict(self):
    return {
      'topic': self.get_topic(),
      'user': self.get_user(),
      'url': self.get_url(),
      'votes': self.get_votes()
    }

  def get_url(self):
    return self.url

  def get_topic(self):
    return self.topic

  def get_user(self):
    return self.user

  def up_vote(self, by):
    self.up_voted_by.add(by)
    if self.down_voted_by.__contains__(by):
      self.down_voted_by.remove(by)
    self.__recalculate_votes()

  def down_vote(self, by):
    self.down_voted_by.add(by)
    if self.up_voted_by.__contains__(by):
      self.up_voted_by.remove(by)
    self.__recalculate_votes()
