
# coding: utf-8

# <font color='seagreen'>
# 
# # Week 9 + 10 -- Scattering in Atmospheres
# 
# *Please finish and submit this project before the start of class on 8 November 2017.*
# 

# <font color='seagreen'> 
# ### Q1: Landscape Painting with Radiative Transfer
# 
# For a scattering atmosphere, we can write the solution to the equation of radiative transfer as
# $$ I_\lambda(0, \phi, \theta) = I_\lambda(\tau_\lambda,\phi, \theta) e^{-{\tau_\lambda}} + \int^{\tau_\lambda}_{0} S_\lambda(\tau', \phi, \theta) e^{-\tau'}d\tau'$$
# where $I_\lambda(0, \phi, \theta)$ is the intensity I measure coming toward me from a direction parameterized by the angles $\phi$ and $\theta$. The variable $\tau_\lambda$ represents the optical depth to the most distant location we are considering in a given $\phi-\theta$ direction, and $I_\lambda(\tau_\lambda,\phi, \theta)$ is the intensity emerging towards us from that distant location. The source function $S_\lambda(\tau', \phi, \theta)$ respresents the new intensity added into the $\phi-\theta$ direction by each little segment along the line of sight. In class, we introduced a single-scattering albedo $\omega_\lambda$ to represent the fraction scattering contributes to the total extinction coefficient. Throughout this project we'll imagine we're standing on Earth, with $\tau'=0$ corresponding to our location as observers and $\tau'=\tau_\lambda$ corresponding to some distance away from us, perhaps all the way out of the atmosphere entirely.
# 
# 1. Derive an expression $I_\lambda(0, \phi, \theta)$ for a general value of $\omega_\lambda$ using the simplifying approximations of (a) an isothermal atmosphere at temperature $T$ where (b) all scattering is isotropic and (c) a mean intensity field $J_\lambda = \frac{1}{4\pi}\int I_\lambda d\Omega$ that is constant everywhere. This last assumption might be reasonable for parcels of gas illuminated by direct overhead sunlight (where scattering changes the total $J_\lambda$ by only a small fraction). Your expression  should no longer contain an integral, and it may make use of $\tau_\lambda$, $\omega_\lambda$, $J_\lambda$, $B_\lambda(T)$, and $I_\lambda(\tau_\lambda, \phi, \theta)$. 
# 
# 1. Let's look at the the terms to put into our expression. From here onward, we will applying these expressions to visible-light radiative transfer on Earth. Explain why we can safely ignore the $B_\lambda(T)$ term in the on-an-Earth-orbiting-the-Sun regime.
# 
# 1. Next, let's determine the intensity field $I_\lambda(\tau_\lambda, \phi, \theta)$ at our boundary conditions. Define the angle $\alpha$ to an angular distance away from the center of the Sun as seen on the sky. $\alpha=0$ is looking directly at the center of the Sun, $\alpha=\alpha_{\odot}$ is looking at the limb of the Sun, and $\alpha>\alpha_{\odot}$ is looking anywhere on the sky other than directly at the Sun (where neglecting starlight the incoming intensity drops to 0). Plot $I_\lambda(\tau_\lambda, \alpha)$, the specific intensity illuminating the top of the atmosphere, as a function of angular separation $\alpha$ away from the center of the disk of the Sun. For your plot, evaluate the intensity at a wavelength of $\lambda = 0.5~\mu m$ and remember that it should have units of $[W/m^2/\mu m/sr]$. You can assume the Sun is $1~R_\odot$, $1~AU$ away, and emits as Planck spectrum with $T=5780~K$. (In case Girish asks, let's ignore limb-darkening on the surface of the Sun.)
# 
# 1. Calculate the angle-averaged mean intensity $J_\lambda$ that would be associated with this intensity field coming from the Sun, also evaluated at $\lambda = 0.5~\mu m$. This should also have units of $[W/m^2/sr/\mu m]$. 
# 
# 1. Make a plot with $\tau_\lambda$ on a logarithmic horizontal axis, spanning at least $10^{-2} < \tau_\lambda < 10^2$. On the vertical, plot two curves: one for direct sunlight $I_\lambda(0, \alpha<\alpha_{\odot})$ and one for indirect illumination scattered from the daytime sky $I_\lambda(0, \alpha>\alpha_{\odot})$, again for $\lambda = 0.5~\mu m$. You can think of this plot as indicating the brightness we would see in each direction if we cranked the optical thickness of the atmosphere up or down. Assume the atmosphere is purely scattering at this wavelength $(\omega_{0.5~\mu m} = 1)$. Explain the qualitative behavior of these curves in the extreme optically thick and optically thin limits.
# 
# 1. The scattering cross section for Rayleigh scattering for Earth air is approximately
# $$\sigma_\lambda = 3.7 \times 10^{-32} \times \left(\frac{1~\mu m}{\lambda} \right)^4~m^2$$
# for a single molecule and for light with wavlength $\lambda$. Using this cross-section, plot the optical depth $\tau_\lambda$ vs distance $s$ for a wavelength of $\lambda = 0.5~\mu m$. For simplicity, you can take the number density of air molecules $n$ to be a constant value appropriate for a temperature of $273~K$ and Boulder's surface pressure of $P = 0.8~bar$. Again, assume $\omega_\lambda = 1$.
# 
# 1. If you go up to the top of the JILA tower and look out, you'll see to a different distance $s$ for each different direction you look in $\phi$ (azimuth) and $\theta$ (zenith angle). The file `distances.npy` contains a 2D array of these distances computed over a grid of $\phi$ (columns) and $\theta$ (rows). Using this array, make an image of the intensity $I_\lambda(0, \phi, \theta)$ we would observe from JILA for pure Rayleigh scattering off air molecules, evaluated at $\lambda = 0.5~\mu m$. For simplicity, you can assume $I_\lambda(\tau_\lambda, \phi, \theta) = 0$ everywhere: this amounts to saying that the ground has a low albedo and that there's no intensity coming towards us from directly behind the atmosphere. Make a second image where you increase the scattering cross section by a factor of $10\times$, for example if there were some very small aerosol particulates in the air.
# 
# 1. Now, imagine there's a snow storm in Boulder. Imagine there is so much snow in the air that we can't even see the Flatirons from the top of the JILA tower. If a typical snowflake is $1~mm$ in radius, roughly what minimum number density of snowflakes would be required in the atmosphere to achieve such white-out conditions? Make one or more images to demonstrate your point.

# In[ ]:

phi, theta, distance = np.load('distances.npy')


# <font color='seagreen'>
# 
# ### Q2: Randall Munroe is a punk.
# Answer [this question](https://xkcd.com/1145/) to your own satisfaction.
