import sys
import os
import string
import vtk
import fileinput
from PIL import Image

pointSource = vtk.vtkProgrammableSource()
data = []
point_colors = []


colors = vtk.vtkUnsignedCharArray()

def readPoints():
    output = pointSource.GetPolyDataOutput()
    points = vtk.vtkPoints()
    output.SetPoints(points)

    colors.SetNumberOfComponents(3)
    #colors.SetNumberOfTuples(len(point_colors))
    colors.SetName("Colors")
    
    for value, color_value in zip(data, point_colors):
        x, y, z = float(value[0]), float(value[1]), float(value[2])
        points.InsertNextPoint(x, y, z)
        
        r, g, b = color_value[0], color_value[1], color_value[2]
        colors.InsertNextTuple3(r, g, b);

def abs2asc(abs_file, tex_file,output):

    ftex = Image.open(tex_file)

    f = open(abs_file)
    rows = int(f.readline().split()[0])
    cols = int(f.readline().split()[0])
    
    values = []

    # Reading the junk line
    f.readline()

    numbers = f.read().split()

    #flags
    fl = numbers[0: rows * cols]

    #X coordinates
    x = numbers[rows * cols: rows * cols * 2]

    # Y coordinates
    y = numbers[rows * cols * 2: rows * cols * 3]

    # Z coordinates
    z = numbers[rows * cols * 3: rows * cols * 4]
    
    for i in xrange(len(fl)):
        if fl[i] == '1':
            data.append([x[i], y[i], z[i]])
            
            px = i%cols
            py = i/cols
            color_pixel = ftex.getpixel((px,py))
            point_colors.append(color_pixel)
    
    pointSource.SetExecuteMethod(readPoints)
    pointSource.GetOutput().GetCellData().SetScalars(colors)
    pointSource.GetOutput().Update()
 
    delaunay = vtk.vtkDelaunay2D()
    #delaunay.SetTolerance(0.5)
    delaunay.SetAlpha(2.0)
    delaunay.SetInput(pointSource.GetOutput())
    delaunay.Update()

    poly = delaunay.GetOutput()

    w = vtk.vtkPLYWriter()
    w.SetInput(poly)
    w.SetFileName(output + ".ply")
    w.SetFileTypeToASCII()
    w.SetDataByteOrderToLittleEndian()
    #w.SetColorModeToUniformPointColor()
    #w.SetScalarsName("aaa")
    w.Write()
    
    lnumber = 1
    count = 0
    max_points = len(point_colors)
    #print max_points
    for line in fileinput.input(output + ".ply", inplace=1):
        if lnumber > 11 and count <= max_points - 1:
            r, g, b = point_colors[count]
            new_line = line.replace("\n", "")
            print new_line, r, g, b
            count += 1
        elif(lnumber == 8):
            print line, "property uchar red\n", "property uchar green\n", "property uchar blue"
        else:
            new_line = line.replace("\n", "")
            print new_line

        lnumber += 1
        
    print "Terminou >> ", abs_file, ">>" , output + ".ply"


def main():
    abs_file = sys.argv[1]
    tex_file = sys.argv[2]
    asc_output = sys.argv[3]
    abs2asc(abs_file, tex_file,asc_output)

if __name__ == '__main__':
    main()
