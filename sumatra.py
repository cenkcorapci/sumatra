from flask import Flask, render_template, request
from actors.topic_actor import TopicActor
import json
import os


class CustomFlask(Flask):
  '''
  template rendering configuration needed to make it work with Vue.js
  '''
  jinja_options = Flask.jinja_options.copy()
  jinja_options.update(dict(
    block_start_string='(%',
    block_end_string='%)',
    variable_start_string='((',
    variable_end_string='))',
    comment_start_string='(#',
    comment_end_string='#)',
  ))


app = CustomFlask(__name__)
topicActor = TopicActor.start()


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/v1/topics', methods=['GET', 'PUT'])
def topics():
  if request.method == 'GET':
    topics = topicActor.ask({'command': 'query',
                             'offset': int(request.args.get('offset')),
                             'limit': int(request.args.get('limit'))})
    response = list(map(lambda t: t.as_dict(), topics))
    return str(json.dumps(response))
  elif request.method == 'PUT':
    topicActor.tell(json.loads(request.data.decode('utf-8')))
    return 'ok'


@app.route('/v1/up-vote', methods=['POST'])
def up_vote():
  req = json.loads(str(request.data.decode('utf-8')))
  by = req.get('by')
  topic = req.get('topic')
  topicActor.tell({'command': 'up_vote', 'by': by, 'topic': topic})
  return 'ok'


@app.route('/v1/down-vote', methods=['POST'])
def down_vote():
  req = json.loads(request.data.decode('utf-8'))
  by = req.get('by')
  topic = req.get('topic')
  topicActor.tell({'command': 'down_vote', 'by': by, 'topic': topic})
  return 'ok'


if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
