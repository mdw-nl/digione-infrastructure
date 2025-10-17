from config_handler import Config
from consumer import Consumer
import os
import logging
import subprocess
import re
import json
import shutil


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
        self.clear_folder_paths = ["data/anonymised_datasets", "data/xnat_listener"]
    
    def open_connection(self):
        self.anonymizer = Consumer(rmq_config=self.rabbitMQ_config_anonymizer)
        # self.radiomics = Consumer(rmq_config=self.rabbitMQ_config_radiomics)

        self.anonymizer.open_connection_rmq()
        # self.radiomics.open_connection_rmq()
        
    def clear_folder(self): 
        for folder_path in self.clear_folder_paths:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.remove(file_path)  
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  
                except Exception as e:
                    logging.info(f"Failed to delete {file_path}. Reason: {e}")

    def send_messages(self, message_folder):
        self.anonymizer.send_message(message_folder)
    
if __name__ == '__main__':
    pipeline = initiate_pipeline()
    pipeline.clear_folder()
    pipeline.open_connection()
    pipeline.send_messages("messages/anonymiser_messages")