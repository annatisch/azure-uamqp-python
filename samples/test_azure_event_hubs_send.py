#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

import os
import logging

import uamqp
from uamqp import authentication


log = logging.getLogger(__name__)


def test_event_hubs_simple_send(live_eventhub_config):
    msg_content = b"Hello world"
    uri = "sb://{}/{}".format(live_eventhub_config['hostname'],live_eventhub_config['event_hub'])
    sas_auth = authentication.SASTokenAuth.from_shared_access_key(
        uri, live_eventhub_config['key_name'], live_eventhub_config['access_key'])
    target = "amqps://{}/{}".format(live_eventhub_config['hostname'], live_eventhub_config['event_hub'])
    uamqp.send_message(target, msg_content, auth=sas_auth)


def test_event_hubs_client_send(live_eventhub_config):
    annotations={b"x-opt-partition-key": b"PartitionKeyInfo"}
    msg_content = b"hello world"

    message = uamqp.Message(msg_content, annotations=annotations)

    uri = "sb://{}/{}".format(live_eventhub_config['hostname'], live_eventhub_config['event_hub'])
    sas_auth = authentication.SASTokenAuth.from_shared_access_key(
        uri, live_eventhub_config['key_name'], live_eventhub_config['access_key'])

    target = "amqps://{}/{}".format(live_eventhub_config['hostname'], live_eventhub_config['event_hub'])
    send_client = uamqp.SendClient(target, auth=sas_auth, debug=False)
    send_client.queue_message(message)
    send_client.send_all_messages()


def test_event_hubs_single_send(live_eventhub_config):
    annotations={b"x-opt-partition-key": b"PartitionKeyInfo"}
    msg_content = b"hello world"

    message = uamqp.Message(msg_content, annotations=annotations)

    uri = "sb://{}/{}".format(live_eventhub_config['hostname'], live_eventhub_config['event_hub'])
    sas_auth = authentication.SASTokenAuth.from_shared_access_key(
        uri, live_eventhub_config['key_name'], live_eventhub_config['access_key'])

    target = "amqps://{}/{}".format(live_eventhub_config['hostname'], live_eventhub_config['event_hub'])
    send_client = uamqp.SendClient(target, auth=sas_auth, debug=False)
    send_client.send_message(message, close_on_done=True)


def test_event_hubs_batch_send(live_eventhub_config):
    def data_generator():
        for i in range(500):
            msg_content = "Hello world {}".format(i).encode('utf-8')
            yield msg_content

    message_batch = uamqp.message.BatchMessage(data_generator())

    uri = "sb://{}/{}".format(live_eventhub_config['hostname'], live_eventhub_config['event_hub'])
    sas_auth = authentication.SASTokenAuth.from_shared_access_key(
        uri, live_eventhub_config['key_name'], live_eventhub_config['access_key'])

    target = "amqps://{}/{}/Partitions/0".format(live_eventhub_config['hostname'], live_eventhub_config['event_hub'])
    send_client = uamqp.SendClient(target, auth=sas_auth, debug=False)
    send_client.queue_message(message_batch)
    send_client.send_all_messages()
