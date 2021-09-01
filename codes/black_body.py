"""
astrodatascience.net
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

params = {'legend.fontsize': 'x-large',
          'figure.figsize': (10, 7),
          'axes.labelsize': 'x-large',
          'axes.titlesize':'x-large',
          'xtick.labelsize':'large',
          'ytick.labelsize':'large'}
pylab.rcParams.update(params)


# Constants in SI
k = 1.380649e-23
e = 2.718281828459045
h = 6.62607015e-34
c = 299792458

def B(lam, T):
    numerator = 2*h*(c**2)
    denominator = (lam**5)*((e**((h*c)/(lam*k*T)))-1)
    return numerator / denominator

# Wavelength in Angstrom
lam_ang = np.linspace(100, 20000, 1000)

# Convert wavelength to meter
lam = lam_ang / (10**10)

# Spectral radiance of 3 bodies
b1 = B(lam=lam, T=3000)
b2 = B(lam=lam, T=4000)
b3 = B(lam=lam, T=5000)

fig, ax = plt.subplots()

ax.plot(lam_ang, b1, c='r', label='T=3000')
ax.plot(lam_ang, b2, c='g', label='T=4000')
ax.plot(lam_ang, b3, c='b', label='T=5000')

plt.title('Black Body Radiation | astrodatascience.net')
plt.xlabel('Wavelength (Angstrom)')
plt.ylabel('Spectral density '+r'$W / (m^{3} sr)$')
plt.legend()
plt.grid()
plt.show()
