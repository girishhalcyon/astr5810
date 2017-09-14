
# coding: utf-8

# <font color='seagreen'>
# 
# 
# # Week 3 -- Radiation Basics and Energy Balance
# *Please finish and submit this project before the start of class on 20 September 2017.*
# 
# This week, we will play with the Planck function and investigate how energy transport via radiation sets the basic temperature scale for planets' atmospheres.

# In[1]:

import matplotlib.pyplot as plt 
import numpy as np
from astropy import units, constants

plt.matplotlib.rcParams['figure.figsize'] = (10,7)
plt.matplotlib.rcParams['font.size'] = 12
get_ipython().magic('matplotlib inline')


# <font color='seagreen'>
# ### Q1: 
# 
# The Planck function expresses the *intensity* from a thermal emitting source. In terms of wavelength (in a form that can be integrated against $d\lambda$), it can be written as 
# 
# $$B_{\lambda}(\lambda, T) = \frac{{2hc}^2}{\lambda^5}\frac{1}{e^{hc/\lambda k_BT} - 1}$$
# 
# and has units that are equivalent to $J~{s}^{-1}~{m}^{-2}~{sr}^{-1}~{\mu m}^{-1}$. (Note that the  ${\mu m}^{-1}$ in refers to the width of the wavelength range $d\lambda$ -- something you'll see $m$, $nm$, $angstrom$, or other units instead.)
# 
# + Write a function that accepts an array of wavelengths and temperature, and returns the thermal emission *flux* $F_\lambda(\lambda, T)$ at those wavelengths and that temperature. Recall that because thermal emission is isotropic, the *flux* of radiation away from a surface, integrated over solid angle, is given by $F_{\lambda}(\lambda, T) = \pi B_\lambda(\lambda, T)$. 

# In[2]:

def planck_flux(wavelength, temperature):
    '''
    This function calculates the thermal emission spectrum of a surface.
    
        Inputs:
            wavelength = numpy array of wavelengths (in nm)
            temperature = a single number, the temperature (in K)
    
        Outputs:
            Returns an array of thermal emission fluxes,
            in units of J/(s*m^2*micron). This is a flux, which has 
            already been integrated over solid angle.
    '''
    
    # CALCULATE AN ARRAY FOR THE FLUX HERE
    return flux


# <font color='seagreen'>
# + Make a plot of $\lambda$ vs. $F_\lambda(\lambda, T=300~K)$, covering $1-100~\mu m$. Wien's Law states that the peak of this spectrum will be at $\lambda_{\rm max} = b/T$, with $b = 2900~\mu m~K$. To make sure you have your horizontal axis lined up appropriately, plot a vertical line at this predicted peak location.

# <font color='seagreen'>
# + The Stefan-Boltzmann Law states that the bolometric flux from a surface is
# $$F_{\rm bol}(T) = \int^{\infty}_{0}F_{\lambda}(\lambda, T)d\lambda = \sigma_{\rm SB}T^4$$
# in units of $W/m^2$. To make sure you have the units and overall scale of your Planck function correct, let's make sure we can recover this result. Numerically integrate your Planck function over wavelength, and compare it to the value from this analytic expression. (There are a couple of ways to do this numerical integral; `np.trapz` can integrate along a defined grid of $y$ and $x$, or `scipy.integrate` has tools for directly integrating a function between limits.)

# <font color='seagreen'>
# ### Q2: What color is a star?
# 
# When we look at a source whose spectrum is $F_\lambda(\lambda)$, our eyes are basically calculating three integrals of that spectrum over wavelength. We perceive different colors as different ratios among these three integrals. Let's write some code to approximate these integrals, so we can display spectra as colors on our computer screens. Flux integrals like these pop up [all the time](https://ui.adsabs.harvard.edu/#abs/2005ARA&A..43..293B/abstract) in astronomy, where we talk about flux through broadband photometric filters.
# 
# First, we need to know the effective response of the cones in our eyes to different wavelengths of light. We can approximate these using three "color matching functions" $\bar{x}(\lambda)$, $\bar{y}(\lambda)$, and $\bar{z}(\lambda)$.  The file `ciexyz31.txt` contains a table of these three functions. Load in these color matching functions, and use them to calculate the following three quantities:
# 
# $$X = \int F_{\lambda}(\lambda)~\bar{x}(\lambda)~d\lambda $$
# $$Y = \int F_{\lambda}(\lambda)~\bar{y}(\lambda)~d\lambda $$
# $$Z = \int F_{\lambda}(\lambda)~\bar{z}(\lambda)~d\lambda $$
# 
# These are integrals of the intrsinsic spectrum, weighted by the sensitivity of each "filter" to light at each wavelength. You can think of $X$, $Y$, and $Z$ roughly as the brightness of three colored lamps ("pseudo-red", "pseudo-green", "pseudo-blue") which all mix together to form the final color. However, these pseudo-colors aren't exactly the RGB ("red", "green", "blue") colors that our screens display. To get to actual RGB values, these need to be stretched and squeezed a little bit through a linear matrix transformation. The function `xyz2rgb` below handles this conversion for you. 
# 
# The final RGB color for a given spectrum should be an array of three numbers, all between 0 and 1. For example, an RGB array of `[0.0, 0.0, 1.0]` means "no brightness in R and G, and full brightness in B", so the color would appear blue. 
# 
# + Make a plot showing $\lambda$ vs. $F_{\lambda}(\lambda, T)$ for temperatures ranging from $3000~K$ to $10000~K$ in $1000~K$ increments. In your plot, set the color of each curve to the RGB color you calculate for that spectrum. 
# 
# + Discuss the overall features you see. Why are there no bright green stars?
# 
# We're going to use this code a few more times in this class!
# 

# In[3]:

def xyz2rgb(X, Y, Z):
    '''
    This function converts CIE XYZ values into CIE RGB values.
    '''

    # normalize these, so they're all between 0 and 1
    x = X/(X+Y+Z)
    y = Y/(X+Y+Z)
    z = Z/(X+Y+Z)

    # make a single column matrix containing the x,y,z values
    xyz = np.matrix([x,y,z]).T
    
    # rgb = conversion * xyz (with matrix math)
    conversion = np.matrix([[0.41847, -0.15866, -0.082835],
                            [-0.091169, 0.25243, 0.015708],
                            [0.00092090, -0.0025498, 0.17860]])
    
    # calculate the rgb single-column matrix
    color_matrix = conversion*xyz

    # 
    color = np.array(color_matrix.T)[0]
    color = color/np.max(color)
    
    return color


# <font color='seagreen'>
# ### Q3: Energy Balance
# 
# The average bolometric flux the Earth receives from the Sun (the "solar constant") is roughly $1360~W/m^2$. The Bond albedo of the Earth, averaged over the incoming solar spectrum, is about $A_B = 0.3$. 
# 
# + What is the total power $[W]$ absorbed by the Earth?
# + What is the total power $[W]$ Earth reflects away to space?
# + What is the equilibrium temperature $T_{eq, \oplus}$ of the Earth? Earth's atmosphere does a  good job of distributing incoming heat evenly across the planet, so you can assume the planet radiates with the same $T_{eq}$ at all latitudes and longitudes.
# + Make a plot of planetary equilibrium temperatures vs. planetary radius, including both the Solar System planets (`solarsystem.txt`) and most of the current confirmed extrasolar planets (`exoplanets.txt`). You can assume (wildly! boldly! inappropriately!) that all planets are in circular orbits and they efficiently redistribute their absorbed energy globally, and that the exoplanets have Bond albedos of $A_B=0.25$.

# <font color='seagreen'>
# 
# ### Q4: Cartoon Spectra of Planets
# 
# In Q3, we balanced the bolometric flux into and out of a planet. In this question, we will investigate the the wavelength-dependence of that light. Let's imagine we have fleets of satellites with spectrometers than can measure spectral flux [$W/m^2/\mu m$ or some related units] over a very broad wavelength range. We place these satllites in close orbits around each of the Solar System planets, and use them to measure the average spectral flux eminating from them. 
# 
# + Using the data in `solarsystem.txt`, make a plot of the pan-chromatic spectrum of each of the Solar System planets. These spectra should span $0.1-100\mu m$ in wavelength, and should reflect the average (over all angles) spectral flux we would measure for these planets. Be sure to include both reflected and emitted components of the spectrum. Treat the Sun and planets as simple thermal Planck emitters. When calculating the reflected light, make the (inappropriate) assumption that the albedo is constant across wavelength.
# + For each planet, indicate the approximate wavelength where the spectrum switches between being dominated by reflected light to being dominated by thermal emission from the planet itself.
# + Pick one exoplanet from the `exoplanets.txt` table, and make a cartoon spectrum for it. (Feel free to make up whatever albedo you want for the exoplanet.)

# <font color='seagreen'>
# 
# ### Q5: Glowing Humans
# 
# + Compute the total power (in $W$) radiated by a person with a normal body temperature of $37^\circ C$. For the purposes of this problem, you can approximate a human is a $1.5m \times 0.5m \times 0.25m$ rectangular prism.
# + Approximately how many photons/second does this human emit with wavelengths in the range $5-10 \mu m$ (the mid-infrared)? What about $0.5-1 \mu m$ (the visible/near-infrared)? 
# + Compute the total power (in W) input that a human would consume, if they on average ate $2000$ kilocalories per day.
# + Why is it OK that that humans radiate so much more power than they ingest through food? 
