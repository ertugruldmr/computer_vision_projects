import cv2
import mediapipe as mp
import numpy as np


class Finger_counter():

    def __init__(self, finger_coor: list = [(8, 6), (12, 10), (16, 14), (20, 18)],  thum_coor: tuple = (4, 3)) -> None:
        """It is the constructur of the object Finger_counter.

        Parameters
        ----------
        finger_coor : list, optional
            The coordinates which used to parse the ROI into areas. These areas are the expected locations of the fingers.  , by default [(8, 6), (12, 10), (16, 14), (20, 18)]
        thum_coor : tuple, optional
           Expected location of the thumb (finger) in the ROI, by default (4, 3)
        """

        # setting the image processing instances
        self.hand = mp.solutions.hands
        self.hands = self.hand.Hands()
        self.hand_draw = mp.solutions.drawing_utils

        # setting the finger coordinates
        self.finger_coor = finger_coor
        self.thum_coor = thum_coor


    def count_fingers(self, image:np.ndarray, text_center_coor:tuple=(150, 150), font:int=cv2.FONT_HERSHEY_PLAIN,  font_scale:int=12, color:tuple=(0, 0, 255), thickness:int = 12)->tuple:
        """Calculates the total  upped finger counts in the detected hand ROI.

        Parameters
        ----------
        image : np.ndarray
            Target image which will be used to process.
        text_center_coor : tuple, optional
            Colour of the text which denotes the total finger count where in the image , by default (150, 150)
        font : int, optional
            Writing font of the finger count text, by default cv2.FONT_HERSHEY_PLAIN
        font_scale : int, optional
            Writing size of the finger count text, by default 12
        color : tuple, optional
            Writing color of the finger count text, by default (0, 0, 255)
        thickness : int, optional
            Writing thickness of the finger count text , by default 12

        Returns
        -------
        tuple
            It returns the drawn image and the total finger count.
        """

        
        # Finding out the Hands in the Frame tgrouh Image Tracking
        results = self.hands.process(image)

        # finding out the finger count throug the hand landmarks
        finger_count = 0
        if results.multi_hand_landmarks:

            # finding out the land mark coordiantes
            landmarks = self._extract_landmarks(image, results)

            # Drawing the hand marks
            self._draw_landmarks(image, results, landmarks)

            # counting the fingers according to the parsed image areas
            finger_count = self._check_finger_positions(landmarks, finger_count)

        # drawing the reults into tge image
        cv2.putText(image, str(finger_count), text_center_coor, font, font_scale, color, thickness)

        return image, finger_count

    def _draw_landmarks(self, image:np.ndarray, results:type, landmarks:list, radius:int = 5, color:tuple = (0, 255, 0))->np.ndarray:
        """It draws the hand landmarks on the image.

        Parameters
        ----------
        image : np.ndarray
            Target image which will be used to draw the landmarks.
        results : type
            Source of the landmarks.
        landmarks : list
            List of lands mark coordiante
        radius : int, optional
            Radius of the circle which will be used to draw landmark points, by default 5
        color : tuple, optional
            Color of the landmark circles, by default (0, 255, 0)

        Returns
        -------
        np.ndarray
            Drawn image.
        """
        
        # drawing Hand Connections
        for hand_in_frame in results.multi_hand_landmarks:
            self.hand_draw.draw_landmarks(image, hand_in_frame, self.hand.HAND_CONNECTIONS)

        # drawing the hand land mark points as circles
        for point in landmarks:
            cv2.circle(image, point, radius, color, cv2.FILLED)
        
        return image
    
    def _check_finger_positions(self, landmarks:list, finger_count:int)->int:
        """Checks the already parsed coordinates whether a finger is exist or not. According to results it increases the finger count or not.

        Parameters
        ----------
        landmarks : list
            List of the landmark coordinates.
        finger_count : int
            Total finger count.

        Returns
        -------
        int
            Updated Total finger count.
        """

        # increase the number according to parsed image areas for fingers
        for coordinate in self.finger_coor:
            if landmarks[coordinate[0]][1] < landmarks[coordinate[1]][1]:
                finger_count += 1

        # increase the number according to parsed image areas for fingers
        if landmarks[self.thum_coor[0]][0] > landmarks[self.thum_coor[1]][0]:
            finger_count += 1

        return finger_count
    
    def _extract_landmarks(self, image:np.ndarray, results:type, referanced_hand_index:int = 0)->list:
        """Extracts the landmarks from result object.

        Parameters
        ----------
        image : np.ndarray
            Target image
        results : type
            It contains landmarks properties.   _
        referanced_hand_index : int, optional
            THe index number of the selected hand to process, by default 0

        Returns
        -------
        list
            listo the landmarks coordinates.
        """

        # finding out the land mark coordiantes
        landmarks = list()
        for landmark in results.multi_hand_landmarks[referanced_hand_index].landmark:

            # calculating the corresponding coordinates. (cate x--> width -> col_size, cate y--> height --> row _size)
            height, width, = image.shape[:2]
            cx, cy = int(landmark.x*width), int(landmark.y*height)
            landmarks.append((cx, cy))

        return landmarks