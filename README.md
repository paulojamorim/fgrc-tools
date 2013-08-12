fgrc-tools
==========

Face Recognition Grand Challenge (FRGC) - Tools

### abs_to_ply.py
Convert abs file to ply file with textures (from ppm files).

**Requirements**
* [python 2.7](http://www.python.org/ "python")
* [vtk](http://www.pythonware.com/products/pil/ "vtk")
* [pil](http://www.vtk.org/ "pil")

**To run**
* python abs_to_ply.py *001.abs* *002.ppm* *output.ply*

**To visualize faces**
* python show_ply.py *my_face.ply*
