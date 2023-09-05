# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 16:37:52 2023
Split large multiplex images into patches using patchify
@author: arojhada
"""

#Import modules
import numpy as np
from matplotlib import pyplot as plt
from patchify import patchify
import tifffile as tiff
from PIL import Image, ImageOps


## Read images
large_image_stack = tiff.imread('/Users/arojhada/downloads/7.ome.tif')
large_mask_stack = tiff.imread('/Users/arojhada/downloads/cell.tif')

large_image_stack.shape
large_mask_stack.shape

## 3d padding
##Padding the image to desired shape
channel_number, old_image_height, old_image_width = large_image_stack.shape

# create new image of desired size and color (blue) for padding
new_image_width = 15360
new_image_height = 15360
#padded_img = np.zeros((channel_number, new_image_height,new_image_width), dtype=np.uint16)
padded_img = np.zeros((channel_number, new_image_height,new_image_width))
padded_img.shape

# compute center offset
x_center = (new_image_width - old_image_width) // 2
y_center = (new_image_height - old_image_height) // 2

channel_number

for img in range(channel_number - 1 ):    
    padded_img[img, y_center:y_center+old_image_height, 
        x_center:x_center+old_image_width] = large_image_stack[img,:,:]

padded_img.shape

##End of padding

#To extract patches as image stacks for all channels
patches = patchify(padded_img, (34,2048,2048), step = 2048)
patches.shape

for i in range(patches.shape[1]):
        for j in range(patches.shape[2]):
            
            single_patch_stack = patches[0,i,j]
            tiff.imwrite('/Users/arojhada/downloads/07_patches/' + 'image_' + str(i)+str(j)+ ".tif", single_patch_stack)


## To extract a desiered patch
patches = patchify(large_image_stack, (34,2048,2048), step = 2048)
patches.shape
single_patch_stack = patches[0,5,3]
single_patch_stack.shape
tiff.imwrite('/Users/arojhada/downloads/patch_1_1.tif',single_patch_stack)


##To extract patches as individual images for each channel 
for img in range(large_image_stack.shape[0]):

    large_image = large_image_stack[img]
    
    patches_img = patchify(large_image, (1024, 1024), step=1024)  #Step=256 for 256 patches means no overlap
    
    for i in range(patches_img.shape[0]):
        for j in range(patches_img.shape[1]):
            
            single_patch_img = patches_img[i,j,:,:]
            tiff.imwrite('/Users/arojhada/downloads/07_patches/' + 'image_' + str(img) + '_' + str(i)+str(j)+ ".tif", single_patch_img)
            

for msk in range(large_mask_stack.shape[0]):
     
    large_mask = large_mask_stack[msk]
    
    patches_mask = patchify(large_mask, (256, 256), step=256)  #Step=256 for 256 patches means no overlap
    

    for i in range(patches_mask.shape[0]):
        for j in range(patches_mask.shape[1]):
            
            single_patch_mask = patches_mask[i,j,:,:]
            tiff.imwrite('patches/masks/' + 'mask_' + str(msk) + '_' + str(i)+str(j)+ ".tif", single_patch_mask)
            single_patch_mask = single_patch_mask / 255.


##2D patching

##Padding the image to desired shape
old_image_height, old_image_width = large_mask_stack.shape

# create new image of desired size and color (blue) for padding
new_image_width = 15360
new_image_height = 15360
#padded_img = np.zeros((channel_number, new_image_height,new_image_width), dtype=np.uint16)
padded_img = np.zeros(( new_image_height,new_image_width))
padded_img.shape

# compute center offset
x_center = (new_image_width - old_image_width) // 2
y_center = (new_image_height - old_image_height) // 2


padded_img[ y_center:y_center+old_image_height, 
        x_center:x_center+old_image_width] = large_mask_stack

padded_img.shape

##End of padding

#To extract patches as image stacks for all channels
patches = patchify(padded_img, (2048,2048), step = 2048)
patches.shape

for i in range(patches.shape[0]):
        for j in range(patches.shape[1]):
            
            single_patch_stack = patches[0,i,j]
            tiff.imwrite('/Users/arojhada/downloads/07_mask_patches/' + 'image_' + str(i)+str(j)+ ".tif", single_patch_stack)
