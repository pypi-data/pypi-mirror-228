from pydantic import BaseModel

from .enums import MavMissionResult, MavMissionType


class MavMessage(BaseModel):
    mavpackettype: str = "UNKNOWN"
    timestamp_ms: int = -1


class Heartbeat(MavMessage):
    """The heartbeat message shows that a system or component is present and responding.
    The type and autopilot fields (along with the message component id), allow the receiving system
    to treat further messages from this system appropriately (e.g. by laying out the user interface based on the autopilot).

    :param type: Vehicle or component type. For a flight controller component the vehicle type (quadrotor, helicopter, etc.).
        For other components the component type (e.g. camera, gimbal, etc.).
        This should be used in preference to component id for identifying the component type.
    :param autopilot: Autopilot type / class. Use MAV_AUTOPILOT_INVALID for components that are not flight controllers.
    :param base_mode: System mode bitmap.
    :param custom_mode: A bitfield for use for autopilot-specific flags
    :param system_status: System status flag.
    :param mavlink_version: MAVLink version, not writable by user, gets added by protocol because of magic data type: uint8_t_mavlink_version
    """

    type: int = 0
    autopilot: int = 0
    base_mode: int = 0
    custom_mode: int = 0
    system_status: int = 0
    mavlink_version: int = 0


class GlobalPositionInt(MavMessage):
    """The filtered global position (e.g. fused GPS and accelerometers).
    The position is in GPS-frame (right-handed, Z-up). It is designed as scaled integer
    message since the resolution of float is not sufficient.

    :param time_boot_ms: Timestamp (time since system boot) (ms),
    :param lat: Latitude, expressed (degE7),
    :param lon: Longitude, expressed (degE7),
    :param alt: Altitude (MSL). Note that virtually all GPS modules provide both WGS84 and MSL (mm),
    :param relative_alt: Altitude above ground (mm).
    """

    time_boot_ms: int = 0
    lat: int = 0
    lon: int = 0
    alt: int = 0
    relative_alt: int = 0
    vx: int = 0
    vy: int = 0
    vz: int = 0
    hdg: int = 0


class SysStatus(MavMessage):
    """The general system state.

    :param onboard_control_sensors_present: Bitmap showing which onboard controllers and sensors are present.
        Value of 0: not present. Value of 1: present.
    :param onboard_control_sensors_enabled: Bitmap showing which onboard controllers and sensors are enabled:
        Value of 0: not enabled. Value of 1: enabled.
    :param onboard_control_sensors_health: Bitmap showing which onboard controllers and sensors have an error (or are operational).
        Value of 0: error. Value of 1: healthy.
    :param load: Maximum usage in percent of the mainloop time. Values: [0-1000] - should always be below 1000
    :param voltage_battery: Battery voltage, UINT16_MAX: Voltage not sent by autopilot
    :param current_battery: Battery current, -1: Current not sent by autopilot
    :param battery_remaining: Battery energy remaining, -1: Battery remaining energy not sent by autopilot
    :param drop_rate_comm: Communication drop rate, (UART, I2C, SPI, CAN),
        dropped packets on all links (packets that were corrupted on reception on the MAV)
    """

    onboard_control_sensors_present: int = 0
    onboard_control_sensors_enabled: int = 0
    onboard_control_sensors_health: int = 0
    load: int = 0
    voltage_battery: int = 0
    current_battery: int = 0
    battery_remaining: int = 0
    drop_rate_comm: int = 0


class GPSRawInt(MavMessage):
    """The global position, as returned by the Global Positioning System (GPS).
    This is NOT the global position estimate of the system, but rather a RAW sensor value.

    :param time_usec: Timestamp (UNIX Epoch time or time since system boot).
        The receiving end can infer timestamp format (since 1.1.1970 or since system boot) by checking for the magnitude of the number.
    :param fix_type: GPS fix type.
    :param lat: GPS fix type.
    :param lon: Longitude (WGS84, EGM96 ellipsoid)
    :param alt: Altitude (MSL). Positive for up. Note that virtually all GPS modules provide the MSL altitude in addition to the WGS84 altitude.
    :param eph: GPS HDOP horizontal dilution of position (unitless * 100). If unknown, set to: UINT16_MAX
    :param epv: GPS VDOP vertical dilution of position (unitless * 100). If unknown, set to: UINT16_MAX
    :param vel: GPS ground speed. If unknown, set to: UINT16_MAX
    :param cog: Course over ground (NOT heading, but direction of movement) in degrees * 100, 0.0..359.99 degrees.
        If unknown, set to: UINT16_MAX
    :param satellites_visible: Number of satellites visible. If unknown, set to UINT8_MAX
    :param alt_ellipsoid: Altitude (above WGS84, EGM96 ellipsoid). Positive for up.
    :param h_acc: Position uncertainty.
    :param v_acc: Altitude uncertainty.
    :param vel_acc: Speed uncertainty.
    :param hdg_acc: Heading / track uncertainty
    :param yaw: Yaw in earth frame from north. Use 0 if this GPS does not provide yaw.
        Use UINT16_MAX if this GPS is configured to provide yaw and is currently unable to provide it. Use 36000 for north.
    """

    time_usec: int = 0
    fix_type: int = 0
    lat: int = 0
    lon: int = 0
    alt: int = 0
    eph: int = 0
    epv: int = 0
    vel: int = 0
    cog: int = 0
    satellites_visible: int = 0
    alt_ellipsoid: int = 0
    h_acc: int = 0
    v_acc: int = 0
    vel_acc: int = 0
    hdg_acc: int = 0
    yaw: int = 0


class GPSStatus(MavMessage):
    """The positioning status, as reported by GPS. This message is intended
    to display status information about each satellite visible to the receiver.
    This message can contain information for up to 20 satellites.

    :param satellites_visible: Number of satellites visible
    :param satellite_prn: Global satellite ID
    :param satellite_used: 0: Satellite not used, 1: used for localization
    :param satellite_elevation: Elevation (0: right on top of receiver, 90: on the horizon) of satellite
    :param satellite_azimuth: Direction of satellite, 0: 0 deg, 255: 360 deg.
    :param satellite_snr: Signal to noise ratio of satellite
    """

    satellites_visible: int = 0
    satellite_prn: int = 0
    satellite_used: int = 0
    satellite_elevation: int = 0
    satellite_azimuth: int = 0
    satellite_snr: int = 0


class Attitude(MavMessage):
    """The attitude in the aeronautical frame (right-handed, Z-down, Y-right, X-front, ZYX, intrinsic).

    :param time_boot_ms: Timestamp (time since system boot).
    :param roll: Roll angle (-pi..+pi)
    :param pitch: Pitch angle (-pi..+pi)
    :param yaw: Yaw angle (-pi..+pi)
    :param rollspeed: Roll angular speed
    :param pitchspeed: Pitch angular speed
    :param yawspeed: Yaw angular speed
    """

    time_boot_ms: int = 0
    roll: float = 0
    pitch: float = 0
    yaw: float = 0
    rollspeed: float = 0
    pitchspeed: float = 0
    yawspeed: float = 0


class RcChannelsRaw(MavMessage):
    """The RAW values of the RC channels received. The standard PPM modulation
    is as follows: 1000 microseconds: 0%, 2000 microseconds: 100%.

    :param time_boot_ms: Timestamp (time since system boot).
    :param port: Servo output port (set of 8 outputs = 1 port).
        Flight stacks running on Pixhawk should use: 0 = MAIN, 1 = AUX.
    :param chan1_raw: RC channel 1 value.
    :param chan2_raw: RC channel 2 value.
    :param chan3_raw: RC channel 3 value.
    :param chan4_raw: RC channel 4 value.
    :param chan5_raw: RC channel 5 value.
    :param chan6_raw: RC channel 6 value.
    :param chan7_raw: RC channel 7 value.
    :param chan8_raw: RC channel 8 value.
    :param rssi: Receive signal strength indicator in device-dependent units/scale.
        Values: [0-254], UINT8_MAX: invalid/unknown.
    """

    time_boot_ms: int = 0
    port: int = 0
    chan1_raw: int = 0
    chan2_raw: int = 0
    chan3_raw: int = 0
    chan4_raw: int = 0
    chan5_raw: int = 0
    chan6_raw: int = 0
    chan7_raw: int = 0
    chan8_raw: int = 0
    rssi: int = 0


class ServoOutputRaw(MavMessage):
    """The RAW values of the servo outputs. The standard PPM
    modulation is as follows: 1000 microseconds: 0%, 2000 microseconds: 100%.

    :param time_usec: Timestamp (UNIX Epoch time or time since system boot).
        The receiving end can infer timestamp format (since 1.1.1970 or since system boot)
        by checking for the magnitude of the number.
    :param port: Servo output port (set of 8 outputs = 1 port).
        Flight stacks running on Pixhawk should use: 0 = MAIN, 1 = AUX.
    :param servo1_raw: Servo output 1 value
    :param servo2_raw: Servo output 2 value
    :param servo3_raw: Servo output 3 value
    :param servo4_raw: Servo output 4 value
    :param servo5_raw: Servo output 5 value
    :param servo6_raw: Servo output 6 value
    :param servo7_raw: Servo output 7 value
    :param servo8_raw: Servo output 8 value
    :param servo9_raw: Servo output 9 value
    :param servo10_raw: Servo output 10 value
    :param servo11_raw: Servo output 11 value
    :param servo12_raw: Servo output 12 value
    :param servo13_raw: Servo output 13 value
    :param servo14_raw: Servo output 14 value
    :param servo15_raw: Servo output 15 value
    :param servo16_raw: Servo output 16 value
    """

    time_usec: int = 0
    servo1_raw: int = 0
    servo2_raw: int = 0
    servo3_raw: int = 0
    servo4_raw: int = 0
    servo5_raw: int = 0
    servo6_raw: int = 0
    servo7_raw: int = 0
    servo8_raw: int = 0
    servo9_raw: int = 0
    servo10_raw: int = 0
    servo11_raw: int = 0
    servo12_raw: int = 0
    servo13_raw: int = 0
    servo14_raw: int = 0
    servo15_raw: int = 0
    servo16_raw: int = 0


class RadioStatus(MavMessage):
    """Status generated by radio and injected into MAVLink stream.

    :param rssi: Local (message sender) received signal strength indication in device-dependent units/scale.
        Values: [0-254], UINT8_MAX: invalid/unknown.
    :param remrssi: Remote (message receiver) signal strength indication in device-dependent units/scale.
        Values: [0-254], UINT8_MAX: invalid/unknown.
    :param txbuf: Remaining free transmitter buffer space.
    :param noise: Local background noise level. These are device dependent RSSI values (scale as approx 2x dB on SiK radios).
        Values: [0-254], UINT8_MAX: invalid/unknown.
    :param remnoise: Remote background noise level. These are device dependent RSSI values (scale as approx 2x dB on SiK radios).
        Values: [0-254], UINT8_MAX: invalid/unknown.
    :param rxerrors: Count of radio packet receive errors (since boot).
    :param fixed: Count of error corrected radio packets (since boot).
    """

    rssi: int = 0
    remrssi: int = 0
    txbuf: int = 0
    noise: int = 0
    remnoise: int = 0
    rxerrors: int = 0
    fixed: int = 0


class MissionRequestInt(MavMessage):
    """Request the information of the mission item with the sequence number seq.
    The response of the system to this message should be a MISSION_ITEM_INT message.
    https://mavlink.io/en/services/mission.html
    """

    target_system: int = 0
    target_component: int = 0
    seq: int = 0
    mission_type: MavMissionType = MavMissionType.MAV_MISSION_TYPE_MISSION


class MissionACK(MavMessage):
    """Acknowledgment message during waypoint handling. The type field states
    if this message is a positive ack (type=0) or if an error happened (type=non-zero).
    """

    target_system: int = 0
    target_component: int = 0
    type: MavMissionResult = MavMissionResult.NOT_RECEIVED
    mission_type: MavMissionType = MavMissionType.MAV_MISSION_TYPE_MISSION


class MissionItemReached(MavMessage):
    """A certain mission item has been reached. The system will either hold this position (or circle on the orbit)
    or (if the autocontinue on the WP was set) continue to the next waypoint.
    """

    seq: int = 0
