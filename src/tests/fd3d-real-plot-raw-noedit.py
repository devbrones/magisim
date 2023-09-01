""" fd3d_4_3.py: 3d FDTD
Chapter 4 Section 3
3D FDTD simulation of a plane wave on a dielectric sphere
"""

from math import exp, sqrt, cos, sin

import numba
import numpy as np
from matplotlib import pyplot as plt


def calculate_pml_parameters(npml, ie, je, ke):
    """ Calculate and return the PML parameters """
    gi1 = np.zeros(ie)
    gi2 = np.ones(ie)
    gi3 = np.ones(ie)
    fi1 = np.zeros(ie)
    fi2 = np.ones(ie)
    fi3 = np.ones(ie)
    gj1 = np.zeros(je)
    gj2 = np.ones(je)
    gj3 = np.ones(je)
    fj1 = np.zeros(je)
    fj2 = np.ones(je)
    fj3 = np.ones(je)
    gk1 = np.zeros(ke)
    gk2 = np.ones(ke)
    gk3 = np.ones(ke)
    fk1 = np.zeros(ke)
    fk2 = np.ones(ke)
    fk3 = np.ones(ke)
    for n in range(npml):
        xxn = (npml - n) / npml
        xn = 0.33 * (xxn ** 3)
        fi1[n] = xn
        fi1[ie - n - 1] = xn
        gi2[n] = 1 / (1 + xn)
        gi2[ie - 1 - n] = 1 / (1 + xn)
        gi3[n] = (1 - xn) / (1 + xn)
        gi3[ie - 1 - n] = (1 - xn) / (1 + xn)
        fj1[n] = xn
        fj1[je - n - 1] = xn
        gj2[n] = 1 / (1 + xn)
        gj2[je - 1 - n] = 1 / (1 + xn)
        gj3[n] = (1 - xn) / (1 + xn)
        gj3[je - 1 - n] = (1 - xn) / (1 + xn)
        fk1[n] = xn
        fk1[ke - n - 1] = xn
        gk2[n] = 1 / (1 + xn)
        gk2[ke - 1 - n] = 1 / (1 + xn)
        gk3[n] = (1 - xn) / (1 + xn)
        gk3[ke - 1 - n] = (1 - xn) / (1 + xn)
        xxn = (npml - n - 0.5) / npml
        xn = 0.33 * (xxn ** 3)
        gi1[n] = xn
        gi1[ie - 1 - n] = xn
        fi2[n] = 1 / (1 + xn)
        fi2[ie - 1 - n] = 1 / (1 + xn)
        fi3[n] = (1 - xn) / (1 + xn)
        fi3[ie - 1 - n] = (1 - xn) / (1 + xn)
        gj1[n] = xn
        gj1[je - 1 - n] = xn
        fj2[n] = 1 / (1 + xn)
        fj2[je - 1 - n] = 1 / (1 + xn)
        fj3[n] = (1 - xn) / (1 + xn)
        fj3[je - 1 - n] = (1 - xn) / (1 + xn)
        gk1[n] = xn
        gk1[ke - 1 - n] = xn
        fk2[n] = 1 / (1 + xn)
        fk2[ke - 1 - n] = 1 / (1 + xn)
        fk3[n] = (1 - xn) / (1 + xn)
        fk3[ke - 1 - n] = (1 - xn) / (1 + xn)
    
    return gi1, gi2, gi3, fi1, fi2, fi3, gj1, gj2, gj3, fj1, fj2, fj3, gk1, gk2, gk3,fk1, fk2, fk3

@numba.jit(nopython=True)
def calculate_dx_field(ie, je, ke, dx, idx, hy, hz, gj3, gk3, gj2, gk2, gi1):
    """ Calculate the Dx Field """
    for i in range(1, ie):
        for j in range(1, je):
            for k in range(1, ke):
                curl_h = (hz[i, j, k] - hz[i, j - 1, k] - hy[i, j, k] + hy[i, j, k - 1])
                idx[i, j, k] = idx[i, j, k] + curl_h
                dx[i, j, k] = gj3[j] * gk3[k] * dx[i, j, k] + gj2[j] * gk2[k] * (0.5 * curl_h + gi1[i] * idx[i, j, k])
    return dx, idx

@numba.jit(nopython=True)
def calculate_dy_field(ie, je, ke, dy, idy, hx, hz, gi3, gk3, gi2, gk2, gj1):
    """ Calculate the Dy Field """
    for i in range(1, ie):
        for j in range(1, je):
            for k in range(1, ke):
                curl_h = (hx[i, j, k] - hx[i, j, k - 1] - hz[i, j, k] + hz[i - 1, j, k])
                idy[i, j, k] = idy[i, j, k] + curl_h
                dy[i, j, k] = gi3[i] * gk3[k] * dy[i, j, k] + gi2[i] * gk2[k] * (0.5 * curl_h + gj1[j] * idy[i, j, k])
    return dy, idy

@numba.jit(nopython=True)
def calculate_dz_field(ie, je, ke, dz, idz, hx, hy, gi3, gj3, gi2, gj2, gk1):
    """ Calculate the Dz Field """
    for i in range(1, ie):
        for j in range(1, je):
            for k in range(1, ke):
                curl_h = (hy[i, j, k] - hy[i - 1, j, k] - hx[i, j, k] + hx[i, j - 1, k])
                idz[i, j, k] = idz[i, j, k] + curl_h
                dz[i, j, k] = gi3[i] * gj3[j] * dz[i, j, k] + gi2[i] * gj2[j] * (0.5 * curl_h + gk1[k] * idz[i, j, k])
    return dz, idz

@numba.jit(nopython=True)
def calculate_inc_dy_field(ia, ib, ja, jb, ka, kb, dy, hx_inc):
    """ Calculate the incident Dy Field """
    for i in range(ia, ib + 1):
        for j in range(ja, jb + 1):
            dy[i, j, ka] = dy[i, j, ka] - 0.5 * hx_inc[j]
            dy[i, j, kb + 1] = dy[i, j, kb + 1] + 0.5 * hx_inc[j]
    return dy

@numba.jit(nopython=True)
def calculate_inc_dz_field(ia, ib, ja, jb, ka, kb, dz, hx_inc):
    """ Calculate the incident Dz Field"""
    for i in range(ia, ib + 1):
        for k in range(ka, kb + 1):
            dz[i, ja, k] = dz[i, ja, k] + 0.5 * hx_inc[ja - 1]
            dz[i, jb, k] = dz[i, jb, k] - 0.5 * hx_inc[jb]
    return dz

@numba.jit(nopython=True)
def calculate_e_fields(ie, je, ke, dx, dy, dz, gax, gay, gaz, gbx, gby, gbz, ex, ey, ez, ix, iy, iz):
    """ Calculate the E field from the D field"""
    for i in range(0, ie):
        for j in range(0, je):
            for k in range(0, ke):
                ex[i, j, k] = gax[i, j, k] * (dx[i, j, k] - ix[i, j, k])
                ix[i, j, k] = ix[i, j, k] + gbx[i, j, k] * ex[i, j, k]
                ey[i, j, k] = gay[i, j, k] * (dy[i, j, k] - iy[i, j, k])
                iy[i, j, k] = iy[i, j, k] + gby[i, j, k] * ey[i, j, k]
                ez[i, j, k] = gaz[i, j, k] * (dz[i, j, k] - iz[i, j, k])
                iz[i, j, k] = iz[i, j, k] + gbz[i, j, k] * ez[i, j, k]
    return ex, ey, ez, ix, iy, iz

@numba.jit(nopython=True)
def calculate_fourier_transform_ex(ie, je, number_of_frequencies, real_pt, imag_pt, ez, arg, time_step, kc):
    """ Calculate the Fourier transform of Ex"""
    for i in range(0, ie):
        for j in range(0, je):
            for m in range(0, number_of_frequencies):
                real_pt[m, i, j] = real_pt[m, i, j] + cos(arg[m] * time_step) * ez[i, j, kc]
                imag_pt[m, i, j] = imag_pt[m, i, j] - sin(arg[m] * time_step) * ez[i, j, kc]
    return real_pt, imag_pt

@numba.jit(nopython=True)
def calculate_hx_field(ie, je, ke, hx, ihx, ey, ez, fi1, fj2, fk2, fj3, fk3):
    """ Calculate the Hx field"""
    for i in range(0, ie):
        for j in range(0, je - 1):
            for k in range(0, ke - 1):
                curl_e = (ey[i, j, k + 1] - ey[i, j, k] - ez[i, j + 1, k] + ez[i, j, k])
                ihx[i, j, k] = ihx[i, j, k] + curl_e
                hx[i, j, k] = fj3[j] * fk3[k] * hx[i, j, k] + fj2[j] * fk2[k] * 0.5 * (curl_e + fi1[i] * ihx[i, j, k])
    return hx, ihx

@numba.jit(nopython=True)
def calculate_hy_field(ie, je, ke, hy, ihy, ex, ez, fj1, fi2, fk2, fi3, fk3):
    """ Calculate the Hy field"""
    for i in range(0, ie - 1):
        for j in range(0, je):
            for k in range(0, ke - 1):
                curl_e = (ez[i + 1, j, k] - ez[i, j, k] - ex[i, j, k + 1] + ex[i, j, k])
                ihy[i, j, k] = ihy[i, j, k] + curl_e
                hy[i, j, k] = fi3[i] * fk3[k] * hy[i, j, k] + fi2[i] * fk2[k] * 0.5 * (curl_e + fj1[j] * ihy[i, j, k])
    return hy, ihy

@numba.jit(nopython=True)
def calculate_hz_field(ie, je, ke, hz, ihz, ex, ey, fk1, fi2, fj2, fi3, fj3):
    """ Calculate the Hz field"""
    for i in range(0, ie - 1):
        for j in range(0, je - 1):
            for k in range(0, ke):
                curl_e = (ex[i, j + 1, k] - ex[i, j, k] - ey[i + 1, j, k] + ey[i, j, k])
                ihz[i, j, k] = ihz[i, j, k] + curl_e
                hz[i, j, k] = fi3[i] * fj3[j] * hz[i, j, k] + fi2[i] * fj2[j] * 0.5 * (curl_e + fk1[k] * ihz[i, j, k])
    return hz, ihz

@numba.jit(nopython=True)
def calculate_hx_inc(je, hx_inc, ez_inc):
    """ Calculate incident Hx field"""
    for j in range(0, je - 1):
        hx_inc[j] = hx_inc[j] + 0.5 * (ez_inc[j] - ez_inc[j + 1])
    return hx_inc

@numba.jit(nopython=True)
def calculate_hx_with_incident_field(ia, ib, ja, jb, ka, kb, hx, ez_inc):
    """ Calculate Hx with incident ez"""
    for i in range(ia, ib + 1):
        for k in range(ka, kb + 1):
            hx[i, ja - 1, k] = hx[i, ja - 1, k] + 0.5 * ez_inc[ja]
            hx[i, jb, k] = hx[i, jb, k] - 0.5 * ez_inc[jb]
    return hx

@numba.jit(nopython=True)
def calculate_hy_with_incident_field(ia, ib, ja, jb, ka, kb, hy, ez_inc):
    """ Calculate Hy with incident ez"""
    for j in range(ja, jb + 1):
        for k in range(ka, kb + 1):
            hy[ia - 1, j, k] = hy[ia - 1, j, k] - 0.5 * ez_inc[j]
            hy[ib, j, k] = hy[ib, j, k] + 0.5 * ez_inc[j]
    return hy

ie = 40
je = 40
ke = 40
ic = int(ie / 2)
jc = int(je / 2)
kc = int(ke / 2)
ia = 7
ja = 7
ka = 7
ib = ie - ia - 1
jb = je - ja - 1
kb = ke - ka - 1

ex = np.zeros((ie, je, ke))
ey = np.zeros((ie, je, ke))
ez = np.zeros((ie, je, ke))
ix = np.zeros((ie, je, ke))
iy = np.zeros((ie, je, ke))
iz = np.zeros((ie, je, ke))
dx = np.zeros((ie, je, ke))
dy = np.zeros((ie, je, ke))
dz = np.zeros((ie, je, ke))
idx = np.zeros((ie, je, ke))
idy = np.zeros((ie, je, ke))
idz = np.zeros((ie, je, ke))
hx = np.zeros((ie, je, ke))
hy = np.zeros((ie, je, ke))
hz = np.zeros((ie, je, ke))
ihx = np.zeros((ie, je, ke))
ihy = np.zeros((ie, je, ke))
ihz = np.zeros((ie, je, ke))
gax = np.ones((ie, je, ke))
gay = np.ones((ie, je, ke))
gaz = np.ones((ie, je, ke))
gbx = np.zeros((ie, je, ke))
gby = np.zeros((ie, je, ke))
gbz = np.zeros((ie, je, ke))
hx_inc = np.zeros(je)
ez_inc = np.zeros(je)

ddx = 0.01 # Cell size
dt = ddx / 6e8 # Time step size
epsz = 8.854e-12

number_of_frequencies = 3
freq = np.array((50e6, 200e6, 500e6))
arg = 2 * np.pi * freq * dt
real_in = np.zeros(number_of_frequencies)
imag_in = np.zeros(number_of_frequencies)
real_pt = np.zeros((number_of_frequencies, ie, je, ke))
imag_pt = np.zeros((number_of_frequencies, ie, je, ke))
amp = np.zeros((number_of_frequencies, je))

# Specify the dielectric sphere
epsilon = np.ones(2)
sigma = np.zeros(2)
epsilon[1] = 30
sigma[1] = 0.3
radius = 10

for i in range(ia, ib + 1):
    for j in range(ja, jb + 1):
        for k in range(ka, kb + 1):
            eps = epsilon[0]
            cond = sigma[0]
            xdist = ic - i - 0.5
            ydist = jc - j
            zdist = kc - k
            dist = sqrt(xdist ** 2 + ydist ** 2 + zdist ** 2)
            if dist <= radius:
                eps = epsilon[1]
                cond = sigma[1]
            gax[i, j, k] = 1 / (eps + (cond * dt / epsz))
            gbx[i, j, k] = cond * dt / epsz

for i in range(ia, ib + 1):
    for j in range(ja, jb + 1):
        for k in range(ka, kb + 1):
            eps = epsilon[0]
            cond = sigma[0]
            xdist = ic - i
            ydist = jc - j - 0.5
            zdist = kc - k
            dist = sqrt(xdist ** 2 + ydist ** 2 + zdist ** 2)
            if dist <= radius:
                eps = epsilon[1]
                cond = sigma[1]
            gay[i, j, k] = 1 / (eps + (cond * dt / epsz))
            gby[i, j, k] = cond * dt / epsz 
            
for i in range(ia, ib + 1):
    for j in range(ja, jb + 1):
        for k in range(ka, kb + 1):
            eps = epsilon[0]
            cond = sigma[0]
            xdist = ic - i
            ydist = jc - j
            zdist = kc - k - 0.5
            dist = sqrt(xdist ** 2 + ydist ** 2 + zdist ** 2)
            if dist <= radius:
                eps = epsilon[1]
                cond = sigma[1]
            gaz[i, j, k] = 1 / (eps + (cond * dt / epsz))
            gbz[i, j, k] = cond * dt / epsz     
            
# Pulse Parameters
t0 = 20
spread = 8

# Calculate the PML parameters
npml = 8
gi1, gi2, gi3, fi1, fi2, fi3, gj1, gj2, gj3, fj1, fj2, fj3, \
gk1, gk2, gk3, fk1, fk2, fk3 = calculate_pml_parameters(npml, ie, je, ke)

boundary_low = [0, 0]
boundary_high = [0, 0]

nsteps = 500

# Main FDTD Loop
for time_step in range(1, nsteps + 1):
    # Calculate the incident buffer
    for j in range(1, je - 1):
        ez_inc[j] = ez_inc[j] + 0.5 * (hx_inc[j - 1] - hx_inc[j])
        # Fourier transform of the incident field
        for m in range(number_of_frequencies):
            real_in[m] = real_in[m] + cos(arg[m] * time_step) * ez_inc[ja - 1]
            imag_in[m] = imag_in[m] - sin(arg[m] * time_step) * ez_inc[ja - 1]
            
            # Absorbing Boundary Conditions
            ez_inc[0] = boundary_low.pop(0)
            boundary_low.append(ez_inc[1])
            ez_inc[je - 1] = boundary_high.pop(0)
            boundary_high.append(ez_inc[je - 2])
            
            # Calculate the D Fields
            dx, idx = calculate_dx_field(ie, je, ke, dx, idx, hy, hz, gj3, gk3, gj2, gk2, gi1)
            dy, idy = calculate_dy_field(ie, je, ke, dy, idy, hx, hz, gi3, gk3, gi2, gk2, gj1)
            dz, idz = calculate_dz_field(ie, je, ke, dz, idz, hx, hy, gi3, gj3, gi2, gj2, gk1)
            
            # Add the source at the gap
            pulse = exp(-0.5 * ((t0 - time_step) / spread) ** 2)
            ez_inc[3] = pulse
            dy = calculate_inc_dy_field(ia, ib, ja, jb, ka, kb, dy, hx_inc)
            dz = calculate_inc_dz_field(ia, ib, ja, jb, ka, kb, dz, hx_inc)
            
            # Calculate the E field from the D field
            ex, ey, ez, ix, iy, iz = calculate_e_fields(ie, je, ke, dx, dy, dz, gax, gay, gaz, gbx, gby, gbz, ex, ey, ez, ix, iy, iz)
            
            # Calculate the Fourier transform of Ex
            real_pt, imag_pt = calculate_fourier_transform_ex(ie, je, number_of_frequencies, real_pt, imag_pt, ez, arg, time_step, kc)  
            # Calculate the H fields
            hx_inc = calculate_hx_inc(je, hx_inc, ez_inc)
            hx, ihx = calculate_hx_field(ie, je, ke, hx, ihx, ey, ez, fi1, fj2, fk2, fj3, fk3)
            hx = calculate_hx_with_incident_field(ia, ib, ja, jb, ka, kb, hx, ez_inc)
            hy, ihy = calculate_hy_field(ie, je, ke, hy, ihy, ex, ez, fj1, fi2, fk2, fi3, fk3)
            hy = calculate_hy_with_incident_field(ia, ib, ja, jb, ka, kb, hy, ez_inc)
            hz, ihz = calculate_hz_field(ie, je, ke, hz, ihz, ex, ey, fk1, fi2, fj2, fi3, fj3)   
            
# Calculate the Fourier amplitude of the incident pulse
amp_in = np.sqrt(real_in ** 2 + imag_in ** 2)

# Calculate the Fourier amplitude of the total field
for m in range(number_of_frequencies):
    for j in range(ja, jb + 1):
        if gaz[ic, j, kc] < 1:
            amp[m, j] = 1 / (amp_in[m]) * sqrt(real_pt[m, ic, j, kc] ** 2 + imag_pt[m, ic, j, kc] ** 2)
        
# Plot Fig. 4.7
plt.rcParams['font.size'] = 12
plt.rcParams['grid.color'] = 'gray'
plt.rcParams['grid.linestyle'] = 'dotted'
fig = plt.figure(figsize=(8, 7))

X, Y = np.meshgrid(range(je), range(ie))

compare_array = np.arange(-8.5, 10.5, step=1)
x_array = np.arange(-20, 20, step=1)

# The data here was generated with the 3D Bessel function expansion program
compare_amp = np.array(
    [[0.074, 0.070, 0.064, 0.059, 0.054, 0.049, 0.044,
    0.038, 0.033, 0.028, 0.022, 0.017, 0.012, 0.007,
    0.005, 0.007, 0.012, 0.017, 0.022],
    [0.302, 0.303, 0.301, 0.294, 0.281, 0.263, 0.238,
    0.208, 0.173, 0.135, 0.095, 0.057, 0.036, 0.056,
    0.091, 0.126, 0.156, 0.182, 0.202],
    [0.329, 0.344, 0.353, 0.346, 0.336, 0.361, 0.436,
    0.526, 0.587, 0.589, 0.524, 0.407, 0.285, 0.244,
    0.300, 0.357, 0.360, 0.304, 0.208]]
    )

def plot_amp(ax, data, compare, freq, scale):
    """Plot the Fourier transform amplitude at a specific frequency"""
    ax.plot(x_array, data, color='k', linewidth=1)
    ax.plot(compare_array, compare, 'ko', mfc='none', linewidth=1)
    plt.xlabel('cm')
    plt.ylabel('Amplitude')
    plt.xticks(np.arange(-5, 10, step=5))
    plt.xlim(-9, 9)
    plt.yticks(np.arange(0, 1, step=scale / 2))
    plt.ylim(0, scale)
    ax.text(20, 0.6, '{} MHz'.format(int(freq / 1e6)), horizontalalignment='center')
    
# Plot the results of the Fourier transform at each of the frequencies
scale = np.array((0.1, 0.5, 0.7))
for m in range(number_of_frequencies):
    ax = fig.add_subplot(3, 1, m + 1)
    plot_amp(ax, amp[m, :], compare_amp[m], freq[m], scale[m])

plt.tight_layout()
plt.show()

