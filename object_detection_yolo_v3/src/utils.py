import cv2
import numpy as np


class Yolo_v3():

    def __init__(self, confThreshold: float, nmsThreshold: float, whT: int):
        #
        # asfdasf
        """Constructor for the Yolo_v3 class.

        Parameters
        ----------
        confThreshold : float
            Confidence threshold, by default 0.5
        nmsThreshold : float
            Non-maximum suppression threshold, by default 0.4
        whT : int
            Width and height threshold, spatial size for output image. Generally recomended 416
        """

        self.confThreshold = confThreshold
        self.nmsThreshold = nmsThreshold
        self.whT = whT

    def read_classes(self, class_path: str = "coco.names"):
        """Reads the class list text. Sets the object name list of the model.

        Parameters
        ----------
        class_path : str, optional
            Path of the class list of the model, by default "coco.names"
        """

        try:
            with open(class_path, 'r') as f:
                self.classes = f.read().rstrip('\n').split("\n")
        except Exception as e:
            print(f"Error: {e}, while reading class names")

    def load_model(self, model_path: str = "model/yolov3.cfg", weights_path: str = "model/yolov3.weights"):
        #
        """Loads the model and its weights. Sets the model and the weights.

        Parameters
        ----------
        model_path : str, optional
           Path of the Deep learning model structure, by default "model/yolov3.cfg"
        weights_path : str, optional
           Path of the weights of the model, by default "model/yolov3.weights"
        """

        # creating deep learning model
        model = cv2.dnn.readNet(model_path, weights_path)
        model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        # loading model
        self.model = model

    def detect_objects(self, image: np.ndarray) -> tuple:
        """Detecs the objects in the image.

        Returns
        -------
        tuple
            Detected objects properties.
        """

        # creating blob from image
        blob = cv2.dnn.blobFromImage(
            image, 1/255, (self.whT, self.whT), [0, 0, 0], 1, crop=False)

        # setting blob as input to model
        self.model.setInput(blob)

        # getting the onject class
        layers = self.model.getLayerNames()
        outputsN = [(layers[i-1])
                    for i in self.model.getUnconnectedOutLayers()]
        outputs = self.model.forward(outputsN)

        return outputs

    def extract_and_draw_objects(self, outputs: tuple, image: np.ndarray) -> np.ndarray:
        """Extracts the detected object properties and draws them on the image.

        Parameters
        ----------
        outputs : tuple
            properties of the detected objects
        image : np.ndarray
            _description_

        Returns
        -------
        np.ndarray
            Drawn image with detected objects.
        """

        # extracting the shape of the image
        height, width = image.shape[:2]

        # extracting the properties
        bbox, class_ids, confs = list(), list(), list()
        for out in outputs:
            for det in out:

                # classes starts from 5
                scores = det[5:]
                classId = np.argmax(scores)
                confindence = scores[classId]

                # save the properties if the object class can be acceptable according to confidence threshold
                if confindence > self.confThreshold:

                    # extracting the object coordinates. note when you take directly x and y it will be center point of the object
                    #w, h = int(det[2]*height), int(det[3]*width)
                    w, h = int(det[2]* width), int(det[3]* height)
                    #x, y = int((det[0]*height)-w/2), int((det[1]*width)-h/2)
                    x, y = int((det[0]*height)-h/2), int((det[1]*width-w/2))

                    # collecting the accepted properties of  the detected object
                    bbox.append([x, y, w, h])
                    class_ids.append(classId)
                    confs.append(float(confindence))

        # drawing the bounding boxes
        indexes = cv2.dnn.NMSBoxes(
            bbox, confs, self.confThreshold, self.nmsThreshold)
        for i in range(len(bbox)):
            if i in indexes:

                # unpacking the bounding box coordiantes
                x, y, w, h = bbox[i]

                # object class name corresponding to the class id
                label = str(self.classes[class_ids[i]])

                # drawing the bounding box
                cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 3)
                cv2.putText(image, label, (x, y+30),
                            cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

        return image
