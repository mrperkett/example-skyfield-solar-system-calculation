
# Summary

An example using the [`skyfield`](https://github.com/skyfielders/python-skyfield/) module to calculate and plot each planet's distance from the Sun and from the Earth.  My calculation uses the `de438t.bsp` spicekernel, which covers a time span from 1549-DEC-21 to 2650-JAN-25.

My initial motivation for this calculation came from a web article titled [Venus is not Earth’s closest neighbor](https://physicstoday.scitation.org/do/10.1063/PT.6.3.20190312a/full/).  It makes a big deal about the difference between an *average* distance and a *closest approach* distance.  Although not as revolutionary of a concept as the article makes it out to be, it does provide a fun test of `skyfield`'s functionality.

![Distance from Sun](/images/plot-distances_from_sun.png)

![Distance from Earth](/images/plot-distances_from_earth.png)
It's interesting to note that Earth is closer to the Sun on average than any of the planets.

![Average Pairwise Distances](/images/plot-pairwise_distances_heatmap-closest.png)

# Setup

```
# install the appropriate version of Python for skyfield (requires Python 3.3–3.5)
pyenv install -v 3.5.7
pyenv local 3.5.7

# set up virtual environment with skyfield and scipy (using Pipfile)
pipenv install
```

At the time of writing, you get an error when attempting this with WSL, but the following works ([possibly related issue](https://github.com/pypa/pipenv/issues/3488)).

```
pipenv install --python=`which python3`
```

## (An alternative to pipenv)
```
# an alternative to using pipenv for the virtual environment
pyenv virtualenv 3.5.7 skyfield-env
pyenv local skyfield-env
python3 -m pip install skyfield
python3 -m pip install scipy
```

# Running

```
# activate virtual environment and run
pipenv shell
python3 calculateDistances.py
```

## Output

This script produces a summary file (`mean_pairwise_distances.csv`) containing the mean pairwise distances between each of the celestial objects.  It also produces a file for each celesital object giving it's distance to all other objects for each time point.

```
output/
  mean_pairwise_distances.csv
  pairwise_distances-EARTH_BARYCENTER.csv
  pairwise_distances-JUPITER_BARYCENTER.csv
  pairwise_distances-MARS_BARYCENTER.csv
  pairwise_distances-MERCURY_BARYCENTER.csv
  pairwise_distances-NEPTUNE_BARYCENTER.csv
  pairwise_distances-PLUTO_BARYCENTER.csv
  pairwise_distances-SATURN_BARYCENTER.csv
  pairwise_distances-SUN.csv
  pairwise_distances-URANUS_BARYCENTER.csv
  pairwise_distances-VENUS_BARYCENTER.csv
```

`example_output.tgz` contains example data for a very short run (so the average distances have not yet converged to their long time average).

# Plotting

Plots are generated using Jupyter notebook (`plot_distances.ipynb`) with Python3.  An export of the notebook is given by `plot_distances.html` and the resulting plots are provided in the `images/` folder.

# Useful Links

* FTP to directly download .bsp files
  * ftp://ssd.jpl.nasa.gov/pub/eph/planets/bsp/
* Web downloads for .bsp files (doesn't have downloads for the longer timescales?)
  * https://naif.jpl.nasa.gov/pub/naif/JUNO/kernels/spk/
* GitHub page with utilities to manipulate JPL DE ephemeris data.  Links to other pages with information I found useful to skim.
  * https://github.com/Bill-Gray/jpl_eph
