#! /usr/bin/env python3

import boto3
from time import sleep
from datetime import datetime, timedelta
import argparse
from contextlib import closing

class ShardConsumer:
    def __init__(self, client, stream_arn, shard_id):
        self.client = client
        self.stream_arn = stream_arn
        self.shard_id = shard_id
        self.shard_iterator: str = client.get_shard_iterator(
            StreamARN=self.stream_arn,
            ShardId=self.shard_id,
            ShardIteratorType='LATEST'
        )['ShardIterator']
        self.lag = 1

    def consume(self):
        resp = self.client.get_records(
            StreamARN=self.stream_arn,
            ShardIterator=self.shard_iterator
        )
        self.shard_iterator = resp['NextShardIterator']
        self.lag = resp['MillisBehindLatest']
        for r in resp['Records']:
            yield r['Data']

class KinesisConsumer:
    def __init__(self, profile_name: str, stream_arn: str):
        self.stream_arn = stream_arn

        session = boto3.Session(profile_name=profile_name)
        self.client = session.client("kinesis")

        # Initialize shards and shard iterators
        shard_response = self.client.list_shards(StreamARN=self.stream_arn)
        self.consumers = [ShardConsumer(self.client, self.stream_arn, shard['ShardId']) for shard in shard_response['Shards']]

    def consume(self, timeout=60, max_records=None):
        end_time = datetime.now() + timedelta(seconds=timeout)
        records_consumed = 0
        
        def should_continue():
            return (max_records is None or records_consumed < max_records) and datetime.now() < end_time

        while should_continue():
            consumers_all_caught_up = True
            for consumer in self.consumers:
                for record in consumer.consume():
                    yield record
                    records_consumed += 1
                if consumer.lag:
                    consumers_all_caught_up = False 
            
            if consumers_all_caught_up:
                sleep(1)

    def close(self):
        self.client.close()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("profile")
    parser.add_argument("streamARN")
    parser.add_argument("-t", "--timeout", type=int, default=60)
    parser.add_argument("-r", "--max-records", type=int)
    return parser.parse_args()

def main(args):
    with closing(KinesisConsumer(args.profile, args.streamARN)) as consumer:
        for msg in consumer.consume(args.timeout, args.max_records):
            print(msg.decode())

if "__main__" == __name__:
    main(parse_args())