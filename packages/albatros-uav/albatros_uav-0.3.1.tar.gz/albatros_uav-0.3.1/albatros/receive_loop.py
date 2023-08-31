import logging
from threading import Thread
from typing import Any

from pymavlink.dialects.v20.ardupilotmega import MAVLink_message
from pymavlink.mavutil import mavfile

from .uav_data import UAVData

logger = logging.getLogger()


def get_message_handlers(uav_data: UAVData) -> dict[str, Any]:
    return {
        "HEARTBEAT": uav_data.process_heartbeat,
        "GLOBAL_POSITION_INT": uav_data.process_global_position_int,
        "ATTITUDE": uav_data.process_attitude,
        "GPS_RAW_INT": uav_data.process_gps_raw_int,
        "GPS_STATUS": uav_data.process_gps_status,
        "RADIO_STATUS": uav_data.process_radio_status,
        "RC_CHANNELS_RAW": uav_data.process_rc_channels_raw,
        "SERVO_OUTPUT_RAW": uav_data.process_servo_output_raw,
        "SYS_STATUS": uav_data.process_sys_status,
        "MISSION_REQUEST": uav_data.process_mission_request_int,
        "MISSION_REQUEST_INT": uav_data.process_mission_request_int,
        "MISSION_ACK": uav_data.process_mission_ack,
        "MISSION_ITEM_REACHED": uav_data.process_mission_item_reached,
    }


class ReceiveLoop(Thread):
    def __init__(self, mavlink_connection: mavfile, uav_data: UAVData) -> None:
        super().__init__(name=self.__class__.__name__)
        self.mavlink_connection = mavlink_connection
        self.uav_data = uav_data

    def run(self) -> None:
        logger.info("Starting Telemetry Loop")

        message_handlers = get_message_handlers(self.uav_data)

        while True:
            msg: MAVLink_message = self.mavlink_connection.recv_match(blocking=True)

            if not msg:
                continue

            msg_type = msg.get_type()
            if msg_type in message_handlers:
                message_handlers[msg_type](msg)
