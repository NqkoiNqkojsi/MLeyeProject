
# import the opencv library
import cv2
import FaceTest as fc
#def Is_Active():
def Stream():
    # define a video capture object
    vid = cv2.VideoCapture(0)
  
    while(True):
      
        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        # Display the resulting frame
        return fc.picture_anal(frame)
      
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()