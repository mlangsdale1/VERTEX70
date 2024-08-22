def calc_f_hole(R, r):
    """
    r: radius of hole
    R: radius of sphere
    
    Calculate the ratio of surface area of hole to surface area of sphere
    """
    import numpy as np
    h = R - (R**2 - r**2)**(0.5)
    a = 2 * np.pi * R * h
    sas = 4*np.pi * R**2        # surface area of sphere
    f = a/sas
    
    return f

def calc_sphere_corr(Q, Qp):
    '''
    Q:  cap on
    Qp: cap off
    '''
    
    # define constants
    R = 150/2       # radius of sphere
    r_e = 30/2      # radius of entrance port
    # r_d = 5/2       # radius of detector port - nb two of these
    r_s = 30/2      # radius of sample port
    
    # calculate fj for each of holes (ratio of area to area of sphere)
    fe = calc_f_hole(R,r_e)
    fs = calc_f_hole(R, r_s)    # called fm in Goebel 1967
    # fd = 2*calc_f_hole(R, r_d)  #   two of these
    fc = fs                     # ratio for removable cap
    
#    # Constants from the notes 
#    A = 1-fe-fd-fs
#    B = fs
#    G = 1-fe-fd
    
    # the Q factor
    fm=fs
    #rho_w = Q - Qp/((Q-Qp)*(1-fe-fs) + Qp*fc)
    deno = Q*(1-fe-fm) - Qp*(1-fe-fm-fc)        # replacing fc for fd
    rho_w_close = (Q-Qp)/deno      # \rho_w - here is the error in Goebels 1967
    
    return rho_w_close

def raw2emi(v_samp, v_ref, v_op,use_subCorr = True):
    """
    Inputs:
        v_samp:         raw sample data (np array)
        v_ref:          raw gold panel data (np array)
        v_op:           raw open port data (np array)
        use_subCorr:    Apply substitution correction from Goebel 1967 (boolean)

    Output: 
        emissivity array calculated using Kirchhoff's law
    """
    if use_subCorr:
        rho_ref = calc_sphere_corr(v_ref, v_op)
    else:
        rho_ref = 0.98
    
    rho_samp = rho_ref*(v_samp -v_op)/(v_ref - v_op)

    return 1 - rho_samp
