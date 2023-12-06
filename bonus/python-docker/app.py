from flask import Flask, request, jsonify
from processor import JobScheduler
#import threading

job_scheduler = JobScheduler()
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Docker!'

@app.route('/api/submit', methods=['GET'])
def submit_job():
    job_str = request.args.get('job')
    if job_scheduler.is_queue_empty():
        job_scheduler.add_in_queue(job_str)
        #task = threading.Thread(group=None, target=job_scheduler.process_queue)
        #task.start()
    else:
        job_scheduler.add_in_queue(job_str)
        return job_str + ' Job added to queue!'
    if not job_scheduler.is_processing:
        job_scheduler.process_queue()
        job_scheduler.is_processing = True
    return job_str + ' Job submitted!'

@app.route('/api/stop', methods=['GET'])
def stop_job():
    return ' Job stopped!'

# comment this when building docker image
# if __name__ == '__main__':
#     app.run(debug=True)