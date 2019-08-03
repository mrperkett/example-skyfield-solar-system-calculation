#! /usr/bin/env python3
"""
Calculate all pairwise distances between the planets + the Sun + Pluto over a specified number
of years.
"""

import csv
import datetime
import logging
import os
import time

import numpy as np
import scipy.spatial
import skyfield.api


def calc_dist_matrices(celestial_objects, ts, start_date, num_days, time_delta_hours=1):
    """
    Calculate the pairwise distance matrix for celestial_objects beginning at start_date
    for num_days calculating every time_delta_hours.

    Args:
        celestial_objects: list of skyfield.jpllib.ChebyshevPosition loaded from bsp file
        ts (skyfield.timelib.Timescale): skyfield timescale
        start_date (datetime): start date/time
        num_days (float): calculate pairwise distances until this number of has been exceeded
        time_delta_hours (float): time step between calculating pairwise distances 

    Return:
        date_times: list of datetime objects corresponding to
        pdists (np.array): arrays of condensed distance matrices (one for each date_time)
    """
    # build a list of date times at which to calculate planetary body positions
    end_date = start_date + datetime.timedelta(days=num_days)
    date_times = [start_date,]
    t = start_date
    while t < end_date:
        # increment time
        t += datetime.timedelta(hours=time_delta_hours)
        date_times.append(t)

    # verify that there is data for all of date range
    try:
        celestial_objects[0].at(ts.utc(date_times[0])).position.km
    except Exception as e:
        raise ValueError("start_date (%s) is outside of allowed range: %s" % (start_date, str(e)))

    try:
        celestial_objects[0].at(ts.utc(date_times[-1])).position.km
    except Exception as e:
        raise ValueError("end_date (%s) is outside of allowed range: %s" % (end_date, str(e)))


    num_chunks = 10
    chunk_size = int(np.floor(len(date_times) / float(num_chunks)))

    pdists = []
    for n, date_time in enumerate(date_times):
        if n % chunk_size == 0:
            frac = n / float(len(date_times))
            logging.debug("\t\tstep %i of %i (%3.1f%%)" % (n, len(date_times), 100.0 * frac))

        # calculate the position of each object and all pairwise distances
        positions = [c.at(ts.utc(date_time)).position.km for c in celestial_objects]
        pdists.append(scipy.spatial.distance.pdist(positions))


    return date_times, np.array(pdists)


def main():
    """
    """
    out_dir = "output"

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # NOTE: these two loads will download the required data if it isn't already located 
    #       on your computer
    # NOTE: you can find other kernels available for download here:
    #           https://naif.jpl.nasa.gov/pub/naif/JUNO/kernels/spk/
    #           ftp://ssd.jpl.nasa.gov/pub/eph/planets/bsp/
    logging.info("Loading timescale and celestial objects...")
    ts = skyfield.api.load.timescale()
#    planets_spicekernel = skyfield.api.load('de438s.bsp')
    planets_spicekernel = skyfield.api.load('de438t.bsp')

    names = ["SUN",
             "MERCURY_BARYCENTER",
             "VENUS_BARYCENTER",
             "EARTH_BARYCENTER",
             "MARS_BARYCENTER",
             "JUPITER_BARYCENTER",
             "SATURN_BARYCENTER",
             "URANUS_BARYCENTER",
             "NEPTUNE_BARYCENTER",
             "PLUTO_BARYCENTER"]
    celestial_objects = [planets_spicekernel[name] for name in names]

    # Shortest orbit time (Mercury): 88 Earth days
    # Longest orbit time (Pluto):    248 Earth years
    # Time span covered by de438t.bsp: 1549-DEC-21 00:00 to   2650-JAN-25 00:00
    num_days = int(248 * 365 * 4)
    time_delta_hours = 24
    start_date = datetime.datetime( year=1550,
                                    month=1,
                                    day=1,
                                    hour=0,
                                    minute=0,
                                    second=0,
                                    tzinfo=datetime.timezone.utc)

    logging.info("Calculating pairwise distances...")
    logging.info("\tnum celestial objects: %i" % len(celestial_objects))
    logging.info("\tstart_date:            %s" % start_date)
    logging.info("\tnum_days:              %i" % num_days)
    logging.info("\ttime step (hours):     %f" % time_delta_hours)

    start_time = time.time()
    date_times, pdists = calc_dist_matrices(celestial_objects, ts, start_date, num_days, time_delta_hours)
    run_time = time.time() - start_time

    logging.info("\trun time: %.2f seconds" % run_time)

    logging.info("Calculating mean pairwise distances...")
    avg_pdist = np.mean(pdists, axis=0)

    logging.info("Writing results to file...")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    # averages
    out_fp = os.path.join(out_dir, "mean_pairwise_distances.csv")
    with open(out_fp, "w") as out_file:
        csvwriter = csv.writer(out_file)
        header = ["",] + names
        csvwriter.writerow(header)

        arr = scipy.spatial.distance.squareform(avg_pdist)
        for i, row_label in enumerate(names):
            row = [row_label,] + [arr[i,j] for j, col_label in enumerate(names)]
            csvwriter.writerow(row)

    # time series for each planet
    for i, name in enumerate(names):
        out_fp = os.path.join(out_dir, "pairwise_distances-%s.csv" % name)
        with open(out_fp, "w") as out_file:
            csvwriter = csv.writer(out_file)
            header = ["DateTime",] + ["%s (km)" % other_name for n, other_name in enumerate(names) if n != i]
            csvwriter.writerow(header)

            for date_time, pdist in zip(date_times, pdists):
                arr = scipy.spatial.distance.squareform(pdist)
                row = [date_time.strftime("%Y-%m-%d %H:%M:%S"),]
                row.extend([arr[i,j] for j in range(len(names)) if j != i])
                csvwriter.writerow(row)
                    
    logging.info("Done.")

    return


if __name__ == "__main__":
    main()
