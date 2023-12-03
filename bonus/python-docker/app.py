from flask import Flask, request, jsonify
from processor import JobScheduler

job_scheduler = JobScheduler()
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Docker!'

@app.route('/submit', methods=['GET'])
def submit_job():
    job_str = request.args.get('job')
    job_scheduler.add_in_queue(job_str)
    job_scheduler.process_queue()
    return job_str + ' Job submitted!'

@app.route('/stop', methods=['GET'])
def stop_job():
    return ' Job stopped!'

# comment this when building docker image
if __name__ == '__main__':
    app.run(debug=True)