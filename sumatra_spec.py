import unittest
from sumatra import app, topicActor
import json


class SumatraTestCase(unittest.TestCase):
  def setUp(self):
    self.app = app
    self.client = app.test_client()
    self.client.testing = True

  def test_index_page(self):
    result = self.client.get('/')
    self.assertEqual(result.status_code, 200)

  def test_create_and_upvote(self):
    expected = [{'url': 'test', 'topic': 'topic', 'user': 'user', 'votes': 2},
                {'url': 'test2', 'topic': 'topic2', 'user': 'user', 'votes': 0}]

    # test creating topics
    self.assertEqual(
      self.client
        .put('/v1/topics', data=str(json.dumps(expected[0])))
        .status_code,
      200)

    self.assertEqual(
      self.client
        .put('/v1/topics', data=str(json.dumps(expected[1])))
        .status_code,
      200)
    # test up voting and down voting
    self.assertEqual(
      self.client
        .post('/v1/up-vote', data=str(json.dumps({'by': 'user1', 'topic': 'topic'})))
        .status_code,
      200)
    self.assertEqual(
      self.client
        .post('/v1/up-vote', data=str(json.dumps({'by': 'user1', 'topic': 'topic'})))
        .status_code,
      200)
    self.assertEqual(
      self.client
        .post('/v1/up-vote', data=str(json.dumps({'by': 'user2', 'topic': 'topic'})))
        .status_code,
      200)
    self.assertEqual(
      self.client
        .post('/v1/down-vote', data=str(json.dumps({'by': 'user2', 'topic': 'topic'})))
        .status_code,
      200)

    self.assertEqual(
      self.client
        .post('/v1/up-vote', data=str(json.dumps({'by': 'user2', 'topic': 'topic'})))
        .status_code,
      200)

    result = self.client.get('/v1/topics?offset=0&limit=10')
    topics = json.loads(result.data.decode('utf-8'))
    # order of the elements can be changed, check selected values
    self.assertEqual(list(map(lambda t: [t.get('topic'), t.get('votes')], topics)),
                     list(map(lambda t: [t.get('topic'), t.get('votes')], expected)))

  def tearDown(self):
    topicActor.stop()

if __name__ == '__main__':
  unittest.main()
