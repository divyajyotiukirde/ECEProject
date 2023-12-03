# to start the controller
# to start the workload - read job from job queue
import sys
import time
import subprocess
from urllib.parse import urlencode
import monitor

def parse_args(job):
    elements = job.split()
    pairs = [(elements[i], elements[i + 1]) for i in range(1, len(elements), 2)]
    formatted_output = ', '.join(f'"{key}", "{value}"' for key, value in pairs)
    return formatted_output

def get_cpu_info():
    cpu_info = []
    cpu_info.append(str(monitor.get_cluster_utilization()))
    cpu_info.append(str(monitor.get_node_cpu_utilization(1)))
    cpu_info.append(str(monitor.get_node_cpu_utilization(2)))
    cpu_str = ','.join(cpu_info)
    return cpu_str

if __name__ == '__main__':

    args = sys.argv
    input_file = args[1]
    with open(input_file, 'r') as f:
        jobs = f.readlines()
        
    job_id = 0

    for job in jobs:
        print("on job id: ", job_id)
        cpu_info = get_cpu_info()
        job = job.strip()
        formatted_output = parse_args(job)
        params = {
            'job': formatted_output,
            'cpu': cpu_info
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
