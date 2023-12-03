
SamplingTime = 1

class PIDController():
    def __init__( self, initial_pods ):

        self.kp = -4.496
        self.ki = 7.543
        self.kd = 1.746

        self.i = 0
        self.d = 0
        self.prev_e = 0

        self.initial_u = initial_pods

        # for that particular node
        self.max_pods = self.initial_u

        self.r = 0.8
        self.current_y = 0
        self.current_pods = self.initial_u
        

    def _adjust(self, yk):
        err = (self.r-yk)
        self.i += SamplingTime*err
        self.d = (err - self.prev_e)/SamplingTime # rate of change of error
        u = self.kp*err + self.i*self.ki + self.kd*self.d
        self.prev_e = err
        #print(u, yk)
        if u>self.max_pods:
            self.max_pods = u
            return self.max_pods
        if u<1:
            return 1
        return u
    
    def _get_utilization(self):
        return self.current_y

    # APIs exposed to middleware

    # from monitoring
    def update_utilization(self, y):
        self.current_y = y
    
    # for the middleware
    def get_number_of_pods(self):
        return self.current_pods
    
    # for the global controller to up another node
    def get_max_pods(self):
        return self.max_pods

    # for every job check utilization
    def run_controller(self):
        y = self._get_utilization()
        self.current_pods = self._adjust(y)
        if self.max_pods < self.current_pods:
            self.max_pods = self.current_pods
