from plantcv.plantcv.morphology import skeletonize,segment_skeleton\
    ,segment_path_length,find_branch_pts,prune,find_tips
import plantcv.plantcv as pcv
import cv2
import numpy as np
import json
from PIL import Image
import io
import base64


class PlantChars:

    def __init__(self):
        self.image = None
        self.mask = None
        self.skel = None

    def loadImage(self, path):
        self.image = cv2.imread(path)
        # Convert RGB to HSV and extract the saturation channel
        s = pcv.rgb2gray_hsv(rgb_img=self.image, channel='s')
        # Take a binary threshold to separate plant from background.
        # Threshold can be on either light or dark objects in the image.
        s_thresh = pcv.threshold.binary(gray_img=s,
                                        threshold=85,
                                        max_value=255,
                                        object_type='light')
        # Median Blur to clean noise
        s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)
        self.mask = s_mblur
        self.mask = cv2.threshold(self.mask, 127, 255, cv2.THRESH_BINARY)[1]
        pcv.print_image(
            self.mask,
            '/home/artium/Desktop/master/image_processing/LeafDetector/binary.png'
        )

    def whiteMask(self):
        # Apply mask (for VIS images, mask_color=white)
        mask = pcv.apply_mask(img=self.image,
                              mask=self.mask,
                              mask_color='white')
        #pcv.print_image(mask, '/home/artium/Desktop/master/image processing/LeafDetector/masked.png')
        return mask

    def skeletonize(self):
        skel = skeletonize(self.mask)
        pcv.print_image(
            skel,
            '/home/artium/Desktop/master/image_processing/LeafDetector/skel.png'
        )
        return skel

    def skeleton(self):
        img = self.mask.copy()
        size = np.size(img)
        skel = np.zeros(img.shape, np.uint8)

        ret, img = cv2.threshold(img, 127, 255, 0)
        element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        done = False

        while (not done):
            eroded = cv2.erode(img, element)
            temp = cv2.dilate(eroded, element)
            temp = cv2.subtract(img, temp)
            skel = cv2.bitwise_or(skel, temp)
            img = eroded.copy()

            zeros = size - cv2.countNonZero(img)
            if zeros == size:
                done = True

        return skel

    def prune(self):
        #skeleton=pcv.closing(gray_img=self.skeleton())
        if self.skel is None:
            self.skel = self.skeletonize()
        img1, seg_img, edge_objects = prune(skel_img=self.skel,
                                            size=15,
                                            mask=self.mask)
        #pcv.print_image(img1, '/home/artium/Desktop/master/image processing/LeafDetector/pruned.png')
        return img1

    def findBranches(self):
        branches = find_branch_pts(skel_img=self.prune(), mask=self.mask)
        #pcv.print_image(branches, '/home/artium/Desktop/master/image processing/LeafDetector/branches.png')
        return branches

    def findTips(self):
        if self.skel is None:
            self.skel = self.skeletonize()
        tip_pts_mask = find_tips(skel_img=self.skel,
                                 label="tips",
                                 mask=self.mask)
        #pcv.print_image(tip_pts_mask, '/home/artium/Desktop/master/image processing/LeafDetector/tips.png')
        return tip_pts_mask

    def height(self):
        # Identify objects and contours
        mask = self.whiteMask()
        id_objects, obj_hierarchy = pcv.find_objects(img=mask, mask=self.mask)
        # Define the region of interest (ROI)
        roi1, roi_hierarchy = pcv.roi.rectangle(img=mask,
                                                x=100,
                                                y=100,
                                                h=200,
                                                w=200)
        # Decide which objects to keep
        roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(
            img=self.image,
            roi_contour=roi1,
            roi_hierarchy=roi_hierarchy,
            object_contour=id_objects,
            obj_hierarchy=obj_hierarchy,
            roi_type='partial')
        # Object combine kept objects
        obj, mask = pcv.object_composition(img=self.image,
                                           contours=roi_objects,
                                           hierarchy=hierarchy3)
        ############### Analysis ################
        # Find shape properties, data gets stored to an Outputs class automatically
        analysis_image = pcv.analyze_object(img=self.image,
                                            obj=obj,
                                            mask=self.mask,
                                            label="default")
        #pcv.print_image(analysis_image, '/home/artium/Desktop/master/image processing/LeafDetector/height.png')
        return analysis_image.astype("uint8")


# u can use tostring or fromtobytes,but tobytes is optimal as long as tostring will be deprecated for behavior reasons

    def encodeImage(self, img):
        enc = cv2.imencode('.png', img)[1]
        data_encode = np.array(enc)
        buff_encode = data_encode.tobytes()
        return buff_encode

    def fullImageTraitment(self):
        return (
        self.encodeImage(np.uint8((self.image))),
        self.encodeImage(np.uint8(self.mask)),
        self.encodeImage(np.uint8(self.whiteMask())),
        self.encodeImage(np.uint8(self.prune())),
        self.encodeImage(np.uint8(self.findBranches())),
        self.encodeImage(np.uint8(self.findTips())),\
        self.encodeImage(np.uint8(self.height())),
        self.encodeImage(np.uint8(self.skel)),
        json.dumps(pcv.outputs.observations))

pc = PlantChars()
pc.loadImage(
    '/home/artium/Desktop/master/image_processing/LeafDetector/src/database/plants/stage08.jpg'
)
pc.skeletonize()