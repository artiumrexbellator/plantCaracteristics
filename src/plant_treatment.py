from plantcv import plantcv as pcv
from plant_sqlite import insert_plant

if __name__ == "__main__":
    print("Started with all stages")

    images = [
        "stage01",
        "stage02",
        "stage03",
        "stage04",
        "stage05",
        "stage06",
        "stage07",
        "stage08",
        "stage09",
        "stage10",
        "stage11",
        "stage12",
    ]

    for image in images:
        print(f"Tearting {image}")

        path = f"./src/database/plants/{image}"

        # Read image
        raw_image, rpath, filename = pcv.readimage(filename=f"{path}.jpg")

        # Convert RGB to HSV and extract the saturation channel
        saturation = pcv.rgb2gray_hsv(rgb_img=raw_image, channel='s')

        # Take a binary threshold to separate plant from background.
        binary_image = pcv.threshold.binary(gray_img=saturation,
                                            threshold=0,
                                            max_value=255,
                                            object_type='light')

        # Generate the plant skeleton
        skeleton_image = pcv.morphology.skeletonize(binary_image)

        # Generate the purned image
        purned_image, seg_img, edge_objects = pcv.morphology.prune(
            skel_img=skeleton_image, size=15, mask=binary_image)

        # Find the plant branches
        branches_image = pcv.morphology.find_branch_pts(skel_img=purned_image,
                                                        mask=binary_image)

        # Find the plant tips
        tips_image = pcv.morphology.find_tips(skel_img=purned_image,
                                              label="tips",
                                              mask=binary_image)

        # Identify objects
        id_objects, obj_hierarchy = pcv.find_objects(img=raw_image,
                                                     mask=binary_image)
        # Define the region of interest (ROI)
        roi_contour, roi_hierarchy = pcv.roi.rectangle(img=binary_image,
                                                       x=0,
                                                       y=0,
                                                       h=790,
                                                       w=1150)
        # Make the region of interest object
        roi_objects, hierarchy, kept_mask, obj_area = pcv.roi_objects(
            img=raw_image,
            roi_contour=roi_contour,
            roi_hierarchy=roi_hierarchy,
            object_contour=id_objects,
            obj_hierarchy=obj_hierarchy,
            roi_type='partial')
        # Object combine kept objects
        composed_image, mask = pcv.object_composition(img=raw_image,
                                                      contours=roi_objects,
                                                      hierarchy=hierarchy)

        # Find shape properties, data gets stored to an Outputs class automatically
        height_image = pcv.analyze_object(img=raw_image,
                                          obj=composed_image,
                                          mask=mask,
                                          label="default")

        # JSON Output
        metadata = pcv.outputs.observations

        # Insert the result to sqlite database
        insert_plant(image, raw_image, binary_image, raw_image, purned_image,
                     branches_image, tips_image, height_image, skeleton_image,
                     metadata)

    print("Done with all stages")
