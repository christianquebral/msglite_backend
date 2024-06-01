#!/usr/bin/env python3

import requests
import traceback

from flask import request 
from flask_restful import Resource

from kafka import KafkaConsumer, KafkaProducer, TopicPartition
from kafka.admin import KafkaAdminClient, NewTopic
#from kakfa.errors import TopicAlreadyExistsError


class Session(Resource):
	def get(self):
		"""Retrieve session info if exists"""
		session_name = None
		error = None
		try:
			session_name = request.args["session_name"]
			consumer = KafkaConsumer(
				bootstrap_servers="localhost:9092",
				auto_offset_reset="earliest",
			)

			tp = TopicPartition("test_topic",0)
			consumer.assign([tp])

			consumer.seek_to_end(tp)
			last_offset = consumer.position(tp)

			consumer.seek_to_beginning(tp)

			status_code = 202
			server_message = "success"

			records = []
			for message in consumer:
				record = message.value.decode("utf-8")
				records.append(record)

				if message.offset == last_offset - 1:
					break

		except Exception as e:
			error = repr(e)
			status_code = 404
			server_message = "Session not found - has the session been created?"
			records = None

		data = {
			"message": server_message,
			"session_name": session_name,
			"error": error,
			"records": records
		}

		return data, status_code

	def post(self):
		"""Create session if does not already exist"""
		error = None
		try:
			session_name = request.args["session_name"]
			admin_client = KafkaAdminClient(
				bootstrap_servers="localhost:9092",
				client_id="test",
			)
			topics = [NewTopic(name=session_name, num_partitions=1, replication_factor=1)]
			admin_client.create_topics(topics)
			status_code = 202
			server_message = f"Session created - session name is [{session_name}]"
		# except TopicAlreadyExistsError as e:
		# 	status_code = 402 #TODO
		# 	server_message = "A session by this name already exists!"
		# 	error = repr(e)
		except Exception as e:
			error = traceback.format_exc()
			status_code = 500
			server_message = "meow"

		data = {
			"message": server_message,
			"session_name": session_name,
			"error": error
		}

		return data, status_code