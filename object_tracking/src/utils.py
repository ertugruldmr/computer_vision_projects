import cv2
import numpy as np

class Tracker():

    def __init__(self, ref_img:np.ndarray) -> None:
        """It creates object tracking instance. 
        Then takes the bounding box of the object through GUI and initializes the tracker.

        Parameters
        ----------
        ref_img : np.ndarray
            Target image for object tracking.
        """

        self.ref_img = ref_img
        
        # creating tracker instance 
        self.tracker = cv2.legacy.TrackerMedianFlow_create()

        # selecting the object through GUI
        self.bbox=cv2.selectROI("Object Select Window", self.ref_img, False)

        # initializing the tracker
        self.tracker.init(self.ref_img, self.bbox)
        
    def draw_bbox(self, image:np.ndarray) -> np.ndarray:
        """It refreshes the object bounding box on the image. Then draws the bounding box on the image.

        Parameters
        ----------
        image : np.ndarray
            Target image which will be used update and draw the bounding box.

        Returns
        -------
        np.ndarray
            Drawn image with bounding box.
        """

        # refresh the object bounding box
        success, bbox=self.tracker.update(image)
        
        # defining the drawing params
        green, red = (0, 255, 0), (0, 0, 255)
        font, font_scale, thickness =cv2.FONT_HERSHEY_SIMPLEX, 0.9, 3
        writing_coor = (40,50)
        
        # setting the rectangle coordinates from boinding box coordinates
        (x,y,w,h) = bbox
        start, stop =  (int(x),int(y)), (int(x)+int(w),int(y)+int(h))

        # drawing the bounding box on the image
        if success:
            cv2.putText(image,"Tracking",writing_coor,font, font_scale, green,thickness)
            cv2.rectangle(image, start, stop, red ,thickness)
        else:
            cv2.putText(image,"Lost", writing_coor, font, font_scale, red,thickness)
        
        return image