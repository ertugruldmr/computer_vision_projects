import cv2
from src.utils import Tracker

def demostration():
    """It is the demostration of the project. The project aims to select an object trough a GUI then track it.
    """

    # creating instances
    cap=cv2.VideoCapture(0)

    # taking an image for selecting the object
    _ , image=cap.read()

    # creating an initializing instance of Tracker 
    tracker = Tracker(ref_img = image)

    # tracking the object through the video
    naming_index = 0
    while True:

        # capturing the image frame by frame
        _, image =cap.read()
        
        # tracking the object and drawing the bounding box
        image = tracker.draw_bbox(image)
        
        # displaying the image
        cv2.imshow("img",image)

        # taking the key input from keyboard
        k = cv2.waitKey(1)
       
        # exit condition
        if k == ord("q"):
            break

        # image save
        if k == ord("s"):
            cv2.imwrite(f"tracking_{naming_index}.jpg",image)
            naming_index+=1
            

    # re-allocating the sources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    demostration()