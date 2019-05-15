# 3D-2D-Medical-Image-Registration

Step 1) Define the normal vector based on the intraoperative points. (Manual step: No)

Step 2) Extract cropped  MRI volume based on intraoperative points at the surface slice with origin O1 and corresponding points at bottom slice with certain depth 'd' and origin O2. (Manual Step: Yes)

Step 3) Fix the intrinsic parameters of the thermal camera obtained from calibration results. (Manual Step: No)

Step 4) Fix the extrinsic parameters of the thermal camera based on the landmark features of the thermal/RGB images. (Manual Step: Yes)

Step 5) Extract the MRI data slices by running data_volume_slicing.py and save as .h5 file. (Manual Step: No)

Step 6) Extract the MRI tumor label slices by running data_label_slices.py and save as .h5 file. (Manual Step: No)
