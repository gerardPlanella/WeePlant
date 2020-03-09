#!/usr/bin/env python3
import sys, traceback
import cv2
import numpy as np
import json
import os
from plantcv import plantcv as pcv

class Plant():
    __slots__ = ["debug", "output_dir", "image_path", "write_image_output", "result_path", "data", "data_ready", "write_result"]

    def __init__(self, image_path, write_image_output,result_path, write_result):
        self.debug = True
        self.output_dir = "./temp"
        self.image_path = image_path
        self.write_image_output = write_image_output
        self.result_path = result_path
        self.data_ready = False
        self.write_result = write_result
        
    def setWriteResult(self, write_result):
        self.write_result = write_result
    
    def setImagePath(self, image_path):
        self.image_path = image_path
    
    def setWriteImageOutput(self, write_image):
        self.write_image = write_image
    
    def setResultPath(self, result_path):
        self.result_path = result_path

    
    
    def calculate(self):
        pcv.params.debug = self.debug
        pcv.params.debug_outdir = self.output_dir

        img, path, filename = pcv.readimage(filename=self.image_path)

        # Convert RGB to HSV and extract the saturation channel
        s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')

        # Threshold the saturation image
        s_thresh = pcv.threshold.binary(gray_img=s, threshold=85, max_value=255, object_type='light')

        # Median Blur
        s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)
        s_cnt = pcv.median_blur(gray_img=s_thresh, ksize=5)

        # Convert RGB to LAB and extract the Blue channel
        b = pcv.rgb2gray_lab( img, channel='b')

        # Threshold the blue image
        b_thresh = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, object_type='light')
        b_cnt = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, object_type='light')

        # Fill small objects
        # b_fill = pcv.fill(b_thresh, 10)

        # Join the thresholded saturation and blue-yellow images
        bs = pcv.logical_or(bin_img1=s_mblur, bin_img2=b_cnt)

        # Apply Mask (for VIS images, mask_color=white)
        masked = pcv.apply_mask( img, mask=bs, mask_color='white')

        # Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels
        masked_a = pcv.rgb2gray_lab(rgb_img=masked, channel='a')
        masked_b = pcv.rgb2gray_lab(rgb_img=masked, channel='b')

        # Threshold the green-magenta and blue images
        maskeda_thresh = pcv.threshold.binary(gray_img=masked_a, threshold=115, max_value=255, object_type='dark')
        maskeda_thresh1 = pcv.threshold.binary(gray_img=masked_a, threshold=135, max_value=255, object_type='light')
        maskedb_thresh = pcv.threshold.binary(gray_img=masked_b, threshold=128, max_value=255, object_type='light')

        # Join the thresholded saturation and blue-yellow images (OR)
        ab1 = pcv.logical_or(bin_img1=maskeda_thresh, bin_img2=maskedb_thresh)
        ab = pcv.logical_or(bin_img1=maskeda_thresh1, bin_img2=ab1)

        # Fill small objects
        ab_fill = pcv.fill(bin_img=ab, size=200)

        # Apply mask (for VIS images, mask_color=white)
        masked2 = pcv.apply_mask(masked, mask=ab_fill, mask_color='white')

        # Identify objects
        id_objects, obj_hierarchy = pcv.find_objects(img=masked2, mask=ab_fill)

        # Define ROI
        roi1, roi_hierarchy= pcv.roi.rectangle(img=masked2, x=100, y=100, h=200, w=200)

        # Decide which objects to keep
        roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=img, roi_contour=roi1, 
                                                                roi_hierarchy=roi_hierarchy, 
                                                                object_contour=id_objects, 
                                                                obj_hierarchy=obj_hierarchy,
                                                                roi_type='partial')

        # Object combine kept objects
        obj, mask = pcv.object_composition(img=img, contours=roi_objects, hierarchy=hierarchy3)

        ############### Analysis ################

        # Find shape properties, output shape image (optional)
        shape_imgs = pcv.analyze_object(img=img, obj=obj, mask=mask)

        # Shape properties relative to user boundary line (optional)
        boundary_img1 = pcv.analyze_bound_horizontal(img=img, obj=obj, mask=mask, line_position=1680)

        outfile=False
        if self.write_image_output == True:
            outfile = self.output_dir + "/" + filename
            cv2.imwrite(outfile,boundary_img1)

        # Determine color properties: Histograms, Color Slices, output color analyzed histogram (optional)
        color_histogram = pcv.analyze_color(rgb_img=img, mask=kept_mask, hist_plot_type="rgb")
        
        # Pseudocolor the grayscale image
        pseudocolored_img = pcv.visualize.pseudocolor(gray_img=s, mask=kept_mask, cmap="jet")

        # Write shape and color data to results file
        pcv.print_results(filename=self.result_path)

        with open(self.result_path) as f:
            self.data = json.load(f)
            if not self.write_result: 
                os.remove(self.result_path)
            self.data_ready = True
        
    def getHeight(self):
        if self.data_ready:
            return self.data["observations"]["height"]["value"]
        else: 
            return False
    def getWidth(self):
        if self.data_ready:
            return self.data["observations"]["width"]["value"]
        else: 
            return False

    def isFramed(self):
        if self.data_ready:
            return self.data["observations"]["object_in_frame"]["value"]
        return False
    
    def getColourHistogram(self):
        if self.data_ready :
            return (self.data["observations"]["red_frequencies"], self.data["observations"]["green_frequencies"], self.data["observations"]["blue_frequencies"])
        return (False, False, False)
    
      
if __name__ == '__main__':
    plant = Plant(image_path="plant_2.jpeg", write_image_output=True,result_path= "./temp/plant_info.json", write_result=True)
    
    plant.calculate()

    if plant.isFramed() is True:
        height = plant.getHeight()
        width = plant.getWidth()

        if (height is not False) and (width is not False) :
            print("Plant Height: " + str(height) + " pix\n")
            print("Plant Width: " + str(width) + " pix\n")
        
        (red, green, blue) = plant.getColourHistogram()

        if (red != green) and (green != blue) and (blue != False) :
            print("-------- RED --------\n\n")
            print(json.dumps(red, indent=4, sort_keys=True) + "\n")

            print("-------- GREEN --------\n\n")
            print(json.dumps(green, indent=4, sort_keys=True) + "\n")

            print("-------- BLUE --------\n\n")
            print(json.dumps(blue, indent=4, sort_keys=True) + "\n")
        
            #e.g: to get the y axis of the colour red:
            red_values = red["value"]
            print("Red Values:\n" + str(red_values) + "\n")

            #e.g to get the first value

            first_red_value = red["value"][0]
            print("First red value " + str(first_red_value) + "\n")

            #e.g get the x axis
            red_labels = red["label"]
            print("Red Labels:\n" + str(red_labels) + "\n")

            #e.g to get the first label
            first_red_label = red["label"][0]
            print("First red label " + str(first_red_label) + "\n")






