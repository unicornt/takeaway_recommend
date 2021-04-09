from PIL import Image
import matplotlib.pyplot as plt
def download_pic():
    im=Image.open('upload/1111111/1111111_picture.jpg')
    print(im)
    plt.imshow(im)
    plt.show()

download_pic()