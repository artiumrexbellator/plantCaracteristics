from plantcv import plantcv as pcv
import json

if __name__ == "__main__":
	images = [
    "bout46",
	  "bout47",
	  "bout48",
	  "bout49",
	  "bout50",
	  "bout51",
	  "bout52",
	  "bout53",
	  "bout54",
	  "bout55",
	  "bout56",
	  "bout57",
  ]
 
	for image in images:
		path=f"./plants/{image}"

		# Read image
		raw_img, path, filename = pcv.readimage(filename=f"{path}/raw.jpg")

		# Convert RGB to HSV and extract the saturation channel
		saturation = pcv.rgb2gray_hsv(rgb_img=raw_img, channel='s')

		# Take a binary threshold to separate plant from background.
		binary_img = pcv.threshold.binary(gray_img=saturation, threshold=0, max_value=255, object_type='light')
		pcv.print_image(binary_img, f"{path}/binary.jpg")
		
  	# Generate the plant skeleton
		skeleton_img = pcv.morphology.skeletonize(binary_img)
		pcv.print_image(skeleton_img, f"{path}/skeleton.jpg")
  
		# Generate the purned image
		purned_img, seg_img, edge_objects = pcv.morphology.prune(skel_img=skeleton_img, size=15,mask=binary_img)
		pcv.print_image(purned_img, f"{path}/purned.jpg")
  
		# Find the plant branches
		branched_img = pcv.morphology.find_branch_pts(skel_img=purned_img, mask=binary_img)
		pcv.print_image(branched_img, f"{path}/branched.jpg")
  
		# Find the plant tips
		tips_img = pcv.morphology.find_tips(skel_img=purned_img, label="tips",mask=binary_img)
		pcv.print_image(tips_img, f"{path}/tips.jpg")

		# Identify objects
		id_objects, obj_hierarchy = pcv.find_objects(img=raw_img, mask=binary_img)
		# Define the region of interest (ROI)
		roi_contour, roi_hierarchy= pcv.roi.rectangle(img=binary_img, x=0, y=0, h=790, w=1150)
		# Make the region of interest object
		roi_objects, hierarchy, kept_mask, obj_area = pcv.roi_objects(img=raw_img, roi_contour=roi_contour, roi_hierarchy=roi_hierarchy, object_contour=id_objects, obj_hierarchy=obj_hierarchy, roi_type='partial')
		# Object combine kept objects
		composed_img, mask = pcv.object_composition(img=raw_img, contours=roi_objects, hierarchy=hierarchy)
		pcv.print_image(mask, f"{path}/composed.jpg")

		# Find shape properties, data gets stored to an Outputs class automatically
		analysed_img = pcv.analyze_object(img=raw_img, obj=composed_img, mask=mask, label="default")
		pcv.print_image(analysed_img, f"{path}/analysed.jpg")

		# JSON Output
		data = json.dumps(pcv.outputs.observations, indent=1)
		f = open(f"{path}/data.json", "w")
		f.write(data)
		f.close()
