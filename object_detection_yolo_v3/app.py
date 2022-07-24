import os
import cv2
from datetime import datetime
from src.utils import Yolo_v3


def demonstration_camera():

    # setting the params
    confThr, nmsThr, whT = 0.5, 0.4, 320
    class_path, model_path, weights_path = "model/coco.names", "model/yolov3.cfg", "model/yolov3.weights"
    image_save_dir = "data/outputs"

    # preparing the model
    yolo_v3 = Yolo_v3(confThr, nmsThr, whT)
    yolo_v3.read_classes(class_path=class_path)
    yolo_v3.load_model(model_path=model_path, weights_path=weights_path)

    # detecting the ohjects in the camera
    cap = cv2.VideoCapture(0)
    while True:

        # reading the images from the camera
        _, image = cap.read()

        # detecting the objects
        outputs = yolo_v3.detect_objects(image)

        # drawing the ROI rectangle of the detected object
        detected_image = yolo_v3.extract_and_draw_objects(outputs, image)

        # showing the results
        cv2.imshow("Real Time Object Detection", detected_image)

        # taking the keys form keyboard
        k = cv2.waitKey(1)

        # imaage saving
        if k == ord("s"):
            current_time = datetime.now().strftime("%m-%d-%Y_%H:%M:%S")
            cv2.imwrite(os.path.join(image_save_dir,
                        f"detected_{current_time}.jpg"), detected_image)
        
        # exit condition
        if k == ord("q"):
            break

        

    # re-allocating the resources
    cap.release()
    cv2.destroyAllWindows()


def demostration_image(image_path: str = "data/inputs/dog.jpeg"):

    # setting the params
    confThr, nmsThr, whT = 0.5, 0.4, 320
    class_path, model_path, weights_path = "model/coco.names", "model/yolov3.cfg", "model/yolov3.weights"
    image_save_path = os.path.join(
        "data/outputs/", "detected_" + os.path.basename(image_path))

    # reading the example image
    try:
        image = cv2.imread(image_path)
    except Exception as e:
        print(f"Error: {e}, while reading image")

    # preparing the model
    yolo_v3 = Yolo_v3(confThr, nmsThr, whT)
    yolo_v3.read_classes(class_path=class_path)
    yolo_v3.load_model(model_path=model_path, weights_path=weights_path)

    # detecting the ohjects in the image
    outputs = yolo_v3.detect_objects(image)

    # draw the ROI of the object
    detected_image = yolo_v3.extract_and_draw_objects(outputs, image)

    # showing the image
    cv2.imshow("Object Detection From An Image", detected_image)

    # taking the keys form keyboard
    k = cv2.waitKey(0)

    # exit condition and image saving
    if k == ord("q"):
        cv2.destroyAllWindows()
    if k == ord("s"):
        cv2.imwrite(image_save_path, detected_image)


if __name__ == "__main__":
    demonstration_camera()
    demostration_image()
