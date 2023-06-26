#! /usr/bin/env python3

import boto3
import argparse
import random
from contextlib import closing

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("profile")
    parser.add_argument("streamARN")
    parser.add_argument("-n", "--num-records", type=int, default=10, help="Number of records to write to the stream")
    return parser.parse_args()

def kinesis_client(args):
    session = boto3.Session(profile_name=args.profile)
    return session.client("kinesis")

def random_string(length = 16):
    chars = set()
    chars.update(range(48, 58)) # digits
    chars.update(range(65, 91)) # upper
    chars.update(range(97, 123)) # lower
    chars = tuple(chars)

    return ''.join(chr(x) for x in random.choices(chars, k=length))


def main(args):
    with closing(kinesis_client(args)) as client:
        records = [{
            "Data": s.encode(),
            "PartitionKey": s
        } for s in (random_string() for i in range(args.num_records))]
        for record in records:
            print(record)

        client.put_records(StreamARN=args.streamARN, Records=records)

if __name__ == "__main__":
    main(parse_args())
