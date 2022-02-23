# Fisheye distortion fix
## Checkerboard calibration 

This folder will contain python code to address the 'fisheye' distortion associated with FLIR Blackfly drivers. A checkerboard with equal checkers (2cm * 2cm), orientated with odd (7) and even (10) checkers in the length and width is filmed; calibration is completed posthoc. 

## To film ~ 
From ​https://docs.nvidia.com/vpi/sample_fisheye.html​
"Move the checkerboard target from one side of the camera's field of view to the other, both horizontally and vertically.
The accumulated checkerboard poses should fill the entire camera's field of view uniformly. The density of checkerboard detections should be roughly the same in all areas of the field of view.
There should be at least 30 calibration images per camera, the more the better. (video works too)
At every position, tilt the checkerboard target both horizontally and vertically up to 45 degrees, and ensure that detections are being processed.
Do this at various distances from the camera. Distances should range from where that the target covers about half of the image, down to 1/8th, but no further than that.
Mount the target on a tripod to keep it steady at each pose. This allows precise constraint detection from motion-blur free images.
Ensure that the camera lens is clean and there are no cables or other items blocking the view of the checkerboard target.
Ensure that there is at most one calibration target present in view" 
