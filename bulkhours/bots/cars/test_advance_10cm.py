#!/usr/bin/env python3
import argparse
import time
from pathlib import Path

from picarx import Picarx as PiCarX

from movement import advance_cm, route_20_right10_10


def main():
    parser = argparse.ArgumentParser(description="Test PiCar-X movement patterns")
    parser.add_argument(
        "--mode",
        choices=["advance", "route"],
        default="advance",
        help="advance: straight distance; route: 20cm then right 10cm then 10cm",
    )
    parser.add_argument("--distance-cm", type=float, default=10.0, help="Target distance in cm")
    parser.add_argument("--speed", type=int, default=50, help="Forward speed")
    parser.add_argument("--cm-per-sec", type=float, default=20.0, help="Calibration constant")
    parser.add_argument("--turn-speed", type=int, default=40, help="Turning speed (route mode)")
    parser.add_argument("--steer-angle", type=int, default=25, help="Steering angle for right turn (route mode)")
    args = parser.parse_args()

    config_path = Path.home() / ".config" / "picar-x" / "picar-x.conf"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    px = PiCarX(config=str(config_path))
    time.sleep(0.2)

    try:
        if args.mode == "advance":
            advance_cm(px, distance_cm=args.distance_cm, speed=args.speed, cm_per_sec=args.cm_per_sec)
        else:
            route_20_right10_10(
                px,
                speed=args.speed,
                cm_per_sec=args.cm_per_sec,
                turn_speed=args.turn_speed,
                steer_angle=args.steer_angle,
            )
    finally:
        px.stop()

    if args.mode == "advance":
        print(
            "Done: requested %.2f cm at speed=%d with cm_per_sec=%.2f"
            % (args.distance_cm, args.speed, args.cm_per_sec)
        )
    else:
        print(
            "Done: route 20cm + right(10cm arc) + 10cm at speed=%d, turn_speed=%d, steer_angle=%d"
            % (args.speed, args.turn_speed, args.steer_angle)
        )


if __name__ == "__main__":
    main()
