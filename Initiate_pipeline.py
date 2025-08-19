from config_handler import Config
from consumer import Consumer
import os
import logging
import subprocess
import re
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger()

"""This class is made to send a message to the pipeline and for the data to automatically go through the whole pipeline."""

class initiate_pipeline:
    def __init__(self):
        self.rabbitMQ_config_anonymizer = Config("anonymizer")
        # self.rabbitMQ_config_radiomics = Config("rabbitMQradiomics")
    
    def open_connection(self):
        self.anonymizer = Consumer(rmq_config=self.rabbitMQ_config_anonymizer)
        # self.radiomics = Consumer(rmq_config=self.rabbitMQ_config_radiomics)

        self.anonymizer.open_connection_rmq()
        # self.radiomics.open_connection_rmq()

    def send_messages(self, message_folder):
        self.anonymizer.send_message(message_folder)
    
if __name__ == '__main__':
    pipeline = initiate_pipeline()
    pipeline.open_connection()
    pipeline.send_messages("messages/anonymiser_messages")