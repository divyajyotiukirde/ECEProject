SamplingTime = 1

class GlobalPIDController():
    def __init__( self, initial_nodes ):

        # update here
        self.kp = 1
        self.ki = 1
        self.kd = 1

        self.i = 0
        self.d = 0
        self.prev_e = 0

        self.initial_u = initial_nodes

        # for that particular node
        self.max_nodes = self.initial_u
        self.node = 1
        self.dead_node = -1

        self.r = 0.8
        self.current_y = 0
        self.current_nodes = self.initial_u
        

    def _adjust(self, yk):
        err = (self.r-yk)
        self.i += SamplingTime*err
        self.d = (err - self.prev_e)/SamplingTime # rate of change of error
        u = self.kp*err + self.i*self.ki + self.kd*self.d
        self.prev_e = err
        print(u, yk)
        if err>0:
            return 1
        if u<1:
            return 1
        if u>self.max_nodes:
            self.max_nodes = u
            return self.max_nodes
        return u
    
    def _get_utilization(self):
        return self.current_y

    # APIs exposed to middleware

    def restart_node(self, node):
        self.node = node
        self.dead_node = -1

    def kill_node(self, node):
        self.dead_node = node

    def switch_nodes(self):
        if self.current_y > 0.8:
            self.node = 2
        else:
            self.node = 1

    def get_node(self):
        if self.dead_node==1:
            return 2
        if self.dead_node==2:
            return 1
        if self.current_y<0.8:
            return 1
        return self.node
    
    def check_dead_node(self):
        return self.dead_node

    # from monitoring
    def update_utilization(self, y):
        self.current_y = y
    
    # for the middleware
    def get_number_of_nodes(self):
        return self.current_nodes
    
    # for the global controller to up another node
    def get_max_nodes(self):
        return self.max_nodes

    # for every job check utilization
    def run_controller(self):
        y = self._get_utilization()
        self.current_nodes = self._adjust(y)
        if self.max_nodes < self.current_nodes:
            self.max_nodes = self.current_nodes
