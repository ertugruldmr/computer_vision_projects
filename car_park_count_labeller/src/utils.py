import numpy as np
import cv2

class Car_labeller():

    def __init__(self, IMAGE:np.ndarray, font:int=None) -> None:
        """This is the constructor of the class. 

        Parameters
        ----------
        IMAGE : np.ndarray
            It is the refernce image object which will be used to process.
        font : int, optional
            It is the font style of the writing on the referenced image, by default None
        """
        
        # variables
        self.pt_x,self. pt_y = None, None
        self.pt1_x, self.pt1_y = None, None
        self.pt2_x, self.pt2_y = None, None
        self.full_count = 0
        self.empty_count = 0
        self.line_count = 0
        self.parking_width = 46

        # style params
        self.font = cv2.FONT_HERSHEY_SIMPLEX if font is None else font

        # referance image
        self.IMAGE = IMAGE

        # defining the mıouse callback variables
        self.event = None
        self.x = None
        self.y = None
        self.flags = None

    def full_counter(self, count_size=1)->int:
        """It updates total number of the cars. It is indented to work with cv2  mouse callback functions.

        Returns
        -------
        int
            Number of the total car.
        """

        # updating per click. Assumption: this fuction will be called only when the user clicks on the right mouse button
        self.full_count += count_size

        return self.full_count


    def empty_counter(self, count_size = 1)->int:
        """It updates total number of the empty car parking locations. It is indented to work with cv2 mouse callback functions.

        Returns
        -------
        int
            Number of the total empty car parking locations.
        """
                    
        # updating per click. Assumption: this fuction will be called only when the user clicks on the right mouse button 
        self.empty_count += count_size
        
        return self.empty_count


    def line_counter(self)->int:
        """It calculates the number of car on the drawn line. It seperates the number of car according to given parking width. Assumption: The line is drawn through a cv function.

        Returns
        -------
        int
            Number of the car on the line.
        """

        # defining calculation variables
        start = np.array([self.pt1_x, self.pt1_y])
        end = np.array([self.pt2_x, self.pt2_y])

        # calculating the euclidian distnace between two mouse action which used to create the line
        euclidean_distance = np.linalg.norm(end-start)
        
        # calculating the number of car on the drawn line
        line_count = int( euclidean_distance/self.parking_width)
        
        return line_count


    def denote_car(self):
        """It updates the total number of the car through the mouse callback. Notation is right mouse button click.
        """


        # Checking whether left mouse button is clicked 
        if self.event == cv2.EVENT_LBUTTONDOWN:
            # saving the current and staring points on the image which triggered by mouse click.
            self.pt_x, self.pt_y = self.x, self.y
            self.pt1_x, self.pt1_y = self.x, self.y

        elif self.event == cv2.EVENT_LBUTTONUP:
            # saving the ending points on the image which triggered by mouse click.
            self.pt2_x, self.pt2_y = self.x, self.y

            # finding out the middle point between starting click (click down) end ending click (click up)
            ptm_x = int((self.pt2_x + self.pt1_x) / 2)
            ptm_y = int((self.pt2_y + self.pt1_y) / 2)

            # updating the total number of the parked car
            parking_spaces = self.line_counter()
            
            # checkt the click is a point or line. Depends on clicking movement while  duration of clicking
            if parking_spaces == 0:
                # update with a point click
                full_spaces = self.full_counter()
                cv2.putText(self.IMAGE, f'{full_spaces}', (self.pt_x - 15, self.pt_y + 5), self.font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            else:
                # update with a line (a series of point such as dragging while clicking) 
                cv2.line(self.IMAGE, (self.pt1_x, self.pt1_y), (self.pt2_x, self.pt2_y), (0, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(self.IMAGE, f'{parking_spaces}', (ptm_x - 15, ptm_y + 7), self.font, 1, (0, 0, 255), 2, cv2.LINE_AA)
                
                # update as corresponding space
                for i in range(parking_spaces):
                    self.full_counter()

    def denote_empty_space(self):
        """It updates the total number of the car through the mouse callback. Notation is Middle mouse button click (it also named as scroll button).
        """

        # Checking whether left middle button is clicked 
        if self.event == cv2.EVENT_MBUTTONDOWN :
            # saving the current and staring points on the image which triggered by mouse click.
            self.pt_x, self.pt_y = self.x, self.y
            self.pt1_x, self.pt1_y = self.x, self.y

        elif self.event == cv2.EVENT_MBUTTONUP:
            self.pt2_x, self.pt2_y = self.x, self.y

            # finding out the middle point between starting click (click down) end ending click (click up)
            ptm_x = int((self.pt2_x + self.pt1_x) / 2)
            ptm_y = int((self.pt2_y + self.pt1_y) / 2)

            # updating the total number of the parked car
            parking_spaces = self.line_counter()
            
            # checkt the click is a point or line. Depends on clicking movement while  duration of clicking
            if parking_spaces == 0:
                # update with a point click
                full_spaces = self.empty_counter()
                cv2.putText(self.IMAGE, f'{full_spaces}', (self.pt_x - 15, self.pt_y + 5), self.font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                # update with a line (a series of point such as dragging while clicking)
                cv2.line(self.IMAGE, (self.pt1_x, self.pt1_y), (self.pt2_x, self.pt2_y), (0, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(self.IMAGE, f'{parking_spaces}', (ptm_x - 15, ptm_y + 7), self.font, 1, (0, 255, 0), 2, cv2.LINE_AA)
                
                # update as corresponding space
                for i in range(parking_spaces):
                    self.empty_counter()


    def search_window(self, event:int, x:int, y:int, flags:int, param:None):
        """It takes the mouse callbacks then determined the determiinated process through using defined functions.
        This function is implemented according to cv2.MouseCallback callback function structure.
        
        Parameters
        ----------
        event : int
            one of the cv2.MouseEventTypes constants.
        x : _type_
            The x-coordinate of the mouse event.
        y : _type_
            The y-coordinate of the mouse event.
        flags : int
            one of the cv2.MouseEventFlags constants.
        param : None
            The optional parameter.
        """
        # updating the mouse callback variables
        self.event = event
        self.x = x
        self.y = y
        self.flags = flags
    

        # implementing the process according to the mouse callback event
        self.denote_car()
        self.denote_empty_space()