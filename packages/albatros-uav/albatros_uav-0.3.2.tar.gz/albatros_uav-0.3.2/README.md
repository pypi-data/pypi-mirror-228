# Albatros UAV

A python library that provides high-level functions for UAVs based on MAVLink. It allows to easily handle communication with the flight controller to create friendly mission management systems. Albatross supports direct communication with UAVs as well as via Redis (WIP)

### Supported functionalities

*General:*

- `wait_gps_fix`
- `is_armed`
- `wait_heartbeat`
- `arm`
- `disarm`
- `set_mode`
- `set_servo`
- `flight_to_gps_position`

*Mission Protocol:*

- `send_mission_count`
- `wait_mission_request_int`
- `get_mission_ack`
- `send_mission_takeoff_item`
- `send_mission_waypoint_item`
- `send_mission_loiter_unlim_item`
- `send_mission_loiter_time_item`
- `send_mission_rtl_item`
- `wait_mission_item_reached`

### Supported MAVLink telemetry messages

- `Attitude`
- `GlobalPositionInt`
- `GPSRawInt`
- `GPSStatus`
- `Heartbeat`
- `MissionACK`
- `MissionRequestInt`
- `RadioStatus`
- `RcChannelsRaw`
- `ServoOutputRaw`
- `SysStatus`
- `MissionItemReached`

## Examples

### Creating connection
```python
from albatros.uav import UAV
from albatros.telemetry import ConnectionType

# SITL connection is default
vehicle = UAV() 

# Direct connection to the flight controller
vehicle = UAV(device="/dev/tty/USB0/", baud_rate=57600)

# You can also specify the ID of the vehicle you want to connect to and the ID of your system
# read more about MAVLink Routing in ArduPilot: https://ardupilot.org/dev/docs/mavlink-routing-in-ardupilot.html
vehicle = UAV(vehicle_system_id=1, vehicle_component_id=1, my_sys_id=1, my_cmp_id=191)

```

### Arming vehicle (in SITL simulation)

Simply arm and disarm vehicle

Flow:
arm vehicle
wait for the vehicle to be armed
disarm vehicle

```bash
$ python -m examples.arming_vehicle
```

```python
from albatros.uav import UAV

vehicle = UAV()

while not vehicle.arm():
    print("waiting ARM")

vehicle.disarm()
```

### Takeoff (Plane)

Flow:
arm plane
wait for the vehicle to be armed
set mode TAKEOFF
print plane altitude

```bash
$ python -m examples.takeoff
```

```python
from time import sleep

from albatros.enums import PlaneFlightModes
from albatros.uav import UAV

plane = UAV()

while not plane.arm():
    print("waiting ARM")

plane.set_mode(PlaneFlightModes.TAKEOFF)

while True:
    print(f"Altitude: {plane.telem.data.global_position_int.relative_alt / 1000.0} m")
    sleep(1)

```

### Fly to point (Plane)

Example of flying plane to the designated point in GUIDED mode.

Flow:
wait GPS fix
arm plane
wait for the plane to be armed
set mode TAKEOFF
wait until the aircraft reaches 30 m AGL
set mode GUIDED
specify the point to which the plane will fly
print distance to point

```bash
$ python -m examples.fly_to_point
```

```python
from time import sleep

from albatros.enums import PlaneFlightModes
from albatros.nav.position import PositionGPS, distance_between_points
from albatros.uav import UAV

plane = UAV()

plane.wait_gps_fix()

while not plane.arm():
    print("waiting ARM")


plane.set_mode(PlaneFlightModes.TAKEOFF)

while plane.telem.data.global_position_int.relative_alt < 30_000:
    print(f"Altitude: {plane.telem.data.global_position_int.relative_alt / 1000.0} m")
    sleep(1)


# because mavlink sends coordinates in scaled form as integers
# we use function which scales WGS84 coordinates by 7 decimal places (degE7)
target = PositionGPS.from_float_position(lat=-35.35674492, lon=149.16324842, alt=50)


plane.set_mode(PlaneFlightModes.GUIDED)
plane.flight_to_gps_position(target.lat, target.lon, target.alt)

while True:
    current_position = PositionGPS(
        lat=plane.telem.data.global_position_int.lat,
        lon=plane.telem.data.global_position_int.lon,
        alt=50,
    )

    dist = distance_between_points(current_position, target)

    print(f"Distance to target: {dist} m")
    sleep(1)
```