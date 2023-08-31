import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import interpolate
import scipy.io
import radyn_xtools.globals as cnst
from astropy.io import fits
from astropy import units as u
import glob as glob
from astropy.table import Table, Column, MaskedColumn
from astropy.io import ascii
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import cdflib


# all call examples are within a Jupyter Notebook.

def findind(array,value):
    ''' closest_index = findind(array, value_of_interest);  finds index of array where array is closest to the given value.'''
    idx = (np.abs(array-value)).argmin()
    return idx


class modelclass:
    pass


def rcdf(fname, H_2 = False,dt_int=-99):
    ''' This automatically finds the largest time in the cdf even if it is 
not the last index.  
    dt_int = -99 reads in all entries in CDF
    dt_int = 0.2 reads in the _closest_ index at every 0.2s, which could have 
        a repeat among indices 

    call:   atmos_F11 = radyn_xtools.rcdf('radyn_out.cdf')
    '''
    run = cdflib.CDF(fname)
    timeS = np.array(run.varget("time"))
    tinds = np.linspace(0, len(timeS)-1, len(timeS), dtype='int')
    dtS = timeS[1:,] - timeS[0:-1]
    bad = np.all([dtS < 0], axis=0)
    nbad = np.count_nonzero(bad)
    if nbad > 0:
        tindS = tinds[1:,]
        badind = tindS[bad]
        tinds = tinds[0:badind[0]]
        timeS = timeS[tinds]

    if dt_int > 0:
        tsearch = np.arange(0.0, np.max(timeS), dt_int)
        tinds2 = []
        for i in range(len(tsearch)):
            found_ind = findind(timeS, tsearch[i])
            tinds2.append(found_ind)
    else:
        tinds2 = np.linspace(0, len(timeS)-1, len(timeS), dtype='int')

 #   radynvar = scipy.io.readsav(fname)  #+ 'radyn_sed.'+model_id+'.sav
    if dt_int < 0:
        print('Reading in all times from the CDF file ... ',fname)
    if dt_int > 0:
        print('Reading in select times from the CDF file ... ',fname)

    atmos = modelclass()
    test = run.varget("z1").transpose()
    atmos.z1t = test[:, tinds2]  # have to transpose all this stuff   atmos.z1t[ndep, ntime]

    test = run.varget("time")
    atmos.timet = test[tinds2]

    test = run.varget("vz1").transpose()
    atmos.vz1t = test[:,tinds2]

    test = run.varget("d1").transpose()
    atmos.d1t = test[:,tinds2]
    atmos.zmu = run.varget("zmu")
 #   try:
 #       test = run.varget("dz").transpose()
 #   except:
    ndep = len(atmos.z1t[:,0])
    atmos.dzt = np.zeros_like(atmos.z1t)
    atmos.dzt[1:ndep,:] = atmos.z1t[0:ndep-1,:]-atmos.z1t[1:ndep,:]

    test = run.varget("pg1").transpose()
    atmos.pg1t = test[:,tinds2]

    test= run.varget("ne1").transpose()
    atmos.ne1t = test[:,tinds2]

    test = run.varget("tau").transpose()
    atmos.taut = test[:,tinds2]

    test = run.varget("tg1").transpose()
    atmos.tg1t = test[:,tinds2]

    test =  run.varget("n1").transpose()
    atmos.n1t = test[:,:,:,tinds2]

    test = run.varget("totn").transpose()
    atmos.totnt = test[:,:,tinds2] #  run.varget("totn").transpose()
    
    try:
        test = run.varget("nstar").transpose() 
        atmos.nstart = test[:,:,:,tinds2]

    except:
        print('Could not read in LTE pops nstart.')

    try:
        test = run.varget("c").transpose()
        atmos.c1t =test[:,:,:,:,tinds2]  # collisional rates.

        test = run.varget("f20").transpose() 
        atmos.f20t = test[:,tinds2]
    except:
        print('Could not read in c1t or f20t')
    try:

        test = run.varget("rij").transpose() 
        atmos.rijt = test[:,:,tinds2] # radynvar.RIJT.transpose()
        test = run.varget("rji").transpose()
        atmos.rjit =test[:,:,tinds2] # radynvar.RJIT.transpose()
    except:
        print('Could not read in rjit, rijt.')

    test = run.varget("cmass1").transpose()
    atmos.cmass1t = test[:,tinds2]

    test = run.varget("bheat1").transpose()
    atmos.bheat1t = test[:,tinds2]
    atmos.cont = run.varget("cont")
    atmos.irad = run.varget("irad")
    atmos.jrad = run.varget("jrad")
    atmos.alamb = run.varget("alamb")
    atmos.ielrad = run.varget("ielrad")
    atmos.atomid = run.varget("atomid")
    atmos.label = run.varget("label")
    atmos.ion = run.varget("ion").transpose()
    atmos.g = run.varget("g").transpose()
    atmos.grph = run.varget("grph")

    if H_2:
        atmos.H_2 = (atmos.d1t / atmos.grph - atmos.totnt[:,0,:])*0.5 
        print('Read in H_2 population densities.')
    return atmos

def make_dataframe_atmos(timet, x1, y1):
    '''
   call:  df_F11 = radyn_xtools.make_dataframe_atmos(atmos_F11.timet, atmos_F11.z1t/1e5, np.log10(atmos_F11.tg1t))
    '''
    nt = len(timet)
    nx = len(x1[:,0])
    t1d = []
    typ1d = []
    x1d  = x1.transpose().flatten()
    y1d  = y1.transpose().flatten()
    for i in range(nt):
        for j in range(nx):
            t1d.append(timet[i])
            typ1d.append('flare')
    for i in range(nt):
        for j in range(nx):
            t1d.append(timet[i])
            typ1d.append('pre')
            x1d = np.append(x1d, x1[j,0])
            y1d = np.append(y1d, y1[j,0])

    d = {'time': t1d, 'x1': x1d, 'y1':y1d, 'typ':typ1d}
    datframe = pd.DataFrame(data=d)
    return datframe


def atmos_movie(df,xlim=(-100,500), ylim=(3000,2e4), save_movie=True,  ylabel='y-axis', xlabel = 'x-axis', movie_name="AtmosMovie.html"):
    '''
   call:  radyn_xtools.atmos_movie(df_F11, ylim=(3,7.5), save_movie=False, xlabel='Distance along loop from photosphere (km)', ylabel='Temperature (K)')
    '''
    fig = px.line(df, x="x1", y="y1",animation_frame="time",\
        color_discrete_sequence=px.colors.qualitative.Set1, \
                  range_x=xlim,range_y=ylim,markers=True,color="typ")
    fig.update_layout(yaxis=dict(title=ylabel), xaxis=dict(title=xlabel))

    fig["layout"].pop("updatemenus") # optional, drop animation buttons
    if save_movie:
        fig.write_html(movie_name)
        print('Saved ',movie_name)
    else:
        fig.show()
