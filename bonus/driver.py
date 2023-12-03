# to start the controller
# to start the workload - read job from job queue
import sys
import time
import subprocess
from urllib.parse import urlencode

def parse_args(job):
    elements = job.split()
    pairs = [(elements[i], elements[i + 1]) for i in range(1, len(elements), 2)]
    formatted_output = ', '.join(f'"{key}", "{value}"' for key, value in pairs)
    return formatted_output

if __name__ == '__main__':

    args = sys.argv
    input_file = args[1]
    with open(input_file, 'r') as f:
        jobs = f.readlines()
        
    job_id = 0

    for job in jobs:
        print("on job id: ", job_id)
        job = job.strip()
        formatted_output = parse_args(job)
        params = {
            'job': formatted_output
        }
        encoded_params = urlencode(params)
        # http://cloud-controller.com
        # http://127.0.0.1:5000
        url = "http://cloud-controller.com/submit?" + encoded_params
        print("Requesting... ", url)
        command = f"curl {url}"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)
        time.sleep(15)
        job_id+=1
