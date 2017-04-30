from flask import Flask, render_template, request
from repository.topic_repository import TopicRepositoryActor
import json

app = Flask(__name__)
repositoryActor = None


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/v1/topics/', methods=['GET', 'PUT'])
def topics():
  if request.method == 'GET':
    return str(json.dumps(repositoryActor.ask({'command': 'query', 'offset': 0, 'step': 10})))
  elif request.method == 'PUT':
    repositoryActor.tell(json.loads(request.data))
    return "Ok"

@app.route('/v1/up-vote/', methods=['POST'])
def topics():
  repositoryActor.tell(json.loads(request.data))


@app.route('/v1/down-vote/', methods=['POST'])
def topics():
  repositoryActor.tell(json.loads(request.data))


if __name__ == '__main__':
  repositoryActor = TopicRepositoryActor.start()
  app.run(debug=True, port=8080)
