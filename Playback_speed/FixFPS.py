#import cv2 library 
import cv2

#find out the resulting frame rate (varies per file) 
def read_frame_number(video):    
    cap = cv2.VideoCapture(video)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print( length )
    cap.release()
    cv2.destroyAllWindows()
    
read_frame_number(r'C:\Users\BMLab21\Desktop\jwasp1.avi')
    
def write_videos(video, file_path, frame_rate):   
    cap = cv2.VideoCapture(video)
    
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
   
    size = (frame_width, frame_height)

    result = cv2.VideoWriter(file_path, 
                             cv2.VideoWriter_fourcc(*'MJPG'), # fourcc is how openCV finds the codec # MJPG is the codec
                             30, size)
    while(True):
        ret, frame = cap.read()
        if ret == True:
            result.write(frame)
            cv2.imshow('frame',frame)
        else:
            break

    cap.release()
    result.release()
    cv2.destroyAllWindows()
    
#rewrite videos to the designated acquired frame rate (in SpinView, this varies per file) 
write_videos(r'C:\Users\BMLab21\Desktop\jwasp0.avi', r'C:\Users\BMLab21\Desktop\jwasp0_120.avi', 120)
