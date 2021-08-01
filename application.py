# -*- coding: utf-8 -*-
"""application.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xRVTuO67omE7yxHBIkuRrkSdt3H6y7jK
"""

import os
import torch
import easydict
import math
import numpy as np
import matplotlib.pyplot as plt
import torch.nn.functional as F
from PIL import Image
from dataset import read_q_table
from dctbasis import load_DCT_basis_torch

from net1 import Net1
from net2 import Net2
from net3 import Net3
from net3 import Net3 


def _extract_patches(Y, patch_size, stride):
    patches=list()
    h, w = Y.shape[0:2] # height, width
    
    H = (h - patch_size) // stride
    W = (w - patch_size) // stride

    for i in range(0,H*stride, stride):
        for j in range(0,W*stride,stride):
            patch = Y[i:i+patch_size, j:j+patch_size]
            patches.append(patch)
            
    return patches, H, W
    

def localizing_double_JPEG(Y, qvectors, net):
    net.eval()
    result=0
    PATCH_SIZE = 256

    default_stride = 32
    default_batchsize = 32

    qvectors = torch.from_numpy(qvectors).float()
    qvectors = qvectors.to(device)
    qvectors = torch.unsqueeze(qvectors, axis=0)

    patches, H, W = _extract_patches(Y, patch_size=PATCH_SIZE, stride=default_stride)

    result = np.zeros((H, W))

    num_batches = math.ceil(len(patches) / default_batchsize)

    result_flatten = np.zeros((H*W))
    for i in range(num_batches):
        print('[{} / {}] Detecting...'.format(i, num_batches))

        if i==(num_batches-1): # last batch
            batch_Y = patches[i*default_batchsize:]
        else:
            batch_Y = patches[i*default_batchsize:(i+1)*default_batchsize]

        batch_size = len(batch_Y) 
        batch_Y = np.array(batch_Y)

        batch_Y = torch.unsqueeze(torch.from_numpy(batch_Y).float().to(device), axis=1)

        batch_qvectors = torch.repeat_interleave(qvectors, batch_size, dim=0)

        batch_output = net(batch_Y, batch_qvectors)
        batch_output = F.softmax(batch_output, dim=1)

        result_flatten[(i*default_batchsize):(i*default_batchsize)+batch_size] = \
                batch_output.detach().cpu().numpy()[:,0]

    result = np.reshape(result_flatten, (H, W))

    return result

    
def calculate_f1(gt_path, result_array):
  a, b = result_array.shape

  gt_img = Image.open(gt_path).convert("L")
  gt_img = gt_img.resize((b, a))
  gt_arr = np.asarray(gt_img)

  threshold = 150
  gt_thres = np.zeros((a, b)).astype('uint8')
  res_thres = np.zeros((a, b)).astype('uint8')

  for i in range(0, a):
    for j in range (0, b):
      if gt_arr[i][j] > threshold:
        gt_thres[i][j] = 255
      if result_array[i][j] > threshold:
        res_thres[i][j] = 255

  tp, fp, fn, tn = 0, 0, 0, 0

  for i in range(0, a):
    for j in range (0, b):
      if gt_thres[i][j] == 255 and res_thres[i][j] == 255:
        tp = tp+1
      elif gt_thres[i][j] == 255 and res_thres[i][j] == 0:
        fn = fn+1
      elif gt_thres[i][j] == 0 and res_thres[i][j] == 255:
        fp = fp+1
      elif gt_thres[i][j] == 0 and res_thres[i][j] == 0:
        tn = tn+1
        
  f1_score = (2*tp)/((2*tp)+fp+fn)
  accuracy = (tp+tn)/(tp+tn+fp+fn)

  return f1_score, accuracy


if __name__ == "__main__":
  global net1, net2, net3, net4
  global device

  result_dir_name = './result'
  dir_name = './images'
  model_dir_name = './model'

  #######################################
  selected_model1 = 'net1'
  selected_model2 = 'net2'
  selected_model3 = 'net3'
  selected_model4 = 'net4'

  model_pth1 = selected_model1 + '.pth'
  model_pth2 = selected_model2 + '.pth'
  model_pth3 = selected_model3 + '.pth'
  model_pth4 = selected_model4 + '.pth'
  #######################################

  model_dir_name1 = os.path.join(model_dir_name, model_pth1)
  model_dir_name2 = os.path.join(model_dir_name, model_pth2)
  model_dir_name3 = os.path.join(model_dir_name, model_pth3)
  model_dir_name4 = os.path.join(model_dir_name, model_pth4)

  args = easydict.EasyDict({ "hidden_size": 256, "output_size": 2, "seq_size": 64, "n_layers": 2})

  device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
      
  #load pre-trained weights
  net1 = Net1(160, args.hidden_size, args.output_size, device, args.n_layers)
  net2 = Net2(120, args.hidden_size, args.output_size, device, args.n_layers)
  net3 = Net3(120, args.hidden_size, args.output_size, device, args.n_layers)
  net4 = Net4(120, args.hidden_size, args.output_size, device, args.n_layers)
      
  net1.load_state_dict(torch.load(model_dir_name1))
  net2.load_state_dict(torch.load(model_dir_name2))
  net3.load_state_dict(torch.load(model_dir_name3))
  net4.load_state_dict(torch.load(model_dir_name4))

  net1.to(device)
  net2.to(device)
  net3.to(device)
  net4.to(device)

  file_name = 'splicing.jpg'
  file_path = os.path.join(dir_name, file_name)

  result_name = 'splicing-result.jpg'
  result_path = os.path.join(result_dir_name, result_name)

  im = Image.open(file_path)

  im = im.convert('YCbCr')
  Y = np.array(im)[:, :, 0]

  qvector = read_q_table(file_path).flatten()

  result1 = localizing_double_JPEG(Y, qvector, net1)
  result2 = localizing_double_JPEG(Y, qvector, net2)
  result3 = localizing_double_JPEG(Y, qvector, net3)
  result4 = localizing_double_JPEG(Y, qvector, net4)

  result_mean = (result1 + result2 + result3 + result4) / 4

  fig = plt.figure()
  columns = 2
  rows = 1
  fig.add_subplot(rows, columns, 1)
  plt.title('input')
  plt.imshow(Image.open(file_path))

  result_mean = result_mean*255
  result_mean = result_mean.astype('unit8')

  img_result = Image.fromarray(result_mean)
  img_result.convert("L")

  plt.imshow(img_result, cmap='gray', vmin=0, vmax=255)

  gt_file_name = 'splicing_gt.jpg'
  gt_path = os.path.join(dir_name, gt_file_name)
  f1, acc = calculate_f1(gt_path, result_mean)
  title = 'F1 score: ' + str(round(f1 * 100) / 100) + ', Accuracy: ' + str(round(acc * 10000) / 100)

  plt.title(title)

  plt.savefig(result_path)

  plt.show()

  print("F1 score: ", f1, "\n Accuracy: ", acc)