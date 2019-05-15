def rendering(path):
    filenameSegmentation = "/home/nora/Desktop/2D-3D Fusion/Data/GBM_1484481 REGISTERED/cropped_volume_cylinder.nii"
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(filenameSegmentation)
    reader.Update()
    (xMin, xMax, yMin, yMax, zMin, zMax) = reader.GetExecutive().GetWholeExtent(reader.GetOutputInformation(0))
    (xSpacing, ySpacing, zSpacing) = reader.GetOutput().GetSpacing()
    (x0, y0, z0) = reader.GetOutput().GetOrigin()
    
    castFilter = vtk.vtkImageCast()
    castFilter.SetInputConnection(reader.GetOutputPort())
    castFilter.SetOutputScalarTypeToUnsignedShort()
    castFilter.Update()
    
    imdataBrainSeg = castFilter.GetOutput()
    #opacity and MIP are the critical transfer functions for tumor segmentation
    opacityTransferFunction = vtk.vtkPiecewiseFunction()
    opacityTransferFunction.AddPoint(0.0, 0.0)
    opacityTransferFunction.AddPoint(466, 0.58)
    opacityTransferFunction.AddPoint(905, 1.0)
    
    funcOpacityGradient = vtk.vtkPiecewiseFunction()
    funcOpacityGradient.AddPoint(0.0,   1.0)
    funcOpacityGradient.AddPoint(905.0,   1.0)

    colorTransferFunction = vtk.vtkColorTransferFunction()
    colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
    colorTransferFunction.AddRGBPoint(117.37, 0.25, 0.25, 0.25)
    colorTransferFunction.AddRGBPoint(234.83, 0.5, 0.5, 0.5)
    colorTransferFunction.AddRGBPoint(352.29, 0.75, 0.75, 0.75)
    colorTransferFunction.AddRGBPoint(467.92, 1.0, 1.0, 1.0)
    colorTransferFunction.AddRGBPoint(905, 1.0, 1.0, 1.0)

    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(colorTransferFunction)
    volumeProperty.SetScalarOpacity(opacityTransferFunction)
    volumeProperty.SetGradientOpacity(funcOpacityGradient)
    volumeProperty.ShadeOn()
    volumeProperty.SetAmbient(0.3)
    volumeProperty.SetDiffuse(0.6)
    volumeProperty.SetSpecular(0.5)
    volumeProperty.SetSpecularPower(40.0)
    volumeProperty.SetInterpolationTypeToLinear() 

    volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
    volumeMapper.SetInputConnection(reader.GetOutputPort())

    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0,0,0)
    renderer.AddVolume(volume)

    #aCamera = vtk.vtkCamera()
    #aCamera.SetWindowCenter(wc_x, wc_y)
    #aCamera.SetViewUp(view_up_ijk)
    #aCamera.SetPosition(pos_ijk)
    #aCamera.SetFocalPoint(foc_point_ijk)
    #aCamera.SetViewAngle(ViewAngle_y)

    renderWin = vtk.vtkRenderWindow()
    renderWin.SetOffScreenRendering(1)
    renderWin.AddRenderer(renderer)
    renderWin.SetSize(640,480)
    
    renderer.ResetCamera()
    renderer.GetActiveCamera().Zoom(1)
    renderer.GetActiveCamera().Roll(60)
    renderer.GetActiveCamera().Azimuth(75)
    renderer.GetActiveCamera().Elevation(-5)
    renderWin.Render()

    windowToImageFilter = vtk.vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renderWin)
    windowToImageFilter.Update()
     
    vtk_image = windowToImageFilter.GetOutput()
    width, height, _ = vtk_image.GetDimensions()
    vtk_array = vtk_image.GetPointData().GetScalars()
    components = vtk_array.GetNumberOfComponents()
    arr = vtk_to_numpy(vtk_array).reshape(height, width, components)
    arr  = arr[:,:,0]
    return arr