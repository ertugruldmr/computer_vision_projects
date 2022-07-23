import os
import cv2
from datetime import datetime

from src.utils import Car_labeller 

def demostration():
    """Aims the demostrate the Opencv Image Processing and High Level GUI functions usage through example project.
    """

    # defining test image
    image_name = "carpark.jpg"
    image_pah = os.path.join("data/input", image_name)
    IMAGE = cv2.imread(image_pah)

    image_save_path = "data/output"

    # defining the style params
    font = cv2.FONT_HERSHEY_SIMPLEX

    # creating an instance of the car labeller class to use GUI interaction
    car_labeller = Car_labeller(IMAGE = IMAGE, font=font)

    # defining the window name for reference the gui window
    win_name = "Labeller"

    # creating a window to display the image
    while True:

        # Creating GUI  window for displating and interacting with the image
        cv2.namedWindow(win_name)

        # Getting the Mouse Events from the GUI window
        cv2.setMouseCallback(win_name, car_labeller.search_window)

        # Updating the Counter Displayer where in the image top-left side
        cv2.rectangle(car_labeller.IMAGE, (0, 0), (70, 80), (255, 255, 255), -1)
        cv2.putText(car_labeller.IMAGE, f'{car_labeller.full_count}', (5, 30), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(car_labeller.IMAGE, f'{car_labeller.empty_count}', (5, 70), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # displating the image
        cv2.imshow(win_name, car_labeller.IMAGE)
        
        # saving the image when the user press the s button on the keyboard
        if cv2.waitKey(1) & 0xFF == ord('s'):
            current_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            cv2.imwrite(os.path.join(image_save_path, f"{current_time}_{image_name}"   ), car_labeller.IMAGE)

        # closing the window when user press the esc button on the keyboard
        if cv2.waitKey(1) & 0xFF == 27:
            break
        
    # re-allocating the sources
    cv2.destroyAllWindows()


if __name__ == '__main__':
    demostration()
    
