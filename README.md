fgrc-tools
==========

Face Recognition Grand Challenge (FRGC) - Tools

### abs_to_ply.py
Convert abs file to ply file with textures (from ppm files).

**Requirements**
* [python 2.7](http://www.python.org/ "python")
* [pil](http://www.pythonware.com/products/pil/ "vtk")
* [vtk](http://www.vtk.org/ "pil")

**To run**
* python abs_to_ply.py *001.abs* *002.ppm* *output.ply*

**To visualize faces**
* python show_ply.py *my_face.ply*

### extract_abs_from_gz.py
Extract abs files from tar.gz.

**To run**
* python extract_abs_from_gz.py *./my_faces_folder/*

### fringe_projection.py
Fringe projection in face and save output in PNG file.

**To run**
* python fringe_projection.py *my_face.ply* *output.png*

**Requirements**
* [python 2.7](http://www.python.org/ "python")
* [vtk](http://www.vtk.org/ "vtk")
* [numpy](http://www.numpy.org/ "numpy")
