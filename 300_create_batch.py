import yaml

path = '201_batches.sh'

lines = []

with open('settings.yml') as file:
    obj = yaml.safe_load(file)

    size = len(obj.keys())
    
    count = 1
    for key in obj:
        lines.append("echo {} / {} {} : {}".format(count, size, key, obj[key]))
        lines.append("sh 200_batch.sh {} {} True".format(obj[key], key))

        count += 1

with open(path, mode='w') as f:
    f.write('\n'.join(lines))