from flask import Flask, render_template, request
from repository.topic_repository import TopicRepositoryActor
import json


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
repositoryActor = TopicRepositoryActor.start()


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/v1/topics', methods=['GET', 'PUT'])
def topics():
  if request.method == 'GET':
    topics = repositoryActor.ask({'command': 'query',
                                  'offset': int(request.args.get('offset')),
                                  'limit': int(request.args.get('limit'))})
    response = list(map(lambda t: t.__dict__(), topics))
    return str(json.dumps(response))
  elif request.method == 'PUT':
    repositoryActor.tell(json.loads(request.data.decode('utf-8')))
    return 'ok'


@app.route('/v1/up-vote', methods=['POST'])
def up_vote():
  req = json.loads(str(request.data.decode('utf-8')))
  by = req.get('by')
  topic = req.get('topic')
  repositoryActor.tell({'command': 'up_vote', 'by': by, 'topic': topic})
  return 'ok'


@app.route('/v1/down-vote', methods=['POST'])
def down_vote():
  req = json.loads(request.data.decode('utf-8'))
  by = req.get('by')
  topic = req.get('topic')
  repositoryActor.tell({'command': 'down_vote', 'by': by, 'topic': topic})
  return 'ok'


if __name__ == '__main__':
  app.run(port=8080)
