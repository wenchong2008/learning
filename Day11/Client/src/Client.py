# /user/bin/env python
__author__ = 'wenchong'


import sys
import pika
import subprocess
import json

from config.setting import RabbitMQ_Server


class Client(object):
    """获取服务器的命令执行并将结果返回给服务器"""
    def __init__(self, ip):
        self.connection = None
        self.channel = None
        self.queue_name = ip
        self.connect()

    def connect(self):
        """连接 RabbitMQ"""
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RabbitMQ_Server))
            channel = connection.channel()

            self.connection = connection
            self.channel = channel

            self.channel.queue_declare(queue=self.queue_name, exclusive=True)

        except pika.exceptions.ChannelClosed:
            print("%s exist! Please define IPAddress again!" % self.queue_name)
            exit()

        except Exception as e:
            print("Connecting RabbitMQ ({}) Failed.\n{}".format(RabbitMQ_Server, e))
            exit()

    def close(self):
        self.connection.close()

    @staticmethod
    def process(command):
        """在本地执行命令并返回结果"""
        command = command.split()
        print(command)
        ret = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        result = ret.stdout.readlines() + ret.stderr.readlines()

        result = [x.decode() for x in result]

        return result

    def request(self, ch, method, props, body):
        """回调函数"""
        response = self.process(json.loads(body.decode()))

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=json.dumps(response)
                         )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self):
        """定义消费者"""
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.request, queue=self.queue_name)

        print("Waiting remote server send command ... ")
        self.channel.start_consuming()


def run():

    ip = None
    if len(sys.argv) == 2:
        ip = sys.argv[1]
    else:
        while not ip:
            try:
                ip = input("Please enter IP: ").strip()
            except KeyboardInterrupt:
                exit("\n")
    try:
        client = Client(ip)
        client.consume()
    except KeyboardInterrupt:
        exit()

if __name__ == '__main__':

    run()
