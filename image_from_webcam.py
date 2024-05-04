import cv2
from time import sleep

# takes an image from the webcam of the computer
# that it resizes it, save both the original and the resized images
# return the path of the resized image

def take_picture(res_width = 256, res_height = 256,
                 name_img = "image_for_description", format = ".jpg", 
                 button1 = " ", button2="\n"):
    key = cv2.waitKey(1)
    webcam = cv2.VideoCapture(0)
    sleep(2)
    while True:

        try:
            check, frame = webcam.read()
            print(check)  # prints true as long as the webcam is running
            print(frame)  # prints matrix values of each framecd
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord(button):
                cv2.imwrite(filename = name_img + "_original"+ format, img=frame)
                webcam.release()
                print("Processing image...")
                img_ = cv2.imread(name_img + "_original"+ format, cv2.IMREAD_ANYCOLOR)
                #print("Converting RGB image to grayscale...")
                #gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
                #print("Converted RGB image to grayscale...")
                print("Resizing image...")
                down_points = (res_width, res_height)
                img_ = cv2.resize(img_, down_points, interpolation=cv2.INTER_LINEAR)
                print("Resized...")
                img_resized = cv2.imwrite(filename= name_img + "_resized" + format, img=img_)
                print("Resize image saved!")

                break

            elif key == ord(button2):
                webcam.release()
                cv2.destroyAllWindows()
                break

        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break

    return name_img + "_resized" + format
