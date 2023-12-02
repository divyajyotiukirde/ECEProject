import monitor
import time

SAMPLING_RATE = 15

def main():
    while True:
        monitor.get_pod_status()
        monitor.get_cpu_utilization()
        time.sleep(SAMPLING_RATE)
    pass

if __name__ == "__main__":
    main()
