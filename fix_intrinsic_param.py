#Transform Camera position from RAS coordinate system to IJK coordinate system 
pos_ras = np.array([590.943844464957, -106.39412544223035, 74.09900647300395])
pos_ijk = ras_to_ijk(pos_ras, header)

#Transform View Up from RAS coordinate system to IJK coordinate system 
view_up = np.array([0.11811973195262135, -0.03507910517365938, -0.9923795570766542, 0])
view_up_ijk = ras_to_ijk(view_up, header)
print(view_up_ijk)

#Transform Focal Point from RAS coordinate system to IJK coordinate system 
foc_point = np.array([0.0,0.0,0.0])
foc_point_ijk = ras_to_ijk(foc_point,header)
print(foc_point_ijk)

#Define intrinsic parameters by assuming negligible skew (square pixels) , distortion and brain shift phenomenom
w_pixel  = 640     #image width in pixels
h_pixel  = 480     #image height in pixels
f_mm     = 60      #focal length in mm
c_x      = 320     #principal point in pixels
c_y      = 240     #principal point  in pixels
w_sensor = 16      #sensor width in mm
h_sensor = 12      #sensor height in mm

#Convert the principal point to window center (normalized coordinate system) defined in vtkCamera
wc_x = -2*(c_x - (w_pixel)/2) / w_pixel
wc_y = -2*(c_y - (h_pixel)/2) / h_pixel

#Calculate the focal length in pixels
f_x = f_mm * (w_pixel/w_sensor)
f_y = f_mm * (h_pixel/h_sensor)

#Calculate the Angular height of the camera as ViewAngle
ViewAngle_y = 2 * atan(float(h_pixel)/(2*f_y)) * 180/pi