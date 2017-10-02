
# coding: utf-8

# <font color='seagreen'>
# 
# 
# # Week 5 -- Real Gas Radiative Transfer
# 
# *Please finish and submit this project before the start of class on 4 October 2017.*
# 
# This week we will build on the radiative transfer tools and expertise you developed last week, applying them to real gas and real opacities. It's through tools like these that we can connect remote sensing observations to the physics and chemistry of distant planets. I'd like you to see what some of the core steps would be!

# In[ ]:

import matplotlib.pyplot as plt, numpy as np
import astropy.units as u, astropy.constants as c


# <font color='seagreen'>
# ### Q1: HITRAN
# 
# The [HITRAN database](http://hitran.org) compiles line lists for common molecules, and is a very useful resource for thinking about spectroscopy and remote sensing of planetary atmospheres. The [HITRAN Application Programming Interface](http://hitran.org/hapi/) provides handy tools for accessing this database through Python.

# In[ ]:

# import tools for interacting with HITRAN
import hapi


# <font color='seagreen'>
# I've written a few cells to get you started here. If you have more questions on what's going on with `hapi`, check out the [hapi manual](http://hitran.org/static/hapi/hapi_manual.pdf) or the `hapi.getHelp()` built-in documentation. The standard `jupyter` tricks of `hapi.<tab>` or `hapi.fetch?` work, as usual, for investigating individual functions.

# <font color='seagreen'>
# ***Set up a local database.*** To use HITRAN data, you need to start a HITRAN database running on your computer. In effect, this is really just a folder where `hapi` will download and store data. 

# In[ ]:

# hapi will download data to your computer; this sets up a directory for it
hapi.db_begin('hitran_data')


# <font color='seagreen'>
# ***See what molecules are available.*** HITRAN has data on only so many molecules. They are indexed according to a molecule number `M`. This code lists the molecules stored in their database:

# In[ ]:

print("  M | molecule\n  ------------")
for M in np.arange(1,48):
    try:
        print('{:3} | {}'.format(M, hapi.moleculeName(M)))
    except KeyError:
        print('{:3} | (not found)'.format(M))


# <font color='seagreen'>
# ***Download some data.***
# To access HITRAN's line data for $CO_2$, we can use the `fetch` command. This will download two files (`CO2.data` and `CO2.header`) into your database directory; for the $CO_2$ lines between $1-100 \mu m$, the `CO2.data` file should be about 26MB in size.

# In[ ]:

print("Let's download some data for CO2.")

# give a name to this table you're downloading (you can set it to anything!)
nameoftable = 'CO2' 

# this integer refers to the molecule number in the HITRAN database
molecule = 2 

# which isotopologue to download (1 = the most abundant on Earth)
isotopologue = 1 

 # the minimum wavenumber to include
wavenumber_min = 1/(100*u.micron).to('cm').value

# the maximum wavenumber to include
wavenumber_max = 1/(1*u.micron).to('cm').value 

# download the data to a folder on your computer
hapi.fetch(nameoftable, molecule, isotopologue, wavenumber_min, wavenumber_max) 


# <font color='seagreen'>
# ***Calculate absorption coefficients.*** The data you downloaded was really just a list of $CO_2$ line strengths, line centers, line shape parameters at standard temperature and pressure ($T = 296~K$ and $P = 1~atm = 1.01325~bar$). The nitty gritty details of what you downloaded are listed [here.](http://hitran.org/docs/definitions-and-units/); the table contains enough information to estimate the line strengths and profiles at a range of temperatures and pressures. `hapi` provides handy functions to calculate absorption coefficients from these line data, effectively adding together a bunch of Voigt profiles.

# In[ ]:

# include molecule = 2, isotopologue = 1
moleculestoinclude = [(2,1)] 

# what table should the data come from?
tabletouse = 'CO2'

# what range of wavenumbers to consider?
wavenumber_min = 1/(100*u.micron).to('cm').value
wavenumber_max = 1/(1*u.micron).to('cm').value 
minmax_wn = [wavenumber_min, wavenumber_max]

# what wavenumber spacing should be used?
step_wn = 0.01

# calculate an array of absorption coefficients
wavenumber, crosssection = hapi.absorptionCoefficient(Components=moleculestoinclude, 
                                                      SourceTables=tabletouse,
                                                      WavenumberRange=minmax_wn,
                                                      WavenumberStep=step_wn)


# <font color='seagreen'>
# ***Plot the absorption coefficients.*** Let's plot these absorption coefficients, on both a linear and logarithm scale (because there's interesting stuff to see on both).

# In[ ]:

# this "magic command" makes plots interactive in jupyter, so you can zoom
get_ipython().magic('matplotlib notebook')
# Watch out! -- If you use this for interactive plotting,
# you'll need to explicitly create a new figure for each
# plot you make, either with `plt.figure()` or with 
# the `plt.subplots()` command seen here.

# create a multipanel plot
fi, ax = plt.subplots(2,1, sharex=True)

# make a linear scale plot on the top
plt.sca(ax[0])
plt.plot(wavenumber, crosssection)
plt.ylabel('Cross-Section (cm$^2$)')
plt.title('$CO_2$ at (T,p) = (296 K,p=1 atm)')

# make a log scale plot on the bottom
plt.sca(ax[1])
plt.plot(wavenumber, crosssection)
plt.yscale('log')
plt.xlabel('Wavenumber (1/cm)')
plt.ylabel('Cross-Section (cm$^2$)')

# (on the interactive plot, 
#      the square allow you to select a region to zoom to
#      the house resets the zoom settings
#      the floppy disk allows you to save the plot to a file


# <font color='seagreen'>
# ***Now, let's do some science!*** With the ingredients you've seen so far, we can now put together a slightly more realistic model of radiation through a planet's atmosphere. 
# 
# 1. Remake the above plot of the absorption cross-section $\sigma_\lambda$ as function of wavelength $\lambda$ (in $[\mu m]$). 
# + Make a plot of the mass opacity $\kappa_\lambda$ vs. $\lambda$. Please note that the absorption coefficient HITRAN returns is a cross-section in $[cm^2/molecule]$, not the mass opacity $[m^2/kg]$ we've been using in our radiative transfer code. 
# + Plot the pressure where $\tau_\lambda = 1$ (as a function of $\lambda$), given a pure $CO_2$ atmosphere with the absorption coefficients you've estimated. Assume a surface gravity of $10~m/s^2$. Plot $P$ on the vertical axis, with lower pressures at the top. 
# + Now, let's imagine this planet has a vaguely Earth-like equilibrium temperature of $T_{\rm eq} = T_{\rm eff} = 250K$. Construct a $T-P$ profile based on the cartoon we discussed in class, where the temperature is constant at $T_{\rm skin}$ at altitudes above some radiative-convective boundary $P_{\rm rc}$ and the *potential* temperature is constant for altitudes below this boundary. Assume $P_{\rm rc} = 0.1~bar$, and that $\gamma = c_{\rm p}/c_{\rm v} = 1.3$. Plot this $T-P$ profile, for altitudes spanning $P = 10^{-8}-10^{2}~bar$.
# + Make a prediction and write it down (it's OK if it's wrong!). If you were to calculate the radiative transfer through this atmosphere (keeping the $T-P$ profile fixed), roughly what brightness temperature would you expect to see at $15~\mu m$, at $20~\mu m$, and at $25~\mu m$? Assume the surface pressure is $100~bar$.
# + Test your predictions. Use your radiative transfer code from Week 04 to calculate the thermal emission spectrum for this planet, assuming a surface pressure of $100~bar$. Plot this spectrum, along with Planck $B_\lambda(T)$ intensity spectra for the skin temperature $T_{\rm skin}$ and the surface temperature $T_{\rm surf}$, on a log-log scale. I *very* strongly recommend not doing this at the full resolution of your arrays (990001 wavelengths); make a crude approximation and only calculate outgoing intensities at a tiny subset of these (maybe 100-1000 wavelengths). How did your $(15, 20, 25)~\mu m$ predictions fare?
# + Pick any other molecule out of the HITRAN list, download its line list, and make a plot comparing its absorption cross section to that of $CO_2$. Would your molecule be a stronger or weaker greenhouse gas (molecule-to-molecule) than $CO_2$ (for temperature equilbrium temperatures around $250~K$)?
# 

# <font color='seagreen'>
# ### Q2: Pressure and Temperature
# 
# We cheated a little bit in our previous example. We assumed $\kappa_\lambda$ was constant everywhere in the atmosphere. In practice, $\kappa_\lambda$ varies with $P$ and $T$. Zoom in around the $15~\mu m$ ro-vibrational band of $CO_2$, and investigate:
# + How do the line shapes vary as you increase the pressure (for instance, between $1-2~atm$)? Explain why, qualitatively.
# + How do the relative strengths of lines change as you increase the temperature (for instance, between $300-400~K$? Explain why, qualitatively.
# 
# The following code example shows how to change the $P$ and $T$ at which the absorption coefficients are calculated.

# In[ ]:

# include molecule = 2, isotopologue = 1
moleculestoinclude = [(2,1)] 

# what table should the data come from?
tabletouse = 'CO2'

# what range of wavenumbers to consider?
wavenumber_min = 1/(17*u.micron).to('cm').value
wavenumber_max = 1/(13*u.micron).to('cm').value 
minmax_wn = [wavenumber_min, wavenumber_max]

# the "environment" sets the pressure (in atmospheres) and temperature (in K)
env = {'p':1.0, 'T':1000}

# calculate an array of absorption coefficients
wavenumber, crosssection = hapi.absorptionCoefficient(Components=moleculestoinclude, 
                                                      SourceTables=tabletouse,
                                                      WavenumberRange=minmax_wn,
                                                      Environment=env)

