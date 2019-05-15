def data_label_slicing(path):
    # Calculate the center of the volume
    filenameSegmentation = "/home/nora/Desktop/2D-3D Fusion/Data/GBM_1484481 REGISTERED/resampled_1.nii"
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(filenameSegmentation)
    reader.Update()
    (xMin, xMax, yMin, yMax, zMin, zMax) = reader.GetExecutive().GetWholeExtent(reader.GetOutputInformation(0))
    (xSpacing, ySpacing, zSpacing) = reader.GetOutput().GetSpacing()
    (x0, y0, z0) = reader.GetOutput().GetOrigin()

    #calculate the orthogonal vectors to the normal
    plane = np.array([1,0,0])
    ortho_1 = np.cross(normal,plane)
    ortho_2 = np.cross(normal,ortho_1)

    #calculate origin
    origin_up = np.array([32,65,120])  #taken where intraop 0, 2, 4 exists
    origin_down = np.array([85,65,120])  #taken where intraop 5,6,8,9 exists

    slices = origin_down[0] - origin_up[0]

    origin = np.zeros((slices,3),dtype =int)
    origin[0,0] = 32
    origin[0,1] = 65
    origin[0,2] = 120

    for i in range(0,slices-1):
        origin[i+1,0] =  origin[i,0] + 1
        origin[i+1,1] =  origin[i,1]
        origin[i+1,2] =  origin[i,2]
    
    
    # Extract a slice in the desired orientation
    reslice = vtk.vtkImageReslice()
    reslice.SetInputConnection(reader.GetOutputPort())
    reslice.SetOutputDimensionality(2)
    reslice.SetInterpolationModeToNearestNeighbor()

    # Display the label
    im_actor = vtk.vtkImageActor()
    im_actor.GetMapper().SetInputConnection(reslice.GetOutputPort())

    im_renderer = vtk.vtkRenderer()
    im_renderer.AddActor(im_actor)
    
    im_renderWin = vtk.vtkRenderWindow()
    im_renderWin.SetOffScreenRendering(1)
    im_renderWin.AddRenderer(im_renderer)
    im_renderWin.SetSize(640,480)
    im_renderer.ResetCamera()
    im_renderer.GetActiveCamera().Zoom(1)
    im_renderer.GetActiveCamera().Roll(140)

    vol = np.zeros((slices,480,640))

    for i in range(slices):
        oblique = vtk.vtkMatrix4x4()
        oblique.DeepCopy((ortho_1[0], ortho_2[0], normal[0], origin[i,0],
                      ortho_1[1], ortho_2[1], normal[1], origin[i,1],
                      ortho_1[2], ortho_2[2], normal[2], origin[i,2],
                               0,          0,         0,        1))
            
        reslice.SetResliceAxes(oblique)

        im_renderWin.Render()
    
        im_windowToImageFilter = vtk.vtkWindowToImageFilter()
        im_windowToImageFilter.SetInput(im_renderWin)
        im_windowToImageFilter.Update()
     
        im_vtk_image = im_windowToImageFilter.GetOutput()
        width, height, _ = im_vtk_image.GetDimensions()
        im_vtk_array = im_vtk_image.GetPointData().GetScalars()
        components = im_vtk_array.GetNumberOfComponents()
        arr = vtk_to_numpy(im_vtk_array).reshape(height, width, components)
        vol[i,:,:]  = arr[:,:,0]
    
    return vol