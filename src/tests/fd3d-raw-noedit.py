from collections import namedtuple
from math import exp, sqrt, cos, sin
import numba
from numba.experimental import jitclass
import numpy as np
from matplotlib import pyplot as plt


def main(nsteps, num_freq, freq, dims):
    c = set_constants(freq)
    real_in, imag_in, real_pt, imag_pt, amp, e, i, d, id, h, ih, hx_inc, ez_inc = generate_initial_arrays(dims, num_freq)
    pml = calculate_pml_params(dims, npml=8)
    ga, gb = create_sphere(c, dims)
    real_in, imag_in, num_freq, real_pt, imag_pt = \
    main_fdtd_loop(nsteps, c, dims, ez_inc, num_freq,
    real_in, imag_in,
    d, h, pml, e, i, ih, id, ga, gb, hx_inc, real_pt,
    imag_pt)
    amp = calculate_fourier_amplitude(dims, real_in, imag_in, ga,
    num_freq, amp, real_pt,
    imag_pt)
    plot_fig_4_7(amp, num_freq, freq)
    
    
# the @numba.jitclass decorator allows us to pass our custom
# class into a `numba.jit`ed function
@jitclass([
    ('x', numba.float32[:, :, :]),
    ('y', numba.float32[:, :, :]),
    ('z', numba.float32[:, :, :])
])
class Field:
    """ This class creates a field in three directions.
    Attributes:
    x: Field strength in the x-direction
    y: Field strength in the y-direction
    z: Field strength in the z-direction
    """
    def __init__(self, x_cells, y_cells, z_cells, initial_value):
        """ Return a Field object with an *x*, *y*, and
        *z* component"""
        self.x = np.ones((x_cells, y_cells, z_cells),
        dtype=np.float32) * initial_value
        self.y = np.ones((x_cells, y_cells, z_cells),
        dtype=np.float32) * initial_value
        self.z = np.ones((x_cells, y_cells, z_cells),
        dtype=np.float32) * initial_value
        
@jitclass([
    ('x', numba.int16),
    ('y', numba.int16),
    ('z', numba.int16),
    ('x_center', numba.int16),
    ('y_center', numba.int16),
    ('z_center', numba.int16),
    ('xa', numba.int16),
    ('ya', numba.int16),
    ('za', numba.int16),
    ('xb', numba.int16),
    ('yb', numba.int16),
    ('zb', numba.int16)
    ])
class Dimensions:
    """ This class keeps track of the problem space in
    three directions.
    Attributes:
    x: Number of cells in the x-direction
    y: Number of cells in the y-direction
    z: Number of cells in the z-direction
    x_center: Index for the center cell in the x-direction
    y_center: Index for the center cell in the y-direction
    z_center: Index for the center cell in the z-direction
    xa: Scattered/total field lower boundary in the x-direction
    ya: Scattered/total field lower boundary in the y-direction
    za: Scattered/total field lower boundary in the z-direction
    xb: Scattered/total field upper boundary in the x-direction
    yb: Scattered/total field upper boundary in the y-direction
    zb: Scattered/total field upper boundary in the z-direction
    """
    def __init__(self, x, y, z, xa, ya, za):
        self.x = x
        self.y = y
        self.z = z
        self.x_center = int(self.x / 2)
        self.y_center = int(self.y / 2)
        self.z_center = int(self.z / 2)
        self.xa = xa
        self.ya = ya
        self.za = za
        self.xb = self.x - self.xa - 1
        self.yb = self.y - self.ya - 1
        self.zb = self.z - self.za - 1
        
Constants = namedtuple('Constants', (
    'ddx', 'dt', 'arg',
    't0', 'spread'
    ))

PerfectlyMatchedLayer = namedtuple('PerfectlyMatchedLayer', (
    'fi1', 'fi2', 'fi3',
    'fj1', 'fj2', 'fj3',
    'fk1', 'fk2', 'fk3',
    'gi1', 'gi2', 'gi3',
    'gj1', 'gj2', 'gj3',
    'gk1', 'gk2', 'gk3',
    ))

def set_constants(freq):
    """ Set up constants that do not change for the
    entire simulation"""
    ddx = 0.01 # Cell size
    dt = ddx / 6e8 # Time step size
    arg = 2 * np.pi * freq * dt
    # Pulse Parameters
    t0 = 20
    spread = 8
    c = Constants(
    ddx, dt, arg,
    t0, spread
    )
    return c

def generate_initial_arrays(dims, num_freq):
    """Generate the arrays that will be used in the program"""
    real_in = np.zeros(num_freq)
    imag_in = np.zeros(num_freq)
    real_pt = np.zeros((num_freq, dims.x, dims.y, dims.z))
    imag_pt = np.zeros((num_freq, dims.x, dims.y, dims.z))
    amp = np.zeros((num_freq, dims.y))
    # Generate the initial field objects
    e = Field(dims.x, dims.y, dims.z, 0)
    i = Field(dims.x, dims.y, dims.z, 0)
    d = Field(dims.x, dims.y, dims.z, 0)
    id = Field(dims.x, dims.y, dims.z, 0)
    h = Field(dims.x, dims.y, dims.z, 0)
    ih = Field(dims.x, dims.y, dims.z, 0)
    hx_inc = np.zeros(dims.y)
    ez_inc = np.zeros(dims.y)
    return real_in, imag_in, real_pt, imag_pt, amp, e, i, d, id, h, ih, hx_inc, ez_inc

def calculate_pml_params(dims, npml):
    """ Creates the Perfectly Matched Layer object """
    fi1, gi2, gi3 = calculate_pml_slice(dims.x, 0, npml)
    fj1, gj2, gj3 = calculate_pml_slice(dims.y, 0, npml)
    fk1, gk2, gk3 = calculate_pml_slice(dims.z, 0, npml)
    gi1, fi2, fi3 = calculate_pml_slice(dims.x, 0.5, npml)
    gj1, fj2, fj3 = calculate_pml_slice(dims.y, 0.5, npml)
    gk1, fk2, fk3 = calculate_pml_slice(dims.z, 0.5, npml)
    pml = PerfectlyMatchedLayer(
    fi1=fi1, fi2=fi2, fi3=fi3,
    fj1=fj1, fj2=fj2, fj3=fj3,
    fk1=fk1, fk2=fk2, fk3=fk3,
    gi1=gi1, gi2=gi2, gi3=gi3,
    gj1=gj1, gj2=gj2, gj3=gj3,
    gk1=gk1, gk2=gk2, gk3=gk3,
    )
    return pml

def calculate_pml_slice(size, offset, pml_cells):
    """ This initializes arrays and calculates a slice of
    the PML parameters
    (three of the parameters along one direction that use
    the same offset).
    fx1, gx2, gx3: offset = 0
    gx1, fx2, fx3: offset = 0.5 """
    distance = np.arange(pml_cells, 0, -1)
    xxn = (distance - offset) / pml_cells
    xn = 0.33 * (xxn ** 3)
    p1 = np.zeros(size)
    p2 = np.ones(size)
    p3 = np.ones(size)
    p1[:pml_cells] = xn
    p1[size - pml_cells: size] = np.flip(xn, 0)
    p2[:pml_cells] = 1 / (1 + xn)
    p2[size - pml_cells: size] = 1 / (1 + np.flip(xn, 0))
    p3[:pml_cells] = (1 - xn) / (1 + xn)
    p3[size - pml_cells: size] = \
    (1 - np.flip(xn, 0)) / (1 + np.flip(xn, 0))
    return p1, p2, p3

def create_sphere(c, dims):
    """ Specify the parameters of the sphere, then
    generate the sphere """
    epsz = 8.854e-12
    # Specify sphere parameters
    epsilon = np.ones(2)
    sigma = np.zeros(2)
    epsilon[1] = 30
    sigma[1] = 0.3
    radius = 10
    # Generate Field objects
    ga = Field(dims.x, dims.y, dims.z, 1)
    gb = Field(dims.x, dims.y, dims.z, 0)
    # Generate the sphere
    ga.x, gb.x = create_sphere_single_direction(c, dims,
    0.5, 0, 0, epsilon, sigma, radius, ga.x, gb.x, epsz)
    ga.y, gb.y = create_sphere_single_direction(c, dims,
    0, 0.5, 0, epsilon, sigma, radius, ga.y, gb.y, epsz)
    ga.z, gb.z = create_sphere_single_direction(c, dims,
    0, 0, 0.5, epsilon, sigma, radius, ga.z, gb.z, epsz)
    return ga, gb

def create_sphere_single_direction(c, dims, offset_x, offset_y, offset_z, epsilon, sigma, radius, ga, gb, epsz):
    """ Create the sphere in one direction (i.e. x, y, or
    z direction) """
    for x in range(dims.xa, dims.xb + 1):
        for y in range(dims.ya, dims.yb + 1):
            for z in range(dims.za, dims.zb + 1):
                eps = epsilon[0]
                cond = sigma[0]
                xdist = dims.x_center - x - offset_x
                ydist = dims.y_center - y - offset_y
                zdist = dims.z_center - z - offset_z
                dist = sqrt(xdist ** 2 + ydist ** 2 + zdist ** 2)
                if dist <= radius:
                    eps = epsilon[1]
                    cond = sigma[1]
                ga[x, y, z] = 1 / (eps + (cond * c.dt / epsz))
                gb[x, y, z] = cond * c.dt / epsz
    return ga, gb

def main_fdtd_loop(nsteps, c, dims, ez_inc, num_freq, real_in, imag_in, d, h, pml, e, i, ih, id, ga, gb, hx_inc, real_pt, imag_pt):
    # Absorbing Boundary Conditions for the Plane Wave
    boundary_low = [0, 0]
    boundary_high = [0, 0]
    for time_step in range(1, nsteps + 1):
        ez_inc = calculate_incident_buffer(ez_inc, hx_inc, dims.y)
        real_in, imag_in = \
            fourier_transform_inc_field(real_in, imag_in, num_freq,
                                        time_step, dims.ya, ez_inc,
                                        c.arg)
        ez_inc, boundary_high, boundary_low = \
            absorbing_bound_cond(ez_inc, boundary_high,
                                boundary_low, dims.y)
        d.x, id.x = calculate_dx_field(dims, d.x, id.x, h, pml)
        d.y, id.y = calculate_dy_field(dims, d.y, id.y, h, pml)
        d.z, id.z = calculate_dz_field(dims, d.z, id.z, h, pml)
        ez_inc[3] = add_source_in_gap(time_step, c.t0, c.spread)
        d.y = calculate_inc_dy_field(dims, d.y, hx_inc)
        d.z = calculate_inc_dz_field(dims, d.z, hx_inc)
        e, i = calculate_e_fields(dims, d, ga, gb, e, i)
        real_pt, imag_pt = calculate_fourier_transform_ex(c, dims, num_freq, real_pt, imag_pt, e.z, time_step)
        hx_inc = calculate_hx_inc(dims.y, hx_inc, ez_inc)
        h.x, ih.x = calculate_hx_field(dims, h.x, ih.x, e, pml)
        h.x = calculate_hx_with_incident_field(dims, h.x, ez_inc)
        h.y, ih.y = calculate_hy_field(dims, h.y, ih.y, e, pml)
        h.y = calculate_hy_with_incident_field(dims, h.y, ez_inc)
        h.z, ih.z = calculate_hz_field(dims, h.z, ih.z, e, pml)
    return real_in, imag_in, num_freq, real_pt, imag_pt

def calculate_incident_buffer(ez_inc, hx_inc, dims_y):
    """ Calculate Ez using the incident fields """
    for y in range(1, dims_y - 1):
        ez_inc[y] = ez_inc[y] + 0.5 * (hx_inc[y - 1] - hx_inc[y])
        
    return ez_inc
    
def fourier_transform_inc_field(real_in, imag_in, num_freq, time_step, dims_y, ez_inc, arg):
    """ Fourier transform of the incident field """
    for m in range(num_freq):
        real_in[m] = real_in[m] + cos(arg[m] * time_step) * ez_inc[dims_y - 1]
        imag_in[m] = imag_in[m] - sin(arg[m] * time_step) * ez_inc[dims_y - 1]
        
    return real_in, imag_in

def absorbing_bound_cond(ez_inc, boundary_high, boundary_low, dims_y):
    """ Absorbing Boundary Conditions for the incident array"""
    ez_inc[0] = boundary_low.pop(0)
    boundary_low.append(ez_inc[1])
    
    ez_inc[dims_y - 1] = boundary_high.pop(0)
    boundary_high.append(ez_inc[dims_y - 2])
    
    return ez_inc, boundary_high, boundary_low

@numba.jit(nopython=True)
def calculate_dx_field(dims, dx, idx, h, pml):
    """ Calculate the Dx Field.
    Implementing equation analogous to Eq. (4.6) """
    for x in range(1, dims.x):
        for y in range(1, dims.y):
            for z in range(1, dims.z):
                curl_h = (h.z[x, y, z] - h.z[x, y - 1, z] - h.y[x, y, z] + h.y[x, y, z - 1])
                idx[x, y, z] = idx[x, y, z] + curl_h
                dx[x, y, z] = pml.gj3[y] * pml.gk3[z] * dx[x, y, z] + pml.gj2[y] * pml.gk2[z] * (0.5 * curl_h + pml.gi1[x] * idx[x, y, z])
    return dx, idx

@numba.jit(nopython=True)
def calculate_dy_field(dims, dy, idy, h, pml):
    """ Calculate the Dy Field.
    Implementing equation analogous to Eq. (4.6) """
    for x in range(1, dims.x):
        for y in range(1, dims.y):
            for z in range(1, dims.z):
                curl_h = (h.x[x, y, z] - h.x[x, y, z - 1] - h.z[x, y, z] + h.z[x - 1, y, z])
                idy[x, y, z] = idy[x, y, z] + curl_h
                dy[x, y, z] = pml.gi3[x] * pml.gk3[z] * dy[x, y, z] + pml.gi2[x] * pml.gk2[z] * (0.5 * curl_h + pml.gj1[y] * idy[x, y, z])
    return dy, idy

@numba.jit(nopython=True)
def calculate_dz_field(dims, dz, idz, h, pml):
    """ Calculate the Dz Field.
    Implementing Eq. (4.6) """
    for x in range(1, dims.x):
        for y in range(1, dims.y):
            for z in range(1, dims.z):
                curl_h = (h.y[x, y, z] - h.y[x - 1, y, z] - h.x[x, y, z] + h.x[x, y - 1, z])
                idz[x, y, z] = idz[x, y, z] + curl_h
                dz[x, y, z] = pml.gi3[x] * pml.gj3[y] * dz[x, y, z] + pml.gi2[x] * pml.gj2[y] * (0.5 * curl_h + pml.gk1[z] * idz[x, y, z])
    return dz, idz

def add_source_in_gap(time_step, t0, spread):
    """Add the source at the gap to generate a pulse"""
    pulse = exp(-0.5 * ((t0 - time_step) / spread) ** 2)
    return pulse

@numba.jit(nopython=True)
def calculate_inc_dy_field(dims, dy, hx_inc):
    """ Calculate the incident Dy Field
    Implementing Eq. (4.7a) and (4.7b) """
    for x in range(dims.xa, dims.xb + 1):
        for y in range(dims.ya, dims.yb + 1):
            dy[x, y, dims.za] = dy[x, y, dims.za] - 0.5 * hx_inc[y]
            dy[x, y, dims.zb + 1] = dy[x, y, dims.zb + 1] + 0.5 * hx_inc[y]
    return dy

@numba.jit(nopython=True)
def calculate_inc_dz_field(dims, dz, hx_inc):
    """ Calculate the incident Dz Field
    Implementing equations analogous to Eq. (3.26a) and
    (3.26b) """
    for x in range(dims.xa, dims.xb + 1):
        for z in range(dims.za, dims.zb + 1):
            dz[x, dims.ya, z] = dz[x, dims.ya, z] + 0.5 * hx_inc[dims.ya - 1]
            dz[x, dims.yb, z] = dz[x, dims.yb, z] - 0.5 * hx_inc[dims.yb]
    return dz

@numba.jit(nopython=True)
def calculate_e_fields(dims, d, ga, gb, e, i):
    """ Calculate the E field from the D field
    Implementing equations analogous to Eq. (2.9b) and (2.9c) """
    for x in range(0, dims.x):
        for y in range(0, dims.y):
            for z in range(0, dims.z):
                e.x[x, y, z] = ga.x[x, y, z] * (d.x[x, y, z] - i.x[x, y, z])
                i.x[x, y, z] = i.x[x, y, z] + gb.x[x, y, z] * e.x[x, y, z]
                e.y[x, y, z] = ga.y[x, y, z] * (d.y[x, y, z] - i.y[x, y, z])
                i.y[x, y, z] = i.y[x, y, z] + gb.y[x, y, z] * e.y[x, y, z]
                e.z[x, y, z] = ga.z[x, y, z] * (d.z[x, y, z] - i.z[x, y, z])
                i.z[x, y, z] = i.z[x, y, z] + gb.z[x, y, z] * e.z[x, y, z]
    return e, i

@numba.jit(nopython=True)
def calculate_fourier_transform_ex(c, dims, number_of_frequencies, real_pt, imag_pt, ez, time_step):
    """ Calculate the Fourier transform of Ez"""
    for x in range(0, dims.x):
        for y in range(0, dims.y):
            for m in range(0, number_of_frequencies):
                real_pt[m, x, y] = real_pt[m, x, y] + cos(c.arg[m] * time_step) * ez[x, y, dims.z_center]
                imag_pt[m, x, y] = imag_pt[m, x, y] - sin(c.arg[m] * time_step) * ez[x, y, dims.z_center]
    return real_pt, imag_pt

@numba.jit(nopython=True)
def calculate_hx_field(dims, hx, ihx, e, pml):
    """ Calculate the Hx field
    Implementing equations analogous to Eq. (3.24a)-(3.24c)
    and described in Section 4.2"""
    for x in range(0, dims.x):
        for y in range(0, dims.y - 1):
            for z in range(0, dims.z - 1):
                curl_e = (e.y[x, y, z + 1] - e.y[x, y, z] - e.z[x, y + 1, z] + e.z[x, y, z])
                ihx[x, y, z] = ihx[x, y, z] + curl_e
                hx[x, y, z] = pml.fj3[y] * pml.fk3[z] * hx[x, y, z] + pml.fj2[y] * pml.fk2[z] * 0.5 * (curl_e + pml.fi1[x] * ihx[x, y, z])
    return hx, ihx

@numba.jit(nopython=True)
def calculate_hy_field(dims, hy, ihy, e, pml):
    """ Calculate the Hy field
    Implementing equations analogous to Eq. (3.24a)-(3.24c)
    and described in Section 4.2"""
    for x in range(0, dims.x - 1):
        for y in range(0, dims.y):
            for z in range(0, dims.z - 1):
                curl_e = (e.z[x + 1, y, z] - e.z[x, y, z] - e.x[x, y, z + 1] + e.x[x, y, z])
                ihy[x, y, z] = ihy[x, y, z] + curl_e
                hy[x, y, z] = pml.fi3[x] * pml.fk3[z] * hy[x, y, z] + pml.fi2[x] * pml.fk2[z] * 0.5 * (curl_e + pml.fj1[y] * ihy[x, y, z])
    return hy, ihy

@numba.jit(nopython=True)
def calculate_hz_field(dims, hz, ihz, e, pml):
    """ Calculate the Hz field
    Implementing equations analogous to Eq. (3.24a)-(3.24c)
    and described in Section 4.2"""
    for x in range(0, dims.x - 1):
        for y in range(0, dims.y - 1):
            for z in range(0, dims.z):
                curl_e = (e.x[x, y + 1, z] - e.x[x, y, z] - e.y[x + 1, y, z] + e.y[x, y, z])
                ihz[x, y, z] = ihz[x, y, z] + curl_e
                hz[x, y, z] = pml.fi3[x] * pml.fj3[y] * hz[x, y, z] + pml.fi2[x] * pml.fj2[y] * 0.5 * (curl_e + pml.fk1[z] * ihz[x, y, z])
    return hz, ihz

@numba.jit(nopython=True)
def calculate_hx_inc(dims_y, hx_inc, ez_inc):
    """ Calculate incident Hx field"""
    for y in range(0, dims_y - 1):
        hx_inc[y] = hx_inc[y] + 0.5 * (ez_inc[y] - ez_inc[y + 1])
    return hx_inc

@numba.jit(nopython=True)
def calculate_hx_with_incident_field(dims, hx, ez_inc):
    """ Calculate Hx with incident Ez
    Implementing equations analogous to Eq. (3.27a) and (3.27b) """
    for x in range(dims.xa, dims.xb + 1):
        for z in range(dims.za, dims.zb + 1):
            hx[x, dims.ya - 1, z] = hx[x, dims.ya - 1, z] + 0.5 * ez_inc[dims.ya]
            hx[x, dims.yb, z] = hx[x, dims.yb, z] - 0.5 * ez_inc[dims.yb]
    return hx

@numba.jit(nopython=True)
def calculate_hy_with_incident_field(dims, hy, ez_inc):
    """ Calculate Hy with incident Ez
    Implementing equations analogous to Eq. (3.28a) and (3.28b) """
    for y in range(dims.ya, dims.yb + 1):
        for z in range(dims.za, dims.zb + 1):
            hy[dims.xa - 1, y, z] = hy[dims.xa - 1, y, z] - 0.5 * ez_inc[y]
            hy[dims.xb, y, z] = hy[dims.xb, y, z] + 0.5 * ez_inc[y]
    return hy

def calculate_fourier_amplitude(dims, real_in, imag_in, ga, num_freq, amp, real_pt, imag_pt):
    """ Calculate the Fourier amplitude of the total field"""
    # Calculate the Fourier amplitude of the incident pulse
    amp_in = np.sqrt(real_in ** 2 + imag_in ** 2)
    # Calculate the Fourier amplitude of the total field
    for m in range(num_freq):
        for y in range(dims.ya, dims.yb + 1):
            if ga.z[dims.x_center, y, dims.z_center] < 1:
                amp[m, y] = 1 / (amp_in[m]) * sqrt(real_pt[m, dims.x_center, y, dims.z_center] ** 2 + imag_pt[m, dims.x_center, y, dims.z_center] ** 2)
    return amp

def plot_fig_4_7(amp, num_freq, freq):
    """Plot Fig. 4.7"""
    
    plt.rcParams['font.size'] = 12
    plt.rcParams['grid.color'] = 'gray'
    plt.rcParams['grid.linestyle'] = 'dotted'
    fig = plt.figure(figsize=(8, 7))
    
    compare_array = np.arange(-9, 10, step=1)
    x_array = np.arange(-20, 20, step=1)
    
    # The data here was generated with the 3D Bessel function
    # expansion program
    compare_amp = np.array(
        [[0.074, 0.070, 0.064, 0.059, 0.054, 0.049, 0.044,
        0.038, 0.033, 0.028, 0.022, 0.017, 0.012, 0.007,
        0.005, 0.007, 0.012, 0.017, 0.022],
        [0.302, 0.303, 0.301, 0.294, 0.281, 0.263, 0.238,
        0.208, 0.173, 0.135, 0.095, 0.057, 0.036, 0.056,
        0.091, 0.126, 0.156, 0.182, 0.202],
        [0.329, 0.344, 0.353, 0.346, 0.336, 0.361, 0.436,
        0.526, 0.587, 0.589, 0.524, 0.407, 0.285, 0.244,
        0.300, 0.357, 0.360, 0.304, 0.208]])
    # Plot the results of the Fourier transform at each of the frequencies
    scale = np.array((0.1, 0.5, 0.7))
    for m in range(num_freq):
        ax = fig.add_subplot(3, 1, m + 1)
        plot_amp(ax, amp[m, :], compare_amp[m], freq[m], scale[m], x_array, compare_array)
    
    save_outputs(freq, amp, compare_amp, x_array, compare_array)
    
    plt.tight_layout()
    plt.show()
    
    return

def plot_amp(ax, data, compare, freq, scale, x_array, compare_array):
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
    
def save_outputs(freq, amp, compare_amp, x_array, compare_array):
    """ Save the numpy arrays of amplitude and
    the Bessel result's amplitude """
    np.save('fdtd_amp', amp)
    np.save('bessel_amp', compare_amp)
    np.save('fdtd_x_axis', x_array)
    np.save('bessel_x_axis', compare_array)
    np.save('frequencies', freq)
    
    return

if __name__ == '__main__':
    dims = Dimensions(
        x=40, y=40, z=40,
        xa=7, ya=7, za=7
    )
    main(
        nsteps=500,
        num_freq=3,
        freq=np.array((50e6, 200e6, 500e6)),
        dims=dims
    )
    
    