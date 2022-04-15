# Plant Caracteristics

Describing a plant using Image processing library PlantCV

# The results

The results can be seen in jupyter book inside src folder, just open `src/plants.ipynb` and you will see the results

# How to use

The first thing you need to do is treat all the growth stages inside the project.

To do so, run the command `python3 src/plant_treatment.py` on the root folder

Once done, open the juperbook `plants.ipynb` to see the results

#### Saving image to disk:

`pcv.print_image(purned_image, f"{path}_purned.jpg")`

#### How to use 3D models based on stl

- Run 3D_using_stl.ipynb
- Assign the path of the image in path variable
- the result will be generated as plant.stl file
- for a better vision,convert stl file to obj,otherwise you still can import that file using Blender.
