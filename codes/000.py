import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy import units as u
 
hdul = fits.open('spec-0285-51930-0184.fits')

# First extension
# ===============
cols1 = hdul[1].columns
data1 = hdul[1].data
 
wavelength = 10 ** data1.field('loglam')
flux = data1.field('flux')
model = data1.field('model')

wavelength = wavelength * u.Unit('AA')
flux = flux * 10**-17 * u.Unit('erg cm-2 s-1 AA-1')
model = model * 10**-17 * u.Unit('erg cm-2 s-1 AA-1')

# Third extension
# ===============
cols3 = hdul[3].columns
data3 = hdul[3].data

line_names = data3.field('LINENAME')
line_waves = data3.field('LINEWAVE')
line_z = data3.field('LINEZ')
line_area = data3.field('LINEAREA')


df = pd.DataFrame(
    {'name': [i for i in line_names],
     'lam_rest': [i for i in line_waves],
     'z': [i for i in line_z],
     'area': [i for i in line_area]
     }
    )

df = df[abs(df['area'])>0]

df['lam_obs'] = df['lam_rest'] * (1 + df['z'])

# plotting
# =========
fig, ax = plt.subplots(figsize=(12,8))

label_y = np.random.uniform(model.min().value*1.1, model.max().value*0.9, len(df))

ax.plot(wavelength, model, linewidth=1)

for i in range(len(df)):
    ax.axvline(x=df['lam_obs'].iloc[i],
               color='r',
               alpha=0.3,
               label=df['name'].iloc[i],
               ls='--',
               lw=0.7)
    
    ax.text(x=df['lam_obs'].iloc[i] ,
            y=label_y[i],
            s=df['name'].iloc[i],
            fontsize='small',
            rotation=90)

plt.xlim(4000,8000)
plt.show()

hdul.close()
