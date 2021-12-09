from flask import Flask, request, jsonify
from celery import Celery

import as3utils

app = Flask(__name__)
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"

celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)


@celery.task(bind=True)
def config_worker(bigip, parsed_data):
    as3utils.process_request(bigip, parsed_data)


@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        return (
            jsonify({"message": "Please POST on /config to configure BIGIP"}),
            200
        )


@app.route("/config", methods=["POST"])
def post_config():
    config = request.get_json()
    parsed_data = as3utils.parse_request(config)
    for bigip in parsed_data['list_of_bigips']:
        config_worker(bigip, parsed_data)


if __name__ == '__main__':
    app.run(debug=True)
