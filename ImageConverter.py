import cv2
import numpy as np
from PIL import Image


class ImageToCSV:
    image_num = 0
    image_directory = None
    training_data = []
    image_pixels = []
    type0 = 0
    type1 = 0
    type2 = 0
    type3 = 0
    type4 = 0

    def __init__(self, image_num, image_directory):
        self.image_num = image_num
        self.image_directory = image_directory
        self.set_training_data()

    def set_training_data(self):
        for i in range(0, self.image_num):
            self.training_data.append(self.image_directory + str(i) + ".png")

    @staticmethod
    def get_image_pixel_similarity(cmp_img, ref_img="reference/ref.png", percentage=28.8896604938):
        cvt_cmp_img = Image.open(cmp_img).convert('L') if isinstance(cmp_img, str) else cmp_img
        cvt_ref_img = Image.open(ref_img).convert('L') \
            .resize(cvt_cmp_img.size, Image.BILINEAR) if isinstance(ref_img, str) else ref_img

        cvt_cmp_img_pixels, cvt_ref_img_pixels = list(cvt_cmp_img.getdata()), list(cvt_ref_img.getdata())
        diff_all_pixel, i = 0, 0

        for pix in range(0, len(cvt_cmp_img_pixels)):
            if abs(cvt_cmp_img_pixels[pix] - cvt_ref_img_pixels[pix]) != 0:
                diff_all_pixel += 1

        all_pixels = cvt_cmp_img.size[0] * cvt_cmp_img.size[1]
        return (float(diff_all_pixel) * 10000) / (float(all_pixels) * percentage)

    def save_reduce_image_to_csv(self, filename, min_width=7, max_width=46, min_height=18, max_height=70):
        out = open(filename + '.csv', 'w')
        for a in range(0, self.image_num):
            im = Image.open(self.training_data[a]).convert('L')
            width, height = im.size[0], im.size[1]
            reduce_image = cv2.resize(np.array(im), (width / 10, height / 10))
            ret, trans_image = cv2.threshold(np.array(reduce_image), 127, 255, cv2.THRESH_BINARY)

            reduce_width, reduce_height = range(min_width, max_width), range(min_height, max_height)

            for i in reduce_height:
                for j in reduce_width:
                    if trans_image[i, j] == 255:
                        trans_image[i, j] = 1
                    self.image_pixels.append(trans_image[i, j])

            diff_percentage = self.get_image_pixel_similarity(self.training_data[a])
            print 'seq: ' + str(a) + ', diff_percentage : ' + str(diff_percentage)
            self._add_csv(a, diff_percentage, out)

        out.close()

    def _add_csv(self, a, diff_percentage, out):

        sim_per = []
        result_type = 0

        if diff_percentage < 14:
            result_type = 0
            print('type: ' + str(result_type) + '\n')
            self.type0 += 1

        elif 14 <= diff_percentage < 25:
            result_type = self._check_image_type(a, sim_per, 1)

        elif 25 <= diff_percentage < 36:
            result_type = self._check_image_type(a, sim_per, 2)

        elif 36 <= diff_percentage < 47:
            result_type = self._check_image_type(a, sim_per, 3)

        elif 47 <= diff_percentage < 58:
            result_type = self._check_image_type(a, sim_per, 4)

        elif 58 <= diff_percentage < 69:
            result_type = self._check_image_type(a, sim_per, 5)

        elif 69 <= diff_percentage < 80:
            result_type = self._check_image_type(a, sim_per, 6)

        elif 80 <= diff_percentage:
            result_type = 4
            print('type: ' + str(result_type) + '\n')
            self.type4 += 1

        out.write(str(result_type) + ",")
        for c in range(0, len(self.image_pixels)):
            out.write(str(self.image_pixels[c]) + ",")
        out.write('\n')
        self.image_pixels = []

    def _check_image_type(self, a, sim_per, folder):
        for j in range(1, 8):
            sim_per.append(
                self.get_image_pixel_similarity(
                    self.training_data[a], 'reference/' + str(folder) + '/' + str(j) + '.png'
                )
            )
            print str(a) + ": " + str(sim_per[j-1])

        if sim_per.index(min(sim_per)) >= 3:
            result_type = 3
            self.type3 += 1
            print('type: ' + str(result_type) + '\n')
            return result_type
        else:
            result_type = sim_per.index(min(sim_per))
            if result_type == 0:
                self.type1 += 1
            elif result_type == 1:
                self.type2 += 1
            print('type: ' + str(result_type + 1) + '\n')
            return result_type + 1


if __name__ == '__main__':
    pass

else:
    pass
