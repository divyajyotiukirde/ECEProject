import middleware
from LocalController import PIDController
from collections import deque
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)

class JobScheduler():
    def __init__( self ):
        self.job_queue = deque()
        self.job_id = 0

        self.cluster_cpu = 0
        self.node_cpu = []

        self.local_controller_store = []
        total_nodes = 2
        for _ in range(total_nodes):
            controller_instance = PIDController(0)
            self.local_controller_store.append(controller_instance)

    def update_cpu(self, cpu_str):
        if len(cpu_str):
            cpu = cpu_str.split(',')
            if len(cpu)>=2:
                self.cluster_cpu = float(cpu[0])
                self.node_cpu = cpu[1:]

    def add_in_queue(self,job):
        self.job_queue.append(job)

    def is_queue_empty(self):
        return True if len(self.job_queue)==0 else False

    def process_queue(self):
        logging.debug("job id ", self.job_id)
        while len(self.job_queue):
            cpu = self.cluster_cpu
            if cpu:
                curr_node = 1
                if cpu > 0.8:
                    curr_node = 2
                local_controller = self.local_controller_store[curr_node-1]

                local_cpu = float(self.node_cpu[curr_node])
                if local_cpu:
                    local_controller.update_utilization(local_cpu)
                    local_controller.run_controller()
                    pods = int(local_controller.get_number_of_pods())
                    print("node: ", curr_node)
                    print("number of pods: ", pods)

                    if self.job_id >= len(self.job_queue):
                        exit(0)

                    if pods > len(self.job_queue):
                        for job in self.job_queue:
                            print("on job id: ", self.job_id)
                            if self.job_id >= len(self.job_queue):
                                break
                            job = job.strip()
                            # i/p example stress-ng --io 4 --vm 5 --vm-bytes 2G --timeout 5m
                            # o/p example "--io", "4", "--vm", "5", "--vm-bytes", "2G", "--timeout", "5m"
                            # start pod on curr_node
                            middleware.start_pod(job, curr_node)
                            self.job_id+=1
                    else:
                        count=0
                        while self.job_id < len(self.job_queue):
                            print("on job id: ", self.job_id)
                            if self.job_id >= len(self.job_queue):
                                break
                            if pods==count:
                                break
                            job = self.job_queue[self.job_id]
                            job = job.strip()
                            # start pod on curr_node
                            middleware.start_pod(job, curr_node)
                            count+=1
                            self.job_id+=1
                    if curr_node==2 and pods>2:
                        exit(0)
