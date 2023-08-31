"""
UAV connection handling module.
"""

import logging
from enum import Enum

from pymavlink import mavutil
from redis import Redis

from .receive_loop import ReceiveLoop
from .uav_data import UAVData

logger = logging.getLogger(__name__)


class ConnectionType(Enum):
    DIRECT = 1
    REDIS = 2


class Telemetry:
    """
    It creates an abstraction so that we don't have to worry at a higher level
    about the origin of the data and the destination of the commands sent.
    """

    def __init__(
        self,
        connection_type: ConnectionType = ConnectionType.DIRECT,
        device: str = "udpin:0.0.0.0:14550",
        baud_rate: int = 115200,
        host: str = "localhost",
        port: int = 6379,
    ) -> None:
        self.direct_connection: mavutil.mavudp
        self.redis_connection: Redis
        self.connection_type = connection_type
        self.device = device
        self.baud_rate = baud_rate
        self.host = host
        self.port = port
        self.data = UAVData()

        if self.connection_type == ConnectionType.DIRECT:
            self.make_direct_connection()

        if self.connection_type == ConnectionType.REDIS:
            self.make_redis_connection()

    def make_direct_connection(self) -> None:
        """
        Create a direct data link to the UAV.
        """
        self.direct_connection = mavutil.mavlink_connection(self.device, self.baud_rate)
        self.direct_connection.wait_heartbeat()
        logger.info("heartbeat recived")

        # starts a thread that receives telemetry
        receive_telem_loop = ReceiveLoop(self.direct_connection, self.data)
        receive_telem_loop.start()

    def make_redis_connection(self) -> None:
        """
        Create a connection to the UAV via Redis (Pub/Sub).
        """
        self.redis_connection = Redis(self.host, self.port)

    def send(self, message: bytes) -> None:
        """
        Sends received messages to a pre-designated connection.

        Parameters:
            message: packed MAVLink message
        """
        if self.connection_type == ConnectionType.DIRECT:
            self.direct_connection.write(message)

        if self.connection_type == ConnectionType.REDIS:
            self.redis_connection.xadd("commands", {"commands": message})
