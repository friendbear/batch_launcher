# python3
import sys
import os, subprocess
import json
import pprint
import time
import datetime
'''
' batch_launcher
' 
'   Usage: batch_launcher.py batch_unique_id param1 param2 ...
'          returncode: success(0)
'                      failed(1)
'''
# ENV Check
assert(os.environ["JAVA_HOME"])
#assert(os.environ["GJK_ROOT"])
ROOT_DIR = '/Users/k22/Develop/batch_launcher/' #os.environ["GJK_ROOT"]
BIN_DIR = os.path.join(ROOT_DIR, 'bin')
LOG_DIR = os.path.join(ROOT_DIR, 'log')
LIB_DIR = os.path.join(ROOT_DIR, "lib")
LAUNCH_FILE_PATH = os.path.join(ROOT_DIR, 'conf', 'launcher_config.json')

# Arg check
if len(sys.argv) < 3:
    print('Usage: {} batch_unique_id_cd param1 param2 ...'.format(sys.args[0]))
    exit(code=1)


# Launch java batch
def run_for_java(condition=object, args=dict):
    jar = "../lib/" + condition['jar']
    subprocess_args = ["java", "-jar", jar] + args + condition['option']
    returncode = subprocess.run(subprocess_args, check=True).returncode
    return 0 if returncode in condition['success_code'] else 1

# Launch asteria batch
def run_for_asteria(condition=object, args=dict):
    return 0 if 200 in condition['success_code'] else 1

start_time = time.time()
start_datetime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
batch_unique_id = sys.argv[1]
with open(LAUNCH_FILE_PATH, 'r') as config:
    data = json.load(config)

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(data)
batch_condition = None
for condition in data['launcher_configuration']['condition']:
    if condition['id'] == batch_unique_id:
        batch_condition = condition

if batch_condition == None: raise Exception('batchUniqueID No entry Error.')
type(batch_condition)

status = -1
if batch_condition['type'] == 'java':
    status = run_for_java(batch_condition, args=sys.argv[1:])

else:
    status = run_for_asteria(batch_condition, args=sys.argv[1:])

end_time = time.time()
end_datetime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
print('batchUniqueID {} - start {}/end {} - elapsed {} - status {}'.format(batch_condition['id'],
                                                                      start_datetime,
                                                                      end_datetime,
                                                                      end_time - start_time,
                                                                      status ))
exit(code=status)
