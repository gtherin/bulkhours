import time


def advance_cm(px_obj, distance_cm=10.0, speed=50, cm_per_sec=20.0):
    """Move forward for an estimated distance in centimeters."""
    duration_s = max(float(distance_cm) / float(cm_per_sec), 0.0)
    px_obj.forward(speed)
    time.sleep(duration_s)
    px_obj.stop()


def turn_right_cm(px_obj, distance_cm=10.0, speed=40, cm_per_sec=20.0, steer_angle=25):
    """Drive a right arc for an estimated arc-length in centimeters."""
    px_obj.set_dir_servo_angle(abs(int(steer_angle)))
    advance_cm(px_obj, distance_cm=distance_cm, speed=speed, cm_per_sec=cm_per_sec)
    px_obj.set_dir_servo_angle(0)


def route_20_right10_10(px_obj, speed=50, cm_per_sec=20.0, turn_speed=40, steer_angle=25):
    """Advance 20 cm, turn right over 10 cm arc, then advance 10 cm."""
    advance_cm(px_obj, distance_cm=20.0, speed=speed, cm_per_sec=cm_per_sec)
    turn_right_cm(
        px_obj,
        distance_cm=10.0,
        speed=turn_speed,
        cm_per_sec=cm_per_sec,
        steer_angle=steer_angle,
    )
    advance_cm(px_obj, distance_cm=10.0, speed=speed, cm_per_sec=cm_per_sec)
