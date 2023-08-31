#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import interpolate
import scipy.io
import radyn_xtools.globals as cnst
#import globals as cnst
from astropy.io import fits
from astropy import units as u
import glob as glob
from astropy.table import Table, Column, MaskedColumn
from astropy.io import ascii
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import cdflib
import matplotlib.font_manager as font_manager
import matplotlib as mpl


# all call examples are within a Jupyter Notebook.

def prep_pmesh(z):
    # z is an irregular grid and must be at cell boundaries for pcolormesh (therefore make an array that is ndep + 1 dimensions.)
    ndep = len(z)
    midz = (z[1:len(z)] + z[0:len(z)-1])/2.
    newz = np.insert(midz, 0, z[0] + (z[0]-midz[0]))
    ndep2=len(newz)
    z_bdry = np.append(newz, z[ndep-1] + (z[ndep-1]-midz[ndep-2]))
    return z_bdry

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

def make_dataframe(timet, x1, y1):
    '''
   call:  df_F11 = radyn_xtools.make_dataframe(atmos_F11.timet, atmos_F11.z1t/1e5, np.log10(atmos_F11.tg1t))
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


def make_movie(df,xlim=(-100,500), ylim=(3000,2e4), save_movie=True,  ylabel='y-axis', xlabel = 'x-axis', movie_name="AtmosMovie.html"):
    '''
   call:  radyn_xtools.make_movie(df_F11, ylim=(3,7.5), save_movie=False, xlabel='Distance along loop from photosphere (km)', ylabel='Temperature (K)')
    '''
    fig = px.line(df, x="x1", y="y1",animation_frame="time",\
        color_discrete_sequence=px.colors.qualitative.Set1, \
                  range_x=xlim,range_y=ylim,markers=True,color="typ")
    fig.update_layout(yaxis=dict(title=ylabel), xaxis=dict(title=xlabel))
    fig.update_layout(width=800,height=600)
    fig["layout"].pop("updatemenus") # optional, drop animation buttons
    if save_movie:
        fig.write_html(movie_name)
        print('Saved ',movie_name)
    else:
        fig.show()





def load_atmos(model_id = 'mF13-85', model_dir='./', H_2 = False, load_by_id=True):
    # this was load_atmos in radx_dm
    if load_by_id:
        fname = glob.glob(model_dir+'radyn_out*'+model_id+'*.idl')
        if len(fname) > 1:
            print('Found more than 1 file with that ID!')
            return None
        radynvar = scipy.io.readsav(fname[0])  #+ 'radyn_sed.'+model_id+'.sav
        print('Read in ... ',fname[0])
    else:
        radynvar = scipy.io.readsav(model_id)
        print('Read in ... ',model_id)

    atmos = modelclass()
    atmos.z1t = radynvar.z1t.transpose()  # have to transpose all this stuff because scipy.io.readsav transposes.   atmos.z1t[ndep, ntime]
    atmos.timet = radynvar.timet
    atmos.vz1t = radynvar.vz1t.transpose()
    atmos.d1t = radynvar.d1t.transpose()
    atmos.zmu = radynvar.zmu
    atmos.dzt = radynvar.dzt.transpose()
    atmos.pg1t = radynvar.pg1t.transpose()
    atmos.ne1t = radynvar.NE1T.transpose()
    atmos.taut = radynvar.taut.transpose()
    atmos.z1t = radynvar.Z1T.transpose()
    atmos.tg1t = radynvar.TG1T.transpose()
    atmos.n1t = radynvar.N1T.transpose()
    atmos.totnt = radynvar.TOTNT.transpose()
    try:
        atmos.nstart = radynvar.NSTART.transpose()
        atmos.c1t = radynvar.CT.transpose()  # collisional rates.
        atmos.f20t = radynvar.F20T.transpose()
    except:
        print('Could not read in nstart, c1t.')
    try:
        atmos.rijt = radynvar.RIJT.transpose()
        atmos.rjit = radynvar.RJIT.transpose()
    except:
        print('Could not read in rjit, rijt.')
    atmos.cmass1t = radynvar.CMASS1T.transpose() 
    atmos.bheat1t = radynvar.bheat1t.transpose()
    atmos.cont = radynvar.cont
    atmos.irad = radynvar.irad
    atmos.jrad = radynvar.jrad
    atmos.alamb = radynvar.alamb
    atmos.ielrad = radynvar.ielrad
    atmos.atomid = radynvar.atomid
    atmos.label = radynvar.label
    atmos.ion = radynvar.ion.transpose()
    atmos.g = radynvar.g.transpose()
    atmos.grph = radynvar.GRPH
    if H_2:
        atmos.H_2 = (atmos.d1t / atmos.grph - atmos.totnt[:,0,:])*0.5 # if H_2 populations were included in LTE chemical equilibrium in radyn (m dwarf only)
        print('Read in H_2 population densities.')
    #isel = np.all([irad == 2],axis=0)
    #jsel = np.all([jrad == 2],axis=0)
    return atmos



def vactoair(wave_vac):
    sigma2 = (1e4/(wave_vac) )**2   
    fact = 1.0 +  5.792105E-2/(238.0185E0 - sigma2) + 1.67917E-3/( 57.362E0 - sigma2)
    wave_air = wave_vac/fact
    return wave_air

def airtovac(wave_air):
    # taken from IDL vactoair and airtovac.pro.
    sigma2 = (1e4/(wave_air) )**2
    fact = 1E0 +  5.792105E-2/(238.0185E0 - sigma2) + 1.67917E-3/( 57.362E0 - sigma2)
    # see also Neckel & Labs 1984
    wave_vac = wave_air*fact
    return wave_vac



def ci_image1(atmos,line='Ha',contrib_file='./',mu=0.95,time=0.,xlim=[6560,6564],ylim=[-100,1500],ci_log=False,vmax=0.5,vmin=0.5*1e-5,user_cmap='gray', oplot_Ilam = True, Ilam_color='white', oplot_vel=True,vel_color='gray',oplot_legend2=True,oplot_legend1=True,savefig=False,plot_filename='contrib_fn_plot',user_figsize=(6,6),user_fontsize=14,ci_prime=[-99,-99],ci_zlim=[-200,-200],ciprime_color='white',oplot_tau1=False, tau_color='k',tau_2d = False,tlim0=0,tlim1=30,src_2d=False,source_ha=False,oplot_t0=True, oplot_annotate=False,flip_wl=True):
    '''  default values for the call are indicated here: 
    your_python_dictionary = adx.ci_image1(atmos,time=18,vmin=-2,vmax=1,xlim=[6560,6566],\
        user_cmap=rnbw_map,savefig=True,user_figsize=(6,6),ci_log=True,user_fontsize=14,\
                                  vel_color='#BBBBBB',oplot_tau1=1)  '''
   # model_dir = np.load('model_dir.tmp.npy')
 #   model_contrib = np.load('model_contrib.tmp.npy')
   # contribf = scipy.io.readsav(str(model_dir)+str(model_contrib),verbose=False,python_dict=True)
    contribf = scipy.io.readsav(contrib_file,verbose=False,python_dict=True)
    
   # model_file = np.load('model_file.tmp.npy')
    cf = contribf['lcontribf'][0]
  #  cf.dtype
    col_rnbw = color_rainbow14()
    if mu < 0.51:
        print('Are you sure you want to look at a mu-value <= 0.5 for a plane parallel flare atmosphere?')
    muind = findind(atmos.zmu, mu)
    user_mu = atmos.zmu[muind]
    if line == 'Ha' and mu==0.95: 
        cfline = cf.LHAINT95_T
        plt_label = r'H$\alpha$'
        lam_rest = atmos.alamb[2]
    if line == 'Ha' and mu==0.77: 
        cfline = cf.LHAINTT77
        plt_label = r'H$\alpha$'
        lam_rest = atmos.alamb[2]
        
    if line == 'Hg' and mu ==0.95:
        cfline = cf.LHGINT95_T
        plt_label=r'H$\gamma$'
        lam_rest = atmos.alamb[7]
        # need to finish
    if line == 'Hg' and mu ==0.77:
        cfline = cf.LHGINTT77
        plt_label=r'H$\gamma$'
        lam_rest = atmos.alamb[7]
        # need to finish

    if line == 'Ca II K' and mu ==0.95:
        cfline = cf.LCAIIKINTT95
        plt_label = 'Ca II K'
        lam_rest = atmos.alamb[17]
    if line == 'Ca II 8542' and mu ==0.95:
        cfline = cf.LCAII8542INTT95
        plt_label = 'Ca II 8542'
        lam_rest = atmos.alamb[20]
    if source_ha == True:
        cfline_ha = cf.LHAINTT95
        # need to finish

    if lam_rest > 3000.:
        lam_rest = vactoair(lam_rest)
        
    print('Plotting contribution function (erg/s/cm3/sr/Ang) for ',plt_label,' at mu= {:0.3f}'.format(user_mu), 'at time = {:0.3f} '.format(time), 'sec for model',str(contrib_file),'.')
    # to do:  put in other lines that adam has stored.
    #print(cfha.dtype)   this prints the available arrays 
    contribline = cfline['contribf']
    contriblinewl = cfline['lam']
    c_I_line = contribline[0].transpose()  # at mu = 0.95
    c_I_line_wl = contriblinewl[0].transpose()


   # contribline_ha = cfline_ha['contribf']
   # contriblinewl_ha = cfline_ha['lam']
    
    tind = findind(atmos.timet, time)
    if ylim[0] < 0:
        ylim[0] = np.min(atmos.z1t[:,tind]/1e5)
    zprep = prep_pmesh(atmos.z1t[:,tind]/1e5)
    zprep2 = atmos.z1t[:,tind]/1e5
    wlprep2 = c_I_line_wl[:,tind]
    wlprep = prep_pmesh(c_I_line_wl[:,tind])
    wl2d, z2d = np.meshgrid(wlprep,zprep)
    vz2d, z2dx = np.meshgrid((lam_rest-wlprep)/lam_rest*2.998e5,zprep)
    vzprep2 = (lam_rest-wlprep2)/lam_rest*2.998e5
    user_time = atmos.timet[tind]
    plt.rc('font',size=user_fontsize)
    f, (ax1,ax4) = plt.subplots(ncols=2,figsize=user_figsize, sharey='row',
                               gridspec_kw={'width_ratios': [4,1]})
#fig.set_tight_layout({'rect': [0, 0, 1, 0.95], 'pad': 0, 'h_pad': 0})
    if ci_log == 0:
        ax1.pcolormesh(wl2d, z2d, c_I_line[:,:,tind],vmax=vmax,vmin=vmin,cmap = user_cmap,rasterized=True)
    else:
        ci0 = np.log10(c_I_line[:,:,tind].squeeze())
        xmap = color_map(umap=user_cmap)
        if tau_2d == True:
            tauall = cfline['tau']
            tauline = tauall[0].transpose()
         #   print(tauline.shape, wl2d.shape, z2d.shape)
            if flip_wl:
                ax1.pcolormesh(wl2d, z2d,np.log10(np.flip(tauline[:,:,tind]/mu,axis=1)),vmax=vmax,vmin=vmin,cmap = xmap,rasterized=True)
            else:
                ax1.pcolormesh(wl2d, z2d,np.log10(tauline[:,:,tind]),vmax=vmax,vmin=vmin,cmap = xmap,rasterized=True)
        elif src_2d == True:
            srcall = cfline['src']
            srcline = srcall[0].transpose()
            print(srcline.shape, wl2d.shape, z2d.shape)
            plvec = np.vectorize(planckfni)
            b1d = np.zeros((len(atmos.tg1t[:,tind]),1))
            b1d[:,0] = plvec(np.median(wlprep), atmos.tg1t[:,tind])
            if flip_wl:
                src_flipped = np.flip(srcline[:,:,tind],axis=1)
            else:
                src_flipped = srcline[:,:,tind]
            dnu2dlam = np.zeros_like(src_flipped) + cnst.CCANG / np.median(wl2d)**2
            src_flipped_dlam = src_flipped * dnu2dlam
            b2d = np.broadcast_to(b1d, src_flipped.shape)
            print(b1d)
            ax1.pcolormesh(wl2d, z2d,( src_flipped_dlam/ b2d),vmax=vmax,vmin=vmin,cmap =xmap,rasterized=True)
            src_ratio =  src_flipped_dlam/ b2d
        else:
            ax1.pcolormesh(wl2d, z2d,ci0,vmax=vmax,vmin=vmin,cmap = xmap,rasterized=True)
    ax1.set_ylim(ylim)
    ax1.set_xlim(xlim)
    ax1.set_xlabel(r'Wavelength ($\rm{\AA}$)')
    ax1.set_ylabel('Distance [km] from Photosphere')
    if oplot_Ilam:
        contriblineint = cfline['int']
        emerg_intline = contriblineint[0].transpose()
        ax1.plot(c_I_line_wl[:,tind], emerg_intline[:,tind] * ylim[1] / np.max(emerg_intline[:,tind]) * 0.75 ,color=Ilam_color,label=r'I$_{\lambda}$',lw=2.0,marker='+',ms=6.)
        if oplot_legend1:
            ax1.legend(loc='upper left',frameon=False,labelcolor=Ilam_color)
        print('The maximum emergent I_lam (erg/s/cm2/sr/Ang) for this profile is {:0.3e}'.format(np.max(emerg_intline[:,tind])))

    if oplot_tau1:
        tauall = cfline['tau']
        tauline = tauall[0].transpose()
        shptau = tauline.shape
        tau2deq1 = np.zeros((shptau[1]))
        for tt in range(shptau[1]):
            tau2deq1[tt] = np.interp(1.0, tauline[:,tt,tind] / mu, atmos.z1t[:,tind]/1e5)
        if flip_wl:
            ax1.plot(c_I_line_wl[:,tind], np.flip(tau2deq1),color=tau_color,ls='dashed',label=r'$\tau=1$',lw=2,zorder=22)  # need to flip tau because contribf is flipped in contribfunc.pro
        else:
            ax1.plot(c_I_line_wl[:,tind], tau2deq1,color=tau_color,ls='dashed',label=r'$\tau=1$',lw=2,zorder=22)
        ax1.legend(loc='upper left',frameon=False,labelcolor='white',ncol=2)

        
    if ci_prime[0] > 0 and ci_prime[1] > 0:
        nlam = len(c_I_line_wl[:,tind])
        ciinds = np.all([atmos.z1t[:,tind]/1e5 > ci_zlim[0], atmos.tg1t[:,tind] < 1e5],axis=0)
        nzci = np.count_nonzero(ciinds)
        CIPRIME = np.zeros((nlam,nzci) )
        CIPRIMEZ0 = np.zeros(nlam)
        for ww in range(nlam):
            dzt_sel = atmos.dzt[ciinds,tind]
            c_I_line_sel = c_I_line[ciinds, :, tind]
            z1t_sel = atmos.z1t[ciinds,tind]
            ZPRIME, CIPRIME[ww,:] = np.abs(akcdf_dz(dzt_sel, c_I_line_sel[:,ww],norm=True))
            CIPRIMEZ0[ww] = np.interp(ci_prime[0], CIPRIME[ww,:], z1t_sel)
        ax1.plot(c_I_line_wl[:,tind], CIPRIMEZ0/1e5, ls=(0,(5,1)),color=ciprime_color,lw=0.7)
        
        nlam = len(c_I_line_wl[:,tind])
        ciinds = np.all([atmos.z1t[:,tind]/1e5 > ci_zlim[1], atmos.tg1t[:,tind] < 1e5],axis=0)
        nzci = np.count_nonzero(ciinds)
        CIPRIME = np.zeros((nlam,nzci) )
        CIPRIMEZ1 = np.zeros(nlam)
        for ww in range(nlam):
            dzt_sel = atmos.dzt[ciinds,tind]
            c_I_line_sel = c_I_line[ciinds, :, tind]
            z1t_sel = atmos.z1t[ciinds,tind]
            ZPRIME, CIPRIME[ww,:] = np.abs(akcdf_dz(dzt_sel, c_I_line_sel[:,ww],norm=True))
            CIPRIMEZ1[ww] = np.interp(ci_prime[1], CIPRIME[ww,:], z1t_sel)
        ax1.plot(c_I_line_wl[:,tind], CIPRIMEZ1/1e5, ls=(0,(5,1)),color=ciprime_color,lw=0.7)
    global X 
    X= vzprep2
    global Y
    Y=zprep2
    global ZVALS

    if tau_2d == True:
        if flip_wl:
            ZVALS = np.flip(tauline[:,:,tind] / mu,axis=1)
        else:
            ZVALS = tauline[:,:,tind] / mu
    elif src_2d == True:
        ZVALS = src_ratio
    else:
        ZVALS = c_I_line[:,:,tind]
        
    ax2 = ax1.twiny()
    if oplot_vel:
        ax2.plot(atmos.vz1t[:,tind]/1e5 * mu, atmos.z1t[:,tind]/1e5,ls='solid',color=vel_color,label=r'$v$',lw=1.75)  # ls=(0,(3,1,1,1,1,1))

    dlammin = lam_rest - xlim[0]
    dlamplus = lam_rest - xlim[1]

    ax2.set_xlim(dlammin/lam_rest *2.998e5, dlamplus/lam_rest * 2.998e5)
    ax2.set_xlabel('L.o.S. Gas Velocity (km s$^{-1}$); negative = downward')

    if oplot_annotate:
        ax2.text(-325,100,'Backwarmed Upper',ha='center',va='center',fontsize=10)
        ax2.text(-325,50,'Photosphere',ha='center',va='center',fontsize=10)

        ax2.text(-325,830,'Stationary Chrom',ha='center',va='center',fontsize=10)
        ax2.text(-325,780,'Flare Layers',ha='center',va='center',fontsize=10)
        ax2.text(-325,890,'CC',ha='center',va='center',fontsize=10)
        ax2.text(-325,1000,'Evaporation',ha='center',va='center',fontsize=10)

    if oplot_legend2:
        ax2.legend(loc='upper right',frameon=False,labelcolor=vel_color)
    ax2.format_coord = format_coord
    ax4.plot(atmos.tg1t[:,tind]/1000.0, atmos.z1t[:,tind]/1e5,color='k')
    ax4.set_xlim(tlim0,tlim1)
    bright = color_bright()
    tinc = np.arange(0, tlim1, 5)
    for ti in range(len(tinc)):
        ax4.plot([tinc[ti],tinc[ti]],[-100,1500],color=bright[6],lw=0.7)

    ax4.plot(atmos.tg1t[:,tind]/1000.0, atmos.z1t[:,tind]/1e5,color='k',label='Gas Temp')

    if oplot_t0:
        ax4.plot(atmos.tg1t[:,0]/1000.0, atmos.z1t[:,0]/1e5,color='k',label='Gas Temp (t=0s)',ls='dotted')

  
    srcall = cfline['src']
    srcline = srcall[0].transpose()
            #print(srcline.shape, wl2d.shape, z2d.shape)
            #plvec = np.vectorize(planckfni)
            #b1d = np.zeros((len(atmos.tg1t[:,tind]),1))
            #b1d[:,0] = plvec(np.median(wlprep), atmos.tg1t[:,tind])
    if flip_wl:
        src_flipped = np.flip(srcline[:,:,tind],axis=1)
    else:
        src_flipped = srcline[:,:,tind]
    dnu2dlam = np.zeros_like(src_flipped) + cnst.CCANG / np.median(wl2d)**2
    src_flipped_dlam = src_flipped * dnu2dlam
    src_slice_dlam = src_flipped_dlam[:,15]
    src_trad = np.zeros(len(src_slice_dlam))
    for tt in range(len(src_slice_dlam)):
        src_trad[tt] = trad(lam_rest, src_slice_dlam[tt])
        
    ax4.plot(src_trad/1000, atmos.z1t[:,tind]/1e5,color=bright[4],ls='dashed',label='Source Fctn Temp')

    if source_ha == True:
        srcall_ha = cfline_ha['src']
        srcline_ha = srcall_ha[0].transpose()
        if flip_wl:
            src_flipped_ha = np.flip(srcline_ha[:,:,tind],axis=1)
        else:
            src_flipped_ha = srcline_ha[:,:,tind]
        dnu2dlam_ha = np.zeros_like(src_flipped_ha) + cnst.CCANG / np.median(6562.8)**2
        src_flipped_dlam_ha = src_flipped_ha * dnu2dlam_ha
        src_slice_dlam_ha = src_flipped_dlam_ha[:,25]
        src_trad_ha = np.zeros(len(src_slice_dlam_ha))
        for tt in range(len(src_slice_dlam_ha)):
            src_trad_ha[tt] = trad(6562.8, src_slice_dlam_ha[tt])
        
        ax4.plot(src_trad_ha/1000, atmos.z1t[:,tind]/1e5,color=bright[4],ls='dashed',label=r'H$\alpha$ Source Function')
    
    ax4.set_ylim(ylim)
    ax4.set_xlabel(r'Temp ($10^3$ K)')
    ax4.legend(fontsize=8,frameon=False,loc=(.02,1.03))
    tval = user_time
    plt.title('t = {0:.2f}'.format(user_time)+' s')
    plt.tight_layout()
    if savefig:
        plt.savefig(plot_filename+'.pdf')
        print('created plot: ',plot_filename+'.pdf')
    print('The map value range is [',vmin,vmax,'] erg/s/cm3/sr/Ang.')
    print('Returned height (km), wl (Ang), and contribution function with dimensions:',zprep2.shape, wlprep2.shape, c_I_line.shape)
    tauall = cfline['tau']
    tauline = tauall[0].transpose()
         #   print(tauline.shape, wl2d.shape, z2d.shape)
            #ax1.pcolormesh(wl2d, z2d,np.log10(np.flip(tauline[:,:,tind]/mu,axis=1)),vmax=vmax,vmin=vmin,cmap = xmap,rasterized=True)
            
    ilam_ret = emerg_intline[:,tind]

    if flip_wl:
        tau_return = np.flip(tauline[:,:,tind]/mu,axis=1)
    else:
        tau_return = tauline[:,:,tind]/mu
    ci_dict = {'zpmesh':z2d, 'wlpmesh':wl2d, 'z1d':zprep2, 'wl1d':wlprep2, 'contrib2D':c_I_line[:,:,tind], 'lam0':lam_rest, 'Ilam':ilam_ret, 'tau2D':tau_return} 
    return ci_dict
    

def color_rainbow14(printc = 'no'):
    ''' This is rainbow14 plus grey as last entry, Figure 18 top panel of Paul Tol's website.  color_rainbow(printc = no or yes)'''
    rainbow = [(209,187,215), (174,118,163), (136,46,114), (25,101,176), (82,137,199), (123,175,222), (77,178,101), (144,201,135), (202, 224, 171), (247, 240, 86), (246,193, 65), (241,147,45), (232, 96,28), (220, 5,12), (119, 119, 119)]
    labels=['ltpurple0', 'medpurple1','darkpurple2', 'darkblue3','medblue4', 'lightblue5', 'darkgreen6','medgreen7', 'ltgreen8','yellow9','ltorange10','medorange11', 'dkorange12', 'red13', 'grey14']
    for i in range(len(rainbow)):    
        r, g, b = rainbow[i]    
        rainbow[i] = (r / 255., g / 255., b / 255.)
        if printc == 'yes' or printc =='y':
            print(i, labels[i])
    return rainbow

# Good color schemes to use from https://www.sron.nl/~pault/
def color_map(umap = 'rnbw'):
#    ''' user_cmap = mf.color_map(umap='rnbw') where umap can be burd, burd_flip, or bryl'''
    from matplotlib.colors import LinearSegmentedColormap
    from matplotlib import cm
    if umap == 'rnbw':  # this is rainbow34 aka rainbow_WhBr from Figure 20 of Paul Tol's website for interpolating.
        print('Brown to White rainbow.')
        clrs = ['#E8ECFB', '#DDD8EF', '#D1C1E1', '#C3A8D1', '#B58FC2','#A778B4','#9B62A7', '#8C4E99', '#6F4C9B', '#6059A9',  '#5568B8', '#4E79C5', '#4D8AC6', '#4E96BC', '#549EB3', '#59A5A9', '#60AB9E', '#69B190', '#77B77D', '#8CBC68',  '#A6BE54', '#BEBC48', '#D1B541', '#DDAA3C', '#E49C39', '#E78C35', '#E67932', '#E4632D', '#DF4828', '#DA2222', '#B8221E', '#95211B', '#721E17', '#521A13']
        cmap_name = 'rainbow_brwh'
        usermap = LinearSegmentedColormap.from_list(cmap_name, np.flip(clrs), N=500)
      #  usermap.set_bad('#666666')
        usermap.set_bad('#521A13')
    if umap == 'rnbw_flip':  # this is rainbow34 aka rainbow_WhBr from Figure 20 of Paul Tol's website for interpolating.
        print('Brown to White rainbow.')
        clrs = ['#E8ECFB', '#DDD8EF', '#D1C1E1', '#C3A8D1', '#B58FC2','#A778B4','#9B62A7', '#8C4E99', '#6F4C9B', '#6059A9',  '#5568B8', '#4E79C5', '#4D8AC6', '#4E96BC', '#549EB3', '#59A5A9', '#60AB9E', '#69B190', '#77B77D', '#8CBC68',  '#A6BE54', '#BEBC48', '#D1B541', '#DDAA3C', '#E49C39', '#E78C35', '#E67932', '#E4632D', '#DF4828', '#DA2222', '#B8221E', '#95211B', '#721E17', '#521A13']
        cmap_name = 'rainbow_brwh'
        usermap = LinearSegmentedColormap.from_list(cmap_name, clrs, N=500)
    elif umap == 'burd':
        BuRd = ["#2166AC", "#4393C3", "#92C5DE", "#D1E5F0","#F7F7F7", "#FDDBC7","#F4A582", "#D6604D", "#B2182B"]  # bad = 255,238,153 = FFEE99
        cmap_name = 'BuRd' 
        usermap = LinearSegmentedColormap.from_list(cmap_name, np.flip(BuRd), N=100)
    elif umap == 'burd_flip':
        BuRd = ["#2166AC", "#4393C3", "#92C5DE", "#D1E5F0","#F7F7F7", "#FDDBC7","#F4A582", "#D6604D", "#B2182B"]  # bad = 255,238,153 = FFEE99
        cmap_name = 'BuRd_Flipped' 
        usermap = LinearSegmentedColormap.from_list(cmap_name, BuRd, N=100)
    elif umap == 'bryl':
        clrs_ylbr = ['#FFFFE5', '#FFF7BC','#FEE391','#FEC44F','#FB9A29','#EC7014','#CC4C02', '#993404','#662506']
        cmap_name = 'ylbr'
        usermap = LinearSegmentedColormap.from_list(cmap_name, np.flip(clrs_ylbr), N=500)
        usermap.set_bad('#662506')
    else:
        print( ' umap can be rnbw, burd, burd_flip, or bryl')
   
    if umap == 'BWB':  # this is rainbow34 aka rainbow_WhBr from Figure 20 of Paul Tol's website for interpolating.
        print('Brown to White rainbow.')
        clrs = ['#000000','#FFFFFF']
        cmap_name = 'BWB_flip'
        usermap = LinearSegmentedColormap.from_list(cmap_name, np.flip(clrs), N=500)
      #  usermap.set_bad('#666666')
        usermap.set_bad('#FFFFFF')

    if umap == 'BWB':  # this is rainbow34 aka rainbow_WhBr from Figure 20 of Paul Tol's website for interpolating.
        print('Brown to White rainbow.')
        clrs = ['#000000','#FFFFFF']
        cmap_name = 'BWB'
        usermap = LinearSegmentedColormap.from_list(cmap_name, clrs, N=500)
      #  usermap.set_bad('#666666')
        usermap.set_bad('#000000')
    return usermap


def trad(wl, ilam):
    # can solve for T_rad on your own using the blackbody formula:
    # ilam in erg/s/cm2/sr/ang,  wl in ang.
    inuv_percm = ilam * 1e8
    hh, cc, kb = 6.626e-27, 2.998e10, 1.38e-16
    Trad = (1./(np.log( (2.0 * hh * cc**2) / (inuv_percm * (wl/1e8)**5) + 1.0))) * \
        hh * cc / (kb * wl/1e8)
    return Trad
    

def akcdf_dz(dz,y,norm=False):
    ciprime = np.zeros_like(y)
    zprime = np.zeros_like(y)
    for j in range(len(dz)):
        ciprime[j] = np.sum(y[0:j]*dz[0:j])
        zprime[j] = np.sum(dz[0:j])
    if norm == True:
        ciprime = ciprime / np.sum(y*dz)
    return zprime, ciprime




def format_coord(x, y):
    global X, Y, ZVALS
    xarr=X
    yarr=Y
    colx = findind(xarr,x)
    rowy = findind(yarr,y)
    zval = ZVALS[rowy, colx]
    return 'x=%1.4f, y=%1.4f, indx = %1i, indy=%4i, val=%1.4e' % (x, y, colx, rowy, zval)

def format_coordxy(x, y):
    global XX, YY, ZZ
    xarr=XX
    yarr=YY
    zarr=ZZ
    colx = findind(xarr,x)
    #rowy = findind(yarr,y)
    #rowy2 = findind(zarr,
    zval = zarr[colx]
    yval = yarr[colx]
    xval = xarr[colx]
    return 'x=%1.4f, y1=%1.2e, y2=%1.2e, indx = %1i' % (xval, zval, yval, colx)


def color_bright(printc='no'):
    ''' color_bright(printc = no or yes) '''
    bright = [(68,119,170), (102,204,238), (34, 136, 51), (204,187,68), (238,102,119), (170,51,119), (187,187,187)]   
    labels=['blue' ,'cyan', 'green', 'yellow','red','purple', 'light grey']
    for i in range(len(bright)):    
        r, g, b = bright[i]    
        bright[i] = (r / 255., g / 255., b / 255.)
        if printc == 'yes' or printc =='y':
            print(i, labels[i])
    return bright


def load_VCSHG(fname, time=-99.0):
    vac2air = np.vectorize(vactoair)
    vcs = scipy.io.readsav(fname)
    line_flux_t_vcs = vcs.line_flux_vcs_t
    line_flux_t0_vcs = vcs.line_flux_vcs_t0
    line_lam_vcs = vcs.line_vcs_lam
    line_lam_air_vcs = vac2air(line_lam_vcs)
    timet = vcs.timet_spec
    line_flux_ave_vcs = vcs.line_flux_vcs_ave
    ave_cont_wl = vcs.ave_cont_wl
    ave_cont_flux = vcs.ave_cont_flux
    cont_flux_t = vcs.cont_flux_t
    ave_cont_flux_prime = vcs.ave_cont_flux
    if time < 0:
        line_select = line_flux_ave_vcs
    else:
        tind = findind(timet, time)
        print('Returning for time = ',timet[tind])
        line_select = line_flux_t_vcs[tind,:]
        print(line_flux_t_vcs.shape)
    print('returned lam(air) in Ang, flux (erg/s/cm2/Ang)')
    return line_lam_air_vcs, line_select




def findind_lower(arr, val):
     tmp = val - arr
     good = (tmp > 0.0)
     ngood = np.count_nonzero(good)
     index = ngood-1
     return index

def bilinear_ry(x0, y0, z, x, y):
    # follows bilinear.f in RADYN source code.  x should be electron density grid (17), y should be temperature grid (7)
    ind1 = findind_lower(x, x0)
    ind2 = findind_lower(y, y0)
    t = (x0 - x[ind1])/(x[ind1+1] - x[ind1])
    u = (y0 - y[ind2])/(y[ind2+1] - y[ind2])

    bilinear = (1-t)*(1-u)*z[ind1,ind2] + t*(1-u)*z[ind1+1,ind2] + t*u*z[ind1+1,ind2+1] + (1-t)*u*z[ind1,ind2+1]
    return bilinear


def readtevol(model_id = 'mF13-85-3', field='C3615p', aveval=-9, model_dir = '/home/adamkowalski/Dropbox/0-Final_Products/ModelOutput/tx_archive/dm/K21_Grid/archive_meta/',print_vals=False):
# To get a list of possible fields, just call readtevol() without any arguments.

    fname = glob.glob(model_dir+'modelvals*'+model_id+'*tevol*new*dat')
    if len(fname) > 1:
        print('Found more than 1 file with that ID!!!!')
        return None
    tevol_meta = ascii.read(fname[0],header_start=0, data_start=1,data_end=2)
    tevol_all = ascii.read(fname[0],header_start=2, data_start=3)

    if aveval > 0:
        print(field, tevol_all[field][-1])
        return float(tevol_all[field][-1])
     
    else:
        times = np.array(tevol_all["time_s"][0:-2])
        try:
            print('Calculated spectral quantities from ', fname[0])
            lc = np.array(tevol_all[field][0:-2])
            if print_vals:
                for tt in range(len(lc)):
                    print(times[tt], lc[tt])
            return times, lc
        except:
            print(tevol_all.keys())
    



def load_spec(model_id='mF13-85-3', time = 1.0, stype = 'cont', norm_wl = -99.0, silent=True,model_dir = '/home/adamkowalski/Dropbox/0-Final_Products/ModelOutput/tx_archive/dm/K21_Grid/grid/'):
    # This used to be radxspec
    # time can be a specific time from t=0s to 9.8s
    # if time is > -10 and < 0, then it returns time-averaged spectrum
    # if time < -10, then it returns the spectra at all times
    
    
    fname = glob.glob(model_dir+'radyn_spectra/spec.*'+model_id+'*')

    if len(fname) > 1:
        print('Error:  Found more than one with that model ID.  Make sure periods are in the model_id')
        return None
    
    radyn = scipy.io.readsav(fname[0])

    print('Reading in spectra from ',fname[0])
    tind = findind(radyn.flam_evol[0].time_s, time)

    t_spec = radyn.flam_evol[0].time_s[tind]

    if time < 0 and time > -10:
        t_spec = time
        
    if time >=  0:  # The flam_evol structures give the spectrum at all times (usually dt = 0.2s, sometimes smaller)
        if stype == 'cont': # non-equilibrium b-f and f-f spectrum (continuum) only, no b-b.  Hyd, Helium, Ca II continua in detail, background continua from other elements in LTE are listed in opctab.dat file (see Allred et al. 2015).
            spec_ret = radyn.flam_evol[0].cont_flux[tind]
            wl_ret = radyn.flam_evol[0].cont_wl[tind]
            t0_ret = radyn.flam_evol[0].cont_flux_pre[tind]  # NOTE: this has many time indices so that it would work
            # with the IDL tool rmovie.pro. radyn.flam_evol[0].cont_flux_pre[tind] is the same as radyn.flam_evol[0].cont_flux[0]
        if stype == 'cont_i95':
            spec_ret = radyn.flam_evol[0].icont95[0].int[tind]
            t0_ret = radyn.flam_evol[0].icont95[0].int0[tind]
            wl_ret = radyn.flam_evol[0].icont95[0].lam[tind]
            
        if stype == 'merged':   # non-equilibrium b-f and f-f spectrum (continuum) + hyd Balmer non-equi. b-b with new Stark broadening (H alpha, H beta, H gamma)
            spec_ret = radyn.flam_evol[0].merged_flux[tind]
            wl_ret = radyn.flam_evol[0].merged_wl[tind]
            t0_ret =  radyn.flam_evol[0].merged_flux_pre[tind]
        if stype == 'halpha' or stype == 'Ha' or stype == 'Halpha' or stype == 'H alpha' or stype == 'ha': # just H alpha at 51 wavelength points (continuum over wavelength range included)
            spec_ret = radyn.flam_evol[0].ha_flux[tind]
            wl_ret = radyn.flam_evol[0].ha_wl[tind]
            t0_ret = radyn.flam_evol[0].ha_flux_pre[tind]
        if stype == 'hbeta' or stype == 'Hb' or stype == 'Hbeta' or stype == 'H beta' or stype == 'hb': # just H beta at 31 wavelength points (continuum over wavelength range included)
            spec_ret = radyn.flam_evol[0].hb_flux[tind]
            wl_ret = radyn.flam_evol[0].hb_wl[tind]
            t0_ret = radyn.flam_evol[0].hb_flux_pre[tind]
        if stype == 'hgamma' or stype == 'Hg' or stype == 'Hgamma' or stype == 'H gamma' or stype == 'hg': # just H gmma at 31 wavelength points (continuum over wavelength range included)
            spec_ret = radyn.flam_evol[0].hg_flux[tind]
            wl_ret = radyn.flam_evol[0].hg_wl[tind]
            t0_ret = radyn.flam_evol[0].hg_flux_pre[tind]
        if stype == 'xray' or stype == 'x-ray' or stype == 'x ray' or stype == 'X-ray': # Just the X-ray spectrum from f-f continuum radiation from hydrogen and helium (optically thin continuum from T_gas > 1 MK), non-equilibrium ionization and excitation of H and He (and electron density) included!
            spec_ret = radyn.xflam_evol[0].cont_flux[tind]
            wl_ret = radyn.xflam_evol[0].cont_wl[tind]
            t0_ret = radyn.xflam_evol[0].cont_flux[0]
        
    if time  < 0 and time > -10: # The flam_ave structures give a single averaged over t1 to t2 (usually 0.2-9.8s).
        if stype == 'cont':
            spec_ret = radyn.flam_ave[0].cont_flux
            wl_ret = radyn.flam_ave[0].cont_wl
            t0_ret = radyn.flam_evol[0].cont_flux_pre[0]  
        if stype == 'merged':
            spec_ret = radyn.flam_ave[0].merged_flux
            wl_ret = radyn.flam_ave[0].merged_wl
            t0_ret =  radyn.flam_ave[0].merged_flux_pre
        if stype == 'halpha' or stype == 'Ha' or stype == 'Halpha' or stype == 'H alpha' or stype == 'ha':
            spec_ret = radyn.flam_ave[0].ha_flux
            wl_ret = radyn.flam_ave[0].ha_wl
            t0_ret = radyn.flam_evol[0].ha_flux_pre[0]
        if stype == 'hbeta' or stype == 'Hb' or stype == 'Hbeta' or stype == 'H beta' or stype == 'hb':
            spec_ret = radyn.flam_ave[0].hb_flux
            wl_ret = radyn.flam_ave[0].hb_wl
            t0_ret = radyn.flam_evol[0].hb_flux_pre[0]
        if stype == 'hgamma' or stype == 'Hg' or stype == 'Hgamma' or stype == 'H gamma' or stype == 'hg':
            spec_ret = radyn.flam_ave[0].hg_flux
            wl_ret = radyn.flam_ave[0].hg_wl
            t0_ret = radyn.flam_evol[0].hg_flux_pre[0]
        if stype == 'xray' or stype == 'x-ray' or stype == 'x ray' or stype == 'X-ray':
            spec_ret = radyn.xflam_ave[0].cont_flux
            wl_ret = radyn.xflam_ave[0].cont_wl
            t0_ret = radyn.xflam_evol[0].cont_flux[0]

    if time < -10:
        if stype == 'cont':
            spec_ret = radyn.flam_evol[0].cont_flux
            t0_ret = radyn.flam_evol[0].cont_flux_pre
            wl_ret = radyn.flam_evol[0].cont_wl
            print('returning all times with shapes (spec0, spectot, wl):', t0_ret.shape, spec_ret.shape, wl_ret.shape)

        if stype == 'hg' or stype == 'hgamma' or stype == 'Hgamma' or stype =='Hg':
            spec_ret = radyn.flam_evol[0].hg_flux
            t0_ret = radyn.flam_evol[0].hg_flux_pre
            wl_ret = radyn.flam_evol[0].hg_wl
    prime_spectrum = spec_ret - t0_ret

    if norm_wl > 0:
        wl_ind = findind(wl_ret, norm_wl)
        prime_spectrum = prime_spectrum / prime_spectrum[wl_ind]
        print('Normalized prime spectrum to wl = ',wl_ret[wl_ind])

    if not silent:
        print('Returned a dictionary with wl, t=0 spectrum, t=T spectrum, prime (preflare-subtracted) spectrum,  time')

    spec_dict = {'wl':wl_ret, 'spec_t0':t0_ret, 'spec':spec_ret, 'spec_prime':prime_spectrum, 'time_s':t_spec}
    return spec_dict


def rad2plot_help():
    names = ['Height','Col Mass', 'Temp', 'Density', 'Nel', 'Beam Heating', 'Pressure', 'Velocity']
    info = ['z1t/1e5 [km]', 'log10 cmass1t [g/cm2]', 'tg1t [K]', 'd1t [g/cm3]', 'ne1t [electrons/cm3]', 'bheat1t [erg/s/cm3]', 'pg1t [dyn/cm2]','vz1t/1e5 [km/s], positive=up']
    print('The options for rad2plot are the following: ')
    for nn in range(len(names)):
        print(names[nn],':', info[nn])
    return None

def rad2plot(atmos,x1in, y1in, y2in, time = 0.0, xlim=[-100,1500], y1lim=[3,6], y2lim=[3,6], user_figsize=(8,6), user_fontsize=16, oplot_t0=False,psym=False, y1log = False, y2log = False,savefig=False,plot_filename='rad2plot',y2_other=0):
    if x1in == 'Height':
        x1 = atmos.z1t/1e5
        x1in = x1in + ' (km)'
    if x1in == 'Col Mass':
        x1 = np.log10(atmos.cmass1t)
        x1in = x1in + r' (g cm$^{-2}$)'
        x1in = r'log$_{10}$ '+x1in
        
    if y1in == 'Temp':
        y1 = atmos.tg1t
        y1in = y1in +' (K)'
    if y1in == 'Density':
        y1 = atmos.d1t
        y1in = y1in+r' (g cm$^{-3}$)'
    if y1in == 'Nel':
        y1 = atmos.ne1t
        y1in = r'N$_e$ (cm$^{-3}$)'
    if y1in == 'Beam Heating':
        y1 = atmos.bheat1t
        y1in = y1in + r' (erg s$^{-1}$ cm$^{-3}$)'
    if y1in == 'Pressure':
        y1 = atmos.pg1t
        y1in = y1in + r' (dyn cm$^{-2}$)'
    if y1in == 'Velocity':
        y1 = atmos.vz1t/1e5
        y1in = y1in+r' (km s$^{-1}$)'

    if y2in == 'Temp':
        y2 = atmos.tg1t
        y2in = y2in +' (K)'
    if y2in == 'Density':
        y2 = atmos.d1t
        y2in = y2in+r' (g cm$^{-3}$)'
    if y2in == 'Nel':
        y2 = atmos.ne1t
        y2in = r'N$_e$ (cm$^{-3}$)'
    if y2in == 'Beam Heating':
        y2 = atmos.bheat1t
        y2in = y2in + r' (erg s$^{-1}$ cm$^{-3}$)'
    if y2in == 'Pressure':
        y2 = atmos.pg1t
        y2in = y2in + r' (dyn cm$^{-2}$)'
    if y2in == 'Velocity':
        y2 = atmos.vz1t/1e5
        y2in = y2in+r' (km s$^{-1}$)'
    if y2in == 'user':
        y2 = y2_other
        
    if y1log:
        y1 = np.log10(y1)
        y1in = r'log$_{10}$ '+y1in
    if y2log:
        y2 = np.log10(y2)
        y2in= r'log$_{10}$ '+y2in
    
    timet = atmos.timet
    brightcol = color_bright()
    rnbw_col = color_rainbow14()
    plt.rc('font',size=user_fontsize)
    f, ax1 = plt.subplots(figsize=user_figsize)
    indt1 = findind(timet, time)
    utime = timet[indt1]
    print('time = ',timet[indt1])
    print('min max of y1:',np.min(y1[:,indt1]), np.max(y1[:,indt1]))
    print('min max of y2:',np.min(y2[:,indt1]), np.max(y2[:,indt1]))

    if psym:
        ax1.plot(x1[:,indt1], y1[:,indt1], ls='solid',color='k',lw=2,marker='+')
    else:
        ax1.plot(x1[:,indt1], y1[:,indt1], ls='solid',color='k',lw=2)
    if oplot_t0 == True:
        ax1.plot(x1[:,0], y1[:,0], ls='dotted',color='k')
        print('Dotted linestyles are the t=0s atmospheric parameters.')
    ax1.set_ylim(y1lim)
    ax1.set_xlim(xlim)
    ax1.set_xlabel(x1in)
    ax1.set_ylabel(y1in)
    ax2 = ax1.twinx()
    if psym:
        ax2.plot(x1[:,indt1], y2[:,indt1],ls='dashed',color=rnbw_col[13],lw=2,marker='+')
    else:
        ax2.plot(x1[:,indt1], y2[:,indt1],ls='dashed',color=rnbw_col[13],lw=2)
    if oplot_t0 == True:
        ax2.plot(x1[:,0], y2[:,0],ls='dashdot',color=rnbw_col[13])
    ax2.set_ylabel(y2in,color=rnbw_col[13])
    ax2.set_ylim(y2lim)
    
    ax2.tick_params(axis='y', colors=rnbw_col[13])
    ax2.spines['right'].set_color(rnbw_col[13])
    ax2.set_title('t = '+str('{0:.2f}'.format(utime))+' s')
    global XX
    global YY
    global ZZ
    XX = x1[:,indt1]
    YY = y2[:,indt1]
    ZZ = y1[:,indt1]
    ax2.format_coord = format_coordxy
    plt.tight_layout()
    if savefig:
        plt.savefig(plot_filename+'.pdf')
        print('created plot: ',plot_filename+'.pdf')
    return None


def make_movie_2panels(model_id = 'mF13-85-3', model_dir = './', xtype = 'z',xrange=[-100,600], tstrt=0.0, tend=10.0, tinc = 0.2, yrange_ul = [2e3,30e6], yrange_ur = [1e2,1e6], yrange_lr = [-50,50], yrange_ll = [1e-11, 1e-6], Esel_1 = 150.0, Esel_2 = 350.0 ): 
    movie_name = "mov."+model_id+".mp4"  # "c5F11-25-4.2_Solar_10s_TB09_new_arrows.mp4"
    plot_title =  model_id  #r'$5\times 10^{11}$ erg cm$^{-2}$ s$^{-1}$, $\delta=4.2$, $E_c=25$ keV (log$_{10}$ $g=4.44$)'

    mpl.rcParams['font.family']='serif'
    cmfont = font_manager.FontProperties(fname=mpl.get_data_path() + '/fonts/ttf/cmr10.ttf')
    mpl.rcParams['font.serif']=cmfont.get_name()
    mpl.rcParams['mathtext.fontset']='cm'
    mpl.rcParams['axes.unicode_minus']=False

    bright = color_bright()

    model_1 = load_atmos(model_id = model_id, model_dir = model_dir)
    
    tmov_sel = np.arange(tstrt, tend, tinc)
    x = model_1.z1t / 1e5
    xlabel = '$z$: Distance (km) from Photosphere along Loop'
    timet = model_1.timet

    # upper left yaxis
    y_ul = model_1.tg1t
    yscale_ul = 'log'
    ylabel_ul = r'Temperature (K)'
    label_ul = 'Temp.' # if you want to plot a legend with ax1.legend()
    color_ul = 'black'
    oplot_ul = 1  # this controls if you want to plot t=0 values as dashed lines.

    # upper right yaxis
    y_ur = model_1.bheat1t
    yscale_ur = 'log'
    ylabel_ur = r'Q$_{\rm{beam}}$: $e$- Beam Heating (erg cm$^{-3}$ s$^{-1}$)'
    label_ur = r'Q$_{\rm{beam}}$'
    color_ur = bright[4]
    oplot_ur = 0

    # lower left yaxis
    y_lr = model_1.vz1t / 1e5
    yscale_lr = 'linear'
    ylabel_lr = r'Gas Velocity (km s$^{-1}$) neg: downward'
    label_lr = r'Vel. (neg: downflows)'
    color_lr = 'k'
    oplot_lr = 0

    y_ll = model_1.d1t

    yscale_ll = 'log'
    ylabel_ll = r'$\rho$: Mass Density (g cm$^{-3}$)'
    label_ll = r'$\rho$'
    color_ll = bright[2]
    oplot_ll = 1
    
    z0 = model_1.z1t[:,0]
    
    inds_movie = [0] * len(tmov_sel)
    ii=0
    while ii < len(tmov_sel):
        inds_movie[ii] = findind(timet, tmov_sel[ii])
        ii+=1
    import matplotlib.animation as ani

    outfname = movie_name
   
    plt.rc('font', family='serif',size=16)

    fig, (ax1, ax2) = plt.subplots(nrows=2,tight_layout=True,figsize=(9,9),sharex=True,sharey=False)


    writer = ani.writers['ffmpeg'](fps=10)
    with writer.saving(fig, outfname, 100):  # 100 dpi, larger gives larger movie
        for j in range(len(inds_movie)):

            i = inds_movie[j]
            print(timet[inds_movie[j]], model_1.timet[inds_movie[j]])
            ax1.plot(x[:,i], y_ul[:,i],label=label_ul,color=color_ul)
            ax1.set_ylabel(ylabel_ul,color=color_ul)
            ax1.set_ylim(yrange_ul)
            ax1.set_yscale(yscale_ul)
            ax1.set_xlim(xrange)
            ax1.text(-20,7e3,'T')
            ax1.grid(axis='both',alpha=0.35,which='both')  # axis='y'

            if yscale_ul == 'linear':
                ax1.ticklabel_format(style='sci',useMathText=True,axis='y',scilimits=(0,0)) 
               # ax1.text(0.1, 0.9, 'Time = '+"{:.2f}".format(timet[i])+' s', \
              #           horizontalalignment='left',verticalalignment='center',transform=ax1.transAxes, \
               #          fontsize=14,color='black')
            if oplot_ul == 1:
                ax1.plot(x[:,0], y_ul[:,0],ls='dashed',color=color_ul)
            ax1.set_title(plot_title+" time={:.2f}".format(timet[i])+' s',fontsize=14)

            if i > 0:
                ax1b.get_yaxis().set_visible(False)

            ax1b = ax1.twinx()
            ax1b.plot(x[:,i], y_ur[:,i],label=label_ur,color=color_ur,lw=2)

           # make_patch_spines_invisible(ax1b)
            ax1b.set_ylim(yrange_ur)
            ax1b.set_yscale(yscale_ur)
            ax1b.set_xlim(xrange)
            ax1b.set_ylabel(ylabel_ur,color=color_ur,alpha=1.0)
            ax1b.set_ylabel(ylabel_ur,color=color_ur,alpha=1.0)
            ax1b.set_ylabel(ylabel_ur,color=color_ur,alpha=1.0)

            #if yscale_ur == 'linear':
             #   ax1b.ticklabel_format(style='sci',useMathText=True,axis='y',scilimits=(0,0))
            #if oplot_ur == 1:
            #    ax1b.plot(x[:,0], y_ur[:,0],ls='dashed',color=color_ur)
        
       # ee1, gg, mm,lil,dz_tot1 = bstop.thicktarg_save_m(atmos_1, timet[inds_movie[j]], Esel_1, \
       #                                          1.0, -10, 0.511,\
      #                                 plot_it=False,helium=True,h2=False)
        #ax1bb = ax1.twinx()
      #  ax1bb.set_yscale('linear')
      #  ax1bb.set_ylim(0,1)
      #  ee2, gg, mm,lil, dz_tot2 = bstop.thicktarg_save_m(atmos_1, timet[inds_movie[j]], Esel_2, \
      #                  1.0, -10, 0.511,\
       #                                plot_it=False,helium=True,h2=False)
      #  ax1bb.plot(x[i,:], ee1 / np.max(ee1),color=bright[6],lw=1.5,ls='dashdot')
     #   ax1bb.plot(x[i,:], ee2 / np.max(ee2),color=bright[6],lw=1.5,ls='dashdot')

      #  make_patch_spines_invisible(ax1bb)
      #  ax1bb.get_xaxis().set_visible(False)
     #   ax1bb.get_yaxis().set_visible(False)

            ax2.plot(x[:,i], y_ll[:,i], color=color_ll,lw=2)
            ax2.text(50,2e-7,label_ll,ha='center',va='center',color=color_ll)
            ax2.set_ylim(yrange_ll)
            ax2.set_yscale(yscale_ll)
            ax2.set_xlim(xrange)
            ax2.set_xlabel(xlabel)
            ax2.set_ylabel(ylabel_ll,color=color_ll)
            ax2.grid(axis='both',alpha=0.35,which='both')  # axis='y'

            if yscale_ll == 'linear':
                ax2.ticklabel_format(style='sci',useMathText=True,axis='y',scilimits=(0,0))
            if oplot_ll == 1:
                ax2.plot(x[:,0], y_ll[:,0],ls='dashed',color=color_ll,zorder=50)
            if i > 0:
                ax2b.get_yaxis().set_visible(False)  # This is HORRIBLE BUG in recent versions of python.

            ax2b = ax2.twinx()
            ax2b.set_ylim(yrange_lr)
            ax2b.plot(x[:,0], np.zeros_like(x[:,0]), color='k',ls='dotted')
            ax2b.set_yscale(yscale_lr)
            ax2b.set_xlim(xrange)

            ax2b.set_ylabel(ylabel_lr,color='k')
            ax2b.plot(x[:,i], y_lr[:,i], color=color_lr,lw=2)
            #plt.tight_layout(pad=-0.8, w_pad=0.5, h_pad=1.)
            writer.grab_frame()
            ax1.cla()
            ax1b.cla()
            ax2.cla()
            ax2b.cla()
            
            # ax1bb.cla()
           # plt.cla()



    
def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
