def main():
    filenameImage = "/.../Desktop/2D-3D Fusion/Data/2017_43/cropped_cylinder_volume_new1.nii"
    Imagereader = vtk.vtkNIFTIImageReader()
    Imagereader.SetFileName(filenameImage)
    castFilter = vtk.vtkImageCast()
    castFilter.SetInputConnection(Imagereader.GetOutputPort())
    castFilter.SetOutputScalarTypeToUnsignedShort()
    castFilter.Update()
    imageData = castFilter.GetOutput()

    filenamePoly = "/.../Desktop/2D-3D Fusion/Data/2017_43/cropped_cylinder_volume_new1.vtk"
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(filenamePoly)
    reader.ReadAllVectorsOn()
    reader.ReadAllScalarsOn()
    reader.Update()
    PolyDataMapper = vtk.vtkPolyDataMapper()
    PolyDataMapper.SetInputConnection(reader.GetOutputPort())
 
    #create a plane to cut,here it cuts in the XZ direction 
    plane = vtk.vtkPlane()
    plane.SetOrigin(49.075,10.772,-1.071) #these values could be taken straight from ras becasue mesh object doesnt perform the transformationrm trans
    plane.SetNormal(-0.957,0.286,-0.057)  # but nii and nrrd perfrom this transformation therefore we need to do ras to ijk transformation of points before feeding them into python code
  
    #create cutter
    cutter = vtk.vtkCutter()
    cutter.SetCutFunction(plane)
    cutter.SetInputConnection(reader.GetOutputPort())
    cutter.Update()
 
    cutStrips = vtk.vtkStripper()  #Forms loops (closed polylines) from cutter
    cutStrips.SetInputConnection(cutter.GetOutputPort())
    cutStrips.Update()
    cutPoly = vtk.vtkPolyData()    #This trick defines polygons as polyline loop
    cutPoly.SetPoints((cutStrips.GetOutput()).GetPoints())
    cutPoly.SetPolys((cutStrips.GetOutput()).GetLines())
    
    scalars = vtk.vtkDoubleArray()
    scalars.SetName("Scalars")
    
    #perform the interpolation for every point in the poly 
    for i in range(cutPoly.GetNumberOfPoints()):
        pt = [0,0,0]
        cutPoly.GetPoint(i, pt)
        scalars.InsertTuple1(i, trilinearSamplePoint(imageData, pt[0], pt[1], pt[2], 1, 0))
        
    #Add the scalar data to the poly data 
    cutPoly.GetPointData().AddArray(scalars); 
    cutPoly.GetPointData().SetActiveScalars("Scalars")

    cutMapper = vtk.vtkPolyDataMapper()
    cutMapper.SetInputData(cutPoly)
    cutMapper.ScalarVisibilityOn()
    
    cutActor = vtk.vtkActor()
    #cutActor.GetProperty().SetColor(0, 0, 1)
    #cutActor.GetProperty().SetEdgeColor(0, 1, 0)
 
    #cutActor.GetProperty().SetLineWidth(2)
    #cutActor.GetProperty().EdgeVisibilityOff()
    #cutActor.GetProperty().SetOpacity(1)
    cutActor.SetMapper(cutMapper)
 
    #create renderers and add actors of plane and cube
    ren = vtk.vtkRenderer()
    ren.AddActor(cutActor)
 
    #Add renderer to renderwindow and render
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(640, 480)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    #ren.SetBackground(1, 1, 1)
    renWin.Render()
    iren.Start()
    
if __name__ == '__main__':
    main()