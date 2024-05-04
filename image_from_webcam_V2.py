import cv2

# takes an image from the webcam of the computer
# that it resizes it, save both the original and the resized images
# return the path of the resized image
def take_picture(res_width = 256, res_height = 256,
                format = ".jpg", name_img = "image_for_description",
                 button1 = " ", button2 = "\n"):
    key = cv2.waitKey(1)
    webcam = cv2.VideoCapture(0)
    while True:
        try:
            check, frame = webcam.read()
            print(check)  # prints true as long as the webcam is running
            print(frame)  # prints matrix values of each frame
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord(button1):
                cv2.imwrite(filename = name_img + "_original"+ format, img=frame)
                webcam.release()
                img_new = cv2.imread(name_img + "_original"+ format, cv2.IMREAD_GRAYSCALE)
                img_new = cv2.imshow("Captured Image", img_new)
                cv2.waitKey(1650)
                cv2.destroyAllWindows()
                print("Processing image...")
                img_ = cv2.imread(name_img + "_original"+ format, cv2.IMREAD_ANYCOLOR)

                print("Resizing image to 28x28 scale...")
                down_points = (res_width, res_height)
                img_ = cv2.resize(img_, down_points, interpolation=cv2.INTER_LINEAR)
                print("Resized...")
                img_resized = cv2.imwrite(filename=name_img + "_resized"+ format, img=img_)
                print("Image saved!")

                break
            elif key == ord(button2):
                print("Turning off camera.")
                webcam.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                break

        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break
    return name_img + "_resized"+ format
