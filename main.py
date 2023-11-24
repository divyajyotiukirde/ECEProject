# to start the controller
# to start the workload - read job from job queue
import sys
import subprocess
import time
import middleware
from LocalController import PIDController
import monitor

# delete status-completed pods
def clean_pods():
    command = f"kubectl delete pod --field-selector=status.phase==Succeeded"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stdout)

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

    # update a,b values
    a,b = 0.007, 0.03

    controller_instance = PIDController(a,b,1)
    max_pods = []

    job_id = 0

    while True:
        cpu = monitor.get_cpu_utilization()
        controller_instance.update_utilization(cpu)
        controller_instance.run_controller()
        pods = controller_instance.get_number_of_pods()

        if job_id >= len(jobs):
            exit(0)

        if pods > len(jobs):
            for job in jobs:
                job = job.strip()
                # i/p example stress-ng --io 4 --vm 5 --vm-bytes 2G --timeout 5m
                # o/p example "--io", "4", "--vm", "5", "--vm-bytes", "2G", "--timeout", "5m"
                formatted_output = parse_args(job)
                # start pod on node 1
                middleware.start_pod(formatted_output, 1)
                time.sleep(15) # process jobs after every 15s
                job_id+=1
        else:
            count=0
            while job_id < len(jobs):
                if pods==count:
                    break
                job = jobs[job_id]
                job = job.strip()
                formatted_output = parse_args(job)
                # start pod on node 1
                middleware.start_pod(formatted_output, 1)
                time.sleep(15) # process jobs after every 15s
                count+=1




    
