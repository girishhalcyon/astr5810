
# coding: utf-8

# <font color='seagreen'>
# 
# 
# # Week 2 -- Vertical Structure of an Atmosphere
# *Please finish and submit this project before the start of class on 13 September 2017.*
# 
# This week, we will play with the vertical structure of atmospheres, from both theoretical and observational perspectives. We'll also introduce some of the useful tools (like unit conversions!) included in the community-developed [astropy](http://docs.astropy.org/en/stable/index.html) Python library.

# In[ ]:

# gain access to numerical tools
import numpy as np

# gain access to plotting tools 
import matplotlib.pyplot as plt 

# set up bigger default plots
plt.matplotlib.rcParams['figure.figsize'] = (10,7)
plt.matplotlib.rcParams['font.size'] = 12

# make plots show up in the notebook
get_ipython().magic('matplotlib inline')


# <font color='seagreen'>
# 
# ### Q1: Atmospheric Scale Heights
# 
# Calculate the scale height of Jupiter's atmosphere, assuming a temperature of 130K, a composition of 85% molecular hydrogen and 15% helium. Use the [`constants`](http://docs.astropy.org/en/stable/constants/index.html) and [`units`](http://docs.astropy.org/en/stable/units/index.html) packages from the community [`astropy`](http://docs.astropy.org/en/stable/index.html) Python library to access the physical constants you need and to handle your unit conversions. *Hint: Jupiter is 1.0 Jupiter radii, and 1.0 Jupiter masses.*

# In[ ]:

# import the constants and units packages from astropy
from astropy import constants, units

# this gives us access to useful constants and units
print(constants.k_B)


# In[ ]:

# define some variables, with units!
temperature = 130*units.K
k_B = constants.k_B
kT = k_B*temperature

# see some examples of units in action
print('''
Example of astropy units:

    The temperature is {}.
    Boltzmann's constant is {}.
    The product of these two is {:.2g}.
      In cgs, it would be {:.2g}.
      In electron volts, it would be {:.2g}.
'''.format(temperature, k_B, kT, kT.to('erg'), kT.to('eV'))
     )


# In[ ]:




# <font color='seagreen'>
# ### Q2: Vertical Profiles of Solar System Planets
# 
# The plain-text data tables located in `verticalprofiles/` contain values for $P$, $T$, $\rho$, and $z$ along vertical traces through the atmospheres of Venus, Earth, Mars, Jupiter, and Titan. Look at the format of those files and check out the `README`. Then, please do the following steps ***for every vertical profile***.
# 
# + Read in the table so that you have access to $P$, $T$, $\rho$, $z$ as arrays in Python.
# + Make a multipanel plot where pressure is the vertical coordinate on every panel, and the scale of the vertical axis is logarithmic. On the horizontal axes, please plot the following quantities (if they are not in the table, you will need to calculate them from the variables you do have).
# 
#     1. altitude 
#     2. temperature
#     3. density
#     4. the lapse rate $dT/dz$
#     5. the rate of change of pressure $dP/dz$
#     6. the mean molecular weight
#     
#     
# + Calculate the dry adiabatic lapse rate. Based on these calculations, at what altitudes/pressures do expect convection is occuring? 
# + Discuss (at least) one interesting feature you see in each atmospheres. 
# 
# *The next five cells give you a few tips to get started.*

# In[ ]:

# For reading tables, I like the flexibility of astropy's table tools, ...
from astropy.io import ascii
table = ascii.read('verticalprofiles/earth.txt')
p = table['pressure']
T = table['temperature']
rho = table['density']
z = table['altitude']


# In[ ]:

# ...although some people prefer to read tables with genfromtxt.
p, T, rho, z = np.genfromtxt('verticalprofiles/earth.txt', skip_header=1, delimiter='|').T


# In[ ]:

# For making multipanel plots, you can...
# ...create a grid of "axes" objects into which you will place your plot
fi, ax = plt.subplots(1,6,sharey=True, figsize=(12,4))

# set current axis to the first of those
plt.sca(ax[0])
plt.plot([1,2,3], marker='.', markersize=20)

# set current axis to the fourth of those
plt.sca(ax[3])
plt.plot([1,5,2], marker='.', markersize=20)


# In[ ]:

# If you have to do the same thing over again with different inputs,
# defining a function might be a helpful trick!

def shout(x):
    print('{} is awesome!'.format(x))
    
shout('Cecelia Payne-Gaposkin')
shout('Galileo Galilei')
shout('Katherine Johnson')


# In[ ]:

# For calculating lapse rates, it may come in handy to use 
# the two modules that have been included alongside this notebook.
import phys, planets

print("")
print("The specific heat at constant pressure for CO2 is {} J/(kg K).".format(phys.CO2.cp))
print("The surface gravity of Titan is {} m/s**2. ".format(planets.Titan.g))


# In[ ]:




# <font color='seagreen'>
# 
# ### Q3: Above the Surface
# + Analytically integrate the equation of hydrostatic equilibrium to derive an expression for the pressure, $p(z)$, as a function of altitude, $z$, in an atmosphere with a linearly decreasing temperature profile with altitude, such that $T(z)=T_{0}-mz$, where $m = dT/dz$ is the slope and $T_{0}$ is the “surface” temperature.  Assume gravity is constant over the altitudes you are considering. 
# + Using the above data for the tropospheres of Venus and Earth (pressures below about $0.1~bar$), compare how well you approximate the actual $p(z)$ using both (a) the assumption of an isothermal atmosphere and (b) your new expression for $p(z)$ along an adiabat. *Hint: to compare how well models work, it can help to make a plot of your data and your model(s). By how much does each model diverge from the data?*

# <font color='seagreen'>
# 
# ### Q4: Below the Surface
# + Analytically integrate the equation of hydrostatic equilibrium to derive an expression for the pressure at the center of a planet with radius $R$ and mass $M$. Assume the density is constant with depth and ignore any contributions from an atmosphere. Recall that for a spherical object $g(R)$, the acceleration due to gravity at a radius $R$, can be written as
# $$ g(R) = \frac{GM(R)}{R^2} $$
# where $M(R)$ is the total mass enclosed within the radius $R$. 
# + Based on your expression, what is the pressure at the center of the Earth?
# 
