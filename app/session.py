#!/usr/bin/env python3

import requests

from flask import request 
from flask_restful import Resource
from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kakfa.errors import TopicAlreadyExistsError


class Session(Resource):
	def get(self):
		"""Retrieve session info if exists"""
		session_name = request.args["session_name"]
		try:
			consumer = KafkaConsumer(
				"test_topic",
				bootstrap_servers="localhost:9092"
			)
			status_code = 202
			server_message = "success"
		except:
			status_code = 404
			server_message = "Session not found - has the session been created?"

		data = {
			"message": server_message,
			"session_name": session_name
		}

		return data, status_code

	def post(self):
		"""Create session if does not already exist"""
		session_name = request.args["session_name"]
		admin_client = KafkaAdminClient(
			bootstrap_servers="localhost:9092",
			client_id="test" #TODO
		)

		try:
			topics = [NewTopic(name=session_name, num_partitions=1, replication_factor=1)]
			admin_client.create_topics(topics)
			status_code = 202
			server_message = f"Session created - session name is [{session_name}]"
		except TopicAlreadyExistsError:
			status_code = 402 #TODO
			server_message = "A session by this name already exists!"
