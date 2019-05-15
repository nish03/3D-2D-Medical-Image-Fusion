def crop_volume(path):
    
    pBrainlabData = '/../Desktop/2D-3D Fusion/Data/2017_43/'
    iop = read_intra_op_points(pBrainlabData)
    AB = iop[4] - iop[2]
    AC = iop[8] - iop[2]       # make sure the points dont coincide or are not colinear to each other
    cross = np.cross(AB,AC)
    magnitude = np.linalg.norm(cross)
    normal = cross/magnitude     
    # define origin_up and origin_down by using reformat module of 3D SLicer
    #origin_ = np.array([66.089,5.685,29.295])
    #origin_down = np.array([23.712,17.119,26.569])

    v_down = iop - origin_down
    dist = np.zeros((9,),dtype=float)
    iop_down = np.zeros((9,3),dtype=float)
    for i in range(0, len(iop[:,0])):
        dist[i] = v_down[i,0]*normal[0] + v_down[i,1]*normal[1] + v_down[i,2]*normal[2]
        iop_down[i,:] = iop[i,:] - dist[i]*normal
    
    print(iop_down)