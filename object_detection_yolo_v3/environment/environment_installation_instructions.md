# Environment Installation Options

## Manuel 
open command line with our determinated  and type

- opencv-contrib 

        pip install opencv-contrib-python

- numpy 

        pip install numpy

- yolov3.weights with linux command
	
	
       ! wget "https://pjreddie.com/media/files/yolov3.weights"
	
       mv yolov3.weights model/


- yolov3.weights manuel
       - go https://pjreddie.com/media/files/yolov3.weights website and download the file.
       - move the file to "object_detection_yolo_v3/model" folder.

## Using pip requirements.txt file
open command line in the project folder (working directory = 'object_detection_yolo_v3') with your determinated virtual environment and type following code.

       pip install -r environment/requirements.txt 

## Using conda environment.yml file
- Go to the project folder (working directory = 'object_detection_yolo_v3')
- set the virtual environment path  through changing change the last row from <your_user_name> to user_name such as 
__'/home/ertugrul/anaconda3/envs/object_detection_yolo_v3-env'__ . ertugrul is the user name of my computer.
- then type following code

       conda env create -f environment/environment.yml
- Don't forget to activate the environment before run the project
       
       conda activate object_detection_yolo_v3-env
- Note that, this environment settted accrding to debian linux distribution.
