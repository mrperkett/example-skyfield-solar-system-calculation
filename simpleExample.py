#! /usr/bin/env python3
"""
Demonstrate how to load required planet information and get the ICRS x, y, z coordinates for Earth
and Mars and specific times.
"""

import datetime

import skyfield.api


def main():
    """
    Usage: python3 ./simpleExample.py
    """
    # NOTE: these two loads will download the required data if it isn't already located on your computer
    ts = skyfield.api.load.timescale()
    planets = skyfield.api.load('de421.bsp')

    earth = planets['earth']
    mars = planets['mars']

    # where were the planets on January 1st, 2019
    dt = datetime.datetime(year=2019, month=1, day=1, hour=0, minute=0, second=0, tzinfo=datetime.timezone.utc)
    print("dt = {dt}".format(**locals()))
    print(earth.at(ts.utc(dt)).position.au)
    print(mars.at(ts.utc(dt)).position.au)

    # where were the planets and hour later?
    dt += datetime.timedelta(hours=1)
    print("dt = {dt}".format(**locals()))
    print(earth.at(ts.utc(dt)).position.au)
    print(mars.at(ts.utc(dt)).position.au)

    
    return


if __name__ == "__main__":
    main()
