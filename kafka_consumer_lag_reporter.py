import os
import subprocess
import argparse

# VERSION 0.1
# from https://github.com/paksu/kafka-consumer-lag-telegraf-reporter

OUTPUT_KEYS = ['topic', 'partition', 'lag']

def parse_output(input_from_checker):
    """
    Parses the output from kafka-consumer-groups.sh, converts metrics in to integers and returns
    a list of dicts from each row as a response
    """
    output = []
    for line in input_from_checker:
        # Parse only lines with data
        if line.strip() and not line.startswith('TOPIC'):
            columns = line.split()

            # Only pick the columns we are interested in
            topic = columns[0]
            metric_columns = [int(c) for c in [columns[1],columns[4]]]

            key_and_value_pairs = zip(OUTPUT_KEYS, [topic] + metric_columns)
            output.append(dict(key_and_value_pairs))

    return output


def to_line_protocol(parsed_output):
    """
    Converts the parsed output to InfluxDB line protocol metrics
    """
    return ["kafka.consumer_offset,topic={topic},partition={partition} lag={lag}"
            .format(**line) for line in parsed_output]


def get_kafka(args):
    """
    Gets consumer offsets from kafka via kafka-consumer-groups.sh

    Tested on Kafka 1.0
    """
    # append trailing slash
    if args.kafka_dir[-1] != "/":
        args.kafka_dir = args.kafka_dir + "/"

    params = [
        '{}bin/kafka-consumer-groups.sh'.format(args.kafka_dir),
        '--group {}'.format(args.group),
        '--describe'
    ]
    params = params + ['--bootstrap-server', args.bootstrap_server]
    fnull = open(os.devnull, 'w')
    cmd = subprocess.Popen(" ".join(params), shell=True, stdout=subprocess.PIPE, stderr=fnull)

    return [line for line in cmd.stdout]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--kafka-dir', default='/opt/kafka/', help='Kafka base directory', required=True)
    parser.add_argument('--group', help='Kafka group to check', required=True)
    parser.add_argument('--bootstrap-server', help='Which kafka to query (for new consumers)', required=True)
    args = parser.parse_args()

    output = get_kafka(args)
    parsed_output = parse_output(output)
    for line in to_line_protocol(parsed_output):
        print line
