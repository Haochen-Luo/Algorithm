import numpy as np
import cv2
import os
import torch
import torchvision

img_h, img_w = 256, 256  # 根据自己数据集适当调整，影响不大
means = [0, 0, 0]
stdevs = [0, 0, 0]
img_list = []

imgs_path = 'E:/BaiduNetdiskDownload/NWPU-RESISC45/'
imgs_path_list = os.listdir(imgs_path)

num_imgs = 0
for data in imgs_path_list:
    data_path = os.path.join(imgs_path, data)
    data_list = os.listdir(data_path)
    #print(data)
    for pic in data_list:
        #print(pic)
        num_imgs += 1
        img = cv2.imread(os.path.join(data_path, pic))
        #print(img.shape)
        # try:
        #     img.shape
        # except:
        #     print("Can not read this image !")
        img = img.astype(np.float32) / 255.
        for i in range(3):
            means[i] += img[:, :, i].mean()
            stdevs[i] += img[:, :, i].std()

means.reverse()
stdevs.reverse()

means = np.asarray(means) / num_imgs
stdevs = np.asarray(stdevs) / num_imgs

print("normMean = {}".format(means))
print("normStd = {}".format(stdevs))
print('transforms.Normalize(normMean = {}, normStd = {})'.format(means, stdevs))

