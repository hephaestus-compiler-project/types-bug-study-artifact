import copy
import json
import sys

with open(sys.argv[1]) as f:
    data = json.load(f)

entries = []
for k, v in data.items():
    element = copy.deepcopy(v)
    element['bug_id'] = k
    entries.append(element)

with open(sys.argv[2], 'w') as f:
    json.dump(entries, f, indent=2)
