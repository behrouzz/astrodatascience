import numpy as np
import pandas as pd
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

# close the FITS file
hdul.close()


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
from bokeh.plotting import figure, show
from bokeh.models.tools import HoverTool
from bokeh.models import Span, Label

label_y = np.random.uniform(
    low=model.min().value*1.1,
    high=model.max().value*0.9,
    size=len(df)
    )

p = figure(title="Spectrum",
           sizing_mode="stretch_width",
           x_range=(4000, 8000),
           tools=[HoverTool(), 'pan', 'wheel_zoom', 'reset'],
           tooltips="lambda=@x{0.000} | flux=@y",
           x_axis_label="Wavelength", y_axis_label="Flux")

p.line(wavelength, model, line_color="blue", line_width=1)

for i in range(len(df)):
    ver = Span(location=df['lam_obs'].iloc[i],
               dimension='height',
               line_color='red',
               line_dash='dashed',
               line_width=1)
    
    p.add_layout(ver)
    
    lbl = Label(x=df['lam_obs'].iloc[i],
                y=label_y[i],
                text=df['name'].iloc[i])
    
    p.add_layout(lbl)
    
show(p)
