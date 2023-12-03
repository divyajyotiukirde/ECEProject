# to start the controller
# to start the workload - read job from job queue
import sys
import time
import middleware
from LocalController import PIDController
from GlobalController import GlobalPIDController
import monitor

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
        

    global_controller = GlobalPIDController(0)

    job_id = 0

    while True:
        cpu = monitor.get_cluster_utilization()
        if cpu:
            global_controller.update_utilization(cpu)
            global_controller.run_controller()
            nodes = int(global_controller.get_number_of_nodes())
            print("number of nodes: ", nodes)
            print("active pods: ", monitor.get_active_pods())

            for node in range(nodes):
                local_controller = PIDController(0)
                curr_node = node+1
                # avoid assigning jobs to dead node
                # check if node dead here
                if nodes==1:
                    curr_node = global_controller.get_node()
                local_cpu = monitor.get_node_cpu_utilization(curr_node)
                if local_cpu:
                    local_controller.update_utilization(local_cpu)
                    local_controller.run_controller()
                    pods = int(local_controller.get_number_of_pods())
                    print("node: ", curr_node)
                    print("number of pods: ", pods)

                    if job_id >= len(jobs):
                        exit(0)

                    if pods > len(jobs):
                        for job in jobs:
                            print("on job id: ", job_id)
                            if job_id >= len(jobs):
                                break
                            job = job.strip()
                            # i/p example stress-ng --io 4 --vm 5 --vm-bytes 2G --timeout 5m
                            # o/p example "--io", "4", "--vm", "5", "--vm-bytes", "2G", "--timeout", "5m"
                            formatted_output = parse_args(job)
                            # start pod on curr_node
                            middleware.start_pod(formatted_output, curr_node)
                            time.sleep(15) # process jobs after every 15s
                            job_id+=1
                    else:
                        count=0
                        while job_id < len(jobs):
                            print("on job id: ", job_id)
                            if job_id >= len(jobs):
                                break
                            if pods==count:
                                break
                            job = jobs[job_id]
                            job = job.strip()
                            formatted_output = parse_args(job)
                            # start pod on curr_node
                            middleware.start_pod(formatted_output, curr_node)
                            time.sleep(15) # process jobs after every 15s
                            count+=1
                            job_id+=1
                    
