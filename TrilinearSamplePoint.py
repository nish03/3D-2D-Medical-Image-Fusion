def calcIndex(x, y, z, width, height):
    ind = x + width * (y + height * z)
    return ind
    
def trilinearSamplePoint(imageData, x, y, z, numComps, comp):
    tuples = imageData.GetPointData().GetNumberOfTuples()
    im_scalars = imageData.GetPointData().GetScalars()
    scalar_arr = vtk_to_numpy(im_scalars)
    #spacing = imageData.GetSpacing()
    spacing = np.array([0.999999, 1, 1])
    #origin = imageData.GetOrigin()
    origin = np.array([-96.8419,-65.001,-144.546])
    dim = imageData.GetDimensions()
    
    #We assume the point x, y, z is in the image 
    xi = int(np.around((x - origin[0]) / spacing[0]))
    yi = int(np.around((y - origin[1]) / spacing[1]))
    zi = int(np.around((z - origin[2]) / spacing[2]))
    
    #Get the intensities at the 8 nearest neighbors
    i000 = scalar_arr[calcIndex(xi, yi, zi, dim[0], dim[1]) * numComps + comp]
    i100 = scalar_arr[calcIndex(xi + 1, yi, zi, dim[0], dim[1]) * numComps + comp]
    i110 = scalar_arr[calcIndex(xi + 1, yi + 1, zi, dim[0], dim[1] * numComps + comp)]
    i010 = scalar_arr[calcIndex(xi, yi + 1, zi, dim[0], dim[1]) * numComps + comp]
    i001 = scalar_arr[calcIndex(xi, yi, zi + 1, dim[0], dim[1]) * numComps + comp]
    i101 = scalar_arr[calcIndex(xi + 1, yi, zi + 1, dim[0], dim[1]) * numComps + comp]
    i111 = scalar_arr[calcIndex(xi + 1, yi + 1, zi + 1, dim[0], dim[1]) * numComps + comp]
    i011 = scalar_arr[calcIndex(xi, yi + 1, zi + 1, dim[0], dim[1]) * numComps + comp]
    
    #Get the fractional/unit distance from the nearest neighbor
    rx = xi * spacing[0] + origin[0]  #position of the node
    rx = (x - rx) / spacing[0]        #(Node- actual point position)/ voxel width
    ry = yi * spacing[1] + origin[1]
    ry = (y - ry) / spacing[1]
    rz = zi * spacing[2] + origin[2]
    rz = (z - rz) / spacing[2]
    
    #start performing trilinear interpolation
    ax = i000 + (i100 - i000) * rx
    bx = i010 + (i110 - i010) * rx
    cy = ax + (bx - ax) * ry
    dx = i001 + (i101 - i001) * rx
    ex = i011 + (i111 - i011) * rx
    fy = dx + (ex - dx) * ry
    gz = cy + (fy - cy) * rz
    return gz
