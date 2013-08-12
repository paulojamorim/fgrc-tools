import sys
import vtk

def show_ply(ply_file):
    r = vtk.vtkPLYReader()
    r.SetFileName(ply_file)
    r.Update()

    mapper = vtk.vtkDataSetMapper()
    mapper.SetInput(r.GetOutput())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    ren.AddActor(actor)
    iren.Render() 
    iren.Start()

if __name__ == '__main__':
    ply_file = sys.argv[1]
    show_ply(ply_file)
