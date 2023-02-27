import psutil
import re
import yaml
import humanize
import datetime

def information(proc_id=None):
    if proc_id:
        return __process_information(proc_id)

    return {
        "ram": humanize.naturalsize(psutil.virtual_memory().total),
        "disk": humanize.naturalsize(psutil.disk_usage('/').total),
        "boot_time": humanize.naturaltime(datetime.datetime.fromtimestamp(psutil.boot_time()))
    }

def chart(proc_id=None):
    if proc_id:
        return __process_chart(proc_id)

    current_time = datetime.datetime.now()

    return {
        "label": f"{current_time.hour}:{current_time.minute}:{current_time.second}",
        "datasets": {
            "Memory": psutil.virtual_memory().percent,
            "CPU": psutil.cpu_percent()
        }
    }

# Return a list of processes that match the information provided in process.yml
def processes():
    processes = {}

    with open('processes.yml', 'r') as file:
        process_matchers = yaml.safe_load(file)

        for proc in psutil.process_iter(['pid', 'name', 'cwd']):
            for process_name, process_matcher in process_matchers.items():
                cwd_matcher = process_matcher.get('cwd', None)

                if proc.info['name'] == process_matcher['name'] and proc.info['cwd'] == cwd_matcher:
                    # Join the command line arguments into a string for easier parsing and parse it with the
                    # regex defined in processes.yml
                    if re.search(process_matcher['cmdline'], ' '.join(proc.cmdline())):
                        processes[process_name] = proc.info['pid']

    return processes

def __process_chart(proc_id):
    current_time = datetime.datetime.now()

    return {
        "label": f"{current_time.hour}:{current_time.minute}:{current_time.second}",
        "datasets": {
            "Memory": psutil.Process(int(proc_id)).memory_percent(),
            "CPU": psutil.Process(int(proc_id)).cpu_percent()
        }
    }

def __process_information(proc_id):
    process = psutil.Process(int(proc_id))

    return {
        "name": process.name(),
        "start_time": humanize.naturaltime(datetime.datetime.fromtimestamp(process.create_time())),
        "cwd": process.cwd(),
        "cmdline": ' '.join(process.cmdline()),
    }