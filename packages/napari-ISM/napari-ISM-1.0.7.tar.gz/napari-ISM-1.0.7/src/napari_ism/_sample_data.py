import numpy as np
from numpy.random import poisson
from scipy.signal import convolve

import brighteyes_ism.simulation.PSF_sim as ism
import brighteyes_ism.simulation.Tubulin_sim as simTub


def make_sample_data():
    """Generates an image"""

    grid = ism.GridParameters()

    grid.N = 5 # number of detector elements in each dimension
    grid.Nx = 201 # number of pixels of the simulation space
    grid.pxsizex = 25 # pixel size of the simulation space (nm)
    grid.pxdim = 50e3 # detector element size in real space (nm)
    grid.pxpitch = 75e3 # detector element pitch in real space (nm)
    grid.M = 500 # total magnification of the optical system (e.g. 100x objective follewd by 5x telescope)
    
    
    exPar = ism.simSettings()
    exPar.wl = 640 # excitation wavelength (nm)
    exPar.mask_sampl = 31
    
    emPar = exPar.copy()
    emPar.wl = 660 # emission wavelength (nm)
    
    z_shift = 0 #nm
    
    ###
    
    PSF, detPSF, exPSF = ism.SPAD_PSF_2D(grid, exPar, emPar, z_shift=z_shift, normalize=True)

    ### Generate tubulin

    tubulin = simTub.tubSettings()
    tubulin.xy_pixel_size = grid.pxsizex
    tubulin.xy_dimension = grid.Nx
    tubulin.xz_dimension = 1
    tubulin.z_pixel = 1     
    tubulin.n_filament = 5
    tubulin.radius_filament = grid.pxsizex*0.6
    tubulin.intensity_filament = [0.5, 0.9]
    phTub = simTub.functionPhTub(tubulin)
    
    TubDec = phTub[:, :, 0]
    flux = 1e4
    obj = TubDec * flux

    # Convolve tubulin with psf

    img = np.empty(PSF.shape)
    
    for n in range(grid.N**2):
        img[:, :, n] = convolve(obj, PSF[:, :, n], mode='same')
    
    # Convert to photons and add Poisson noise
    img[img < 0] = 0
    img = np.uint16(img)
    img = poisson(img)
    
    # optional kwargs for the corresponding viewer.add_* method
    scale = (grid.pxsizex, grid.pxsizex, 1)
    add_kwargs = {'colormap': 'magma', 'scale': scale}

    layer_type = "image"  # optional, default is "image"
    
    return [(img, add_kwargs, layer_type)]