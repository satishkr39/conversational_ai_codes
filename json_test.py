import json

with open("test.json") as f:
    json_text = dict(f.read())

# j_text = json.loads('name')
print(json_text.get('name'))

'''
for item, value in j_text['currentIntent']['slots'].items():
    j_text['currentIntent']['slots'][item] = 'my value 1'


print(j_text['currentIntent']['slots'])

with open('changed_json.json', 'w') as f:
    f.write(json.dumps(j_text, sort_keys=False, indent=4))
    
    '''
