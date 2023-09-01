from django.core.management.base import BaseCommand
from kfsd.apps.core.msmq.rabbitmq.base import RabbitMQ
from kfsd.apps.core.utils.time import Time
from kfsd.apps.endpoints.serializers.common.outpost import MsgSerializer

from kfsd.apps.core.common.logger import Logger, LogLevel
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.models.tables.outpost import Outpost, send_msg
from kfsd.apps.models.constants import (
    OUTPOST_ACTION_CLEAR,
    USER_ACTION_CREATE,
    USER_ACTION_DELETE,
    USER_ACTION_UPDATE,
)

from kfsd.apps.models.tables.reference import Reference
from kfsd.apps.endpoints.serializers.common.reference import (
    ReferenceViewModelSerializer,
)


import json

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


def clear_outpost(data):
    outpostQS = Outpost.objects.filter(status="E").order_by("created")
    identifiers = [outpost.identifier for outpost in outpostQS]
    logger.info(
        "Recd CLEAR_OUTPOST command on msmq, identifiers: {} with 'Error' status found.".format(
            identifiers if identifiers else None
        )
    )
    for outpostIns in outpostQS:
        send_msg(outpostIns)


def construct_ref(sourceModel, data):
    identifier = data.pop("identifier")
    return {"identifier": identifier, "type": sourceModel, "attrs": data}


def create_ref(source, data):
    idSerailizer = ReferenceViewModelSerializer(data=construct_ref(source, data))
    idSerailizer.is_valid(raise_exception=True)
    idSerailizer.save()


def update_ref(source, data):
    refData = construct_ref(source, data)
    identifier = DictUtils.get(refData, "identifier")
    instance = Reference.objects.get(identifier=identifier)
    serializedData = ReferenceViewModelSerializer(instance, data=refData, partial=True)
    serializedData.is_valid(raise_exception=True)
    serializedData.save()


def delete_ref(source, data):
    refData = construct_ref(source, data)
    identifier = DictUtils.get(refData, "identifier")
    instance = Reference.objects.get(identifier=identifier)
    instance.delete()


def action_map_to_source_model(action):
    if action in [USER_ACTION_CREATE, USER_ACTION_UPDATE, USER_ACTION_DELETE]:
        return "USER"


def process_ref(requestData):
    action = DictUtils.get_by_path(requestData, "action")
    data = DictUtils.get_by_path(requestData, "data")
    targetModel = DictUtils.get(requestData, "target_model", "")
    logger.info(
        "Recd {} command on msmq, request data: {}".format(
            action, json.dumps(requestData, indent=4)
        )
    )
    if action in [
        USER_ACTION_CREATE,
    ]:
        create_ref(targetModel, data)

    if action in [
        USER_ACTION_UPDATE,
    ]:
        update_ref(targetModel, data)

    if action in [
        USER_ACTION_DELETE,
    ]:
        delete_ref(targetModel, data)


callback_map = {
    OUTPOST_ACTION_CLEAR: clear_outpost,
    USER_ACTION_CREATE: process_ref,
    USER_ACTION_UPDATE: process_ref,
    USER_ACTION_DELETE: process_ref,
}


def base_callback(ch, method, properties, body):
    bodyStr = body.decode().replace("'", '"')
    jsonStr = json.loads(bodyStr)
    serializedData = MsgSerializer(data=jsonStr)
    serializedData.is_valid(raise_exception=True)

    action = DictUtils.get(serializedData.data, "action")
    if action in callback_map:
        callback_map[action](serializedData.data)
    else:
        logger.error("Action : {} not handled in message consumption".format(action))


class Command(BaseCommand):
    help = "Listens to a RabbitMQ topic"

    def __init__(self, callbackFn=base_callback):
        self.__callbackFn = callbackFn

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--service_config_id",
            type=str,
            help="Service Config Id",
        )

    def connectToMSMQ(self, serviceConfigId):
        try:
            msmqHandler = RabbitMQ.getSingleton(serviceConfigId)
            return msmqHandler
        except Exception as e:
            print(e)
            logger.error(
                "Error connecting to RabbitMQ, check if RabbitMQ instance is up!"
            )
            Time.sleep(30)
            self.connectToMSMQ()

    def handle(self, *args, **options):
        logger.info("Listening to MSMQ messages...")
        serviceConfigId = DictUtils.get(options, "service_config_id")
        msmqHandler = self.connectToMSMQ(serviceConfigId)
        msmqHandler.consumeQueues(self.__callbackFn)
        msmqHandler.startConsuming()
