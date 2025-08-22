import cv2
import numpy as np

class Model:
    def __init__(self, prob: float):
        super().__init__()
        if prob > 1 or prob < 0:
            raise Exception(f"Impossible probability value {prob}!")
        self.prob = prob

    def _some_method(self):
        pass

    def __call__(self, path: str):
        image = cv2.imread(path)
        res_image = image.copy()
        if np.random.rand() > 0.5:
            res_image = cv2.blur(image, (10,10))
            status = 'OK'
        else:
            status = 'Fail'
        img_path = path.split('/')[0] + '/res' + path.split('/')[1]
        cv2.imwrite(img_path, res_image)
        return status, img_path
