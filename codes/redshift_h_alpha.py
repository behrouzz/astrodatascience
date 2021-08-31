"""
astrodatascience.net
"""
import sdss
import pandas as pd
from astropy.io import fits
from astropy import units as u
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

params = {'legend.fontsize': 'x-large',
          'figure.figsize': (12, 8),
          'axes.labelsize': 'x-large',
          'axes.titlesize':'x-large',
          'xtick.labelsize':'large',
          'ytick.labelsize':'large'}
pylab.rcParams.update(params)

sp = sdss.SpecObj(320932083365079040)
url = sp.spec_url()

hdul = fits.open(url)
data1 = hdul[1].data
data3 = hdul[3].data
hdul.close()

line_names = data3.field('LINENAME')
line_waves = data3.field('LINEWAVE')
line_z = data3.field('LINEZ')
line_area = data3.field('LINEAREA')
line_names = [i for i in line_names]
line_waves = [i for i in line_waves]
line_z = [i for i in line_z]
line_area = [i for i in line_area]

flux_m = data1.field('model')
flux_m = flux_m * 10**-17 * u.Unit('erg cm-2 s-1 AA-1')

wavelength = 10 ** data1.field('loglam')
wavelength = wavelength * u.Unit('AA')

df = pd.DataFrame({'name':line_names, 'lam_rest':line_waves, 'z':line_z, 'area':line_area})
df['abs_area'] = abs(df['area'])
df.loc[df['area']!=0, 'lam_obs'] = df['lam_rest'] * (1 + df['z'])

# index of H_alpha
i = df[df['name']=='H_alpha'].index[0]
line_name = df['name'].loc[i]
lam_obs = df['lam_obs'].loc[i]
lam_rest = df['lam_rest'].loc[i]
z = (lam_obs - lam_rest) / lam_rest

print('Name of the line    :', line_name)
print('Observed wavelength :', lam_obs)
print('Emitted wavelength  :', lam_rest)
print('Redshift            :', z)

fig, ax = plt.subplots()
ax.plot(wavelength, flux_m, linewidth=1)

# Observed
ax.axvline(x=lam_obs, color='r', alpha=0.7, label=line_name, ls='--', lw=0.7)
ax.text(lam_obs , flux_m.min().value, line_name+' (observed)', fontsize='large', rotation=90)

# Rest (emitted)
ax.axvline(x=lam_rest, color='b', alpha=0.7, label=line_name, ls='--', lw=0.7)
ax.text(lam_rest , flux_m.min().value, line_name+' (emitted)', fontsize='large', rotation=90)

plt.xlim(4000,8000)
plt.title('Redshift in H_alpha | astrodatascience.net')
ax.set_xlabel('Wavelength '+r'($A$)')
ax.set_ylabel('Flux '+r'($erg/cm^{2}/s/A$)')
plt.show()
