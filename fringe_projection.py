import sys
import math
import numpy
import vtk

class FringeProjection:

    def __init__(self):
       
        self.renderer = vtk.vtkRenderer()
        self.renderer.GradientBackgroundOn()

        self.ren_win = ren_win = vtk.vtkRenderWindow()
        
        ren_win.SetSize(512,512) 
        ren_win.SetMultiSamples(0)
        ren_win.SetAlphaBitPlanes(1)
        ren_win.SetOffScreenRendering(1) #default 1

        iren = self.iren = vtk.vtkRenderWindowInteractor()
        iren.SetRenderWindow(ren_win)
        ren_win.AddRenderer(self.renderer)
       
        camera_pass = vtk.vtkCameraPass()
        opaque = vtk.vtkOpaquePass()

        peeling=vtk.vtkDepthPeelingPass()
        peeling.SetMaximumNumberOfPeels(200)
        peeling.SetOcclusionRatio(0.1)

        translucent=vtk.vtkTranslucentPass()
        peeling.SetTranslucentPass(translucent)

        volume=vtk.vtkVolumetricPass()
        overlay=vtk.vtkOverlayPass()
        lights=vtk.vtkLightsPass()
        opaque_sequence=vtk.vtkSequencePass()

        passes2=vtk.vtkRenderPassCollection()
        passes2.AddItem(lights)
        passes2.AddItem(opaque)

        opaque_sequence.SetPasses(passes2)
        opaque_camera_pass=vtk.vtkCameraPass()
        opaque_camera_pass.SetDelegatePass(opaque_sequence)

        shadows_baker=vtk.vtkShadowMapBakerPass()
        shadows_baker.SetOpaquePass(opaque_camera_pass)
        shadows_baker.SetResolution(1024)

        #To cancel self-shadowing.
        shadows_baker.SetPolygonOffsetFactor(3.1)
        shadows_baker.SetPolygonOffsetUnits(10.0)

        shadows=vtk.vtkShadowMapPass()
        shadows.SetShadowMapBakerPass(shadows_baker)
        shadows.SetOpaquePass(opaque_sequence)

        seq=vtk.vtkSequencePass()
        passes=vtk.vtkRenderPassCollection()
        passes.AddItem(shadows_baker)
        passes.AddItem(shadows)
        passes.AddItem(lights)
        passes.AddItem(peeling)
        passes.AddItem(volume)
        passes.AddItem(overlay)

        seq.SetPasses(passes)
        camera_pass.SetDelegatePass(seq)
        self.renderer.SetPass(camera_pass)

        

    def FringeSimulator(self, file_name, file_output):
        
 
        reader = vtk.vtkPLYReader()
        reader.SetFileName(file_name)
        reader.Update()

        smooth = vtk.vtkWindowedSincPolyDataFilter()   
        smooth.SetInput(reader.GetOutput())
        smooth.Update()
  
        normals = vtk.vtkPolyDataNormals()
        normals.SetInput(smooth.GetOutput())
        normals.SetComputePointNormals(1)
        normals.SetComputeCellNormals(1)
        normals.Update()

        mapper=vtk.vtkDataSetMapper()
        mapper.SetInput(smooth.GetOutput())
        mapper.SetScalarVisibility(1)

        actor = vtk.vtkActor()
        actor.GetProperty().SetInterpolationToFlat()
        actor.SetMapper(mapper)

        self.renderer.AddActor(actor)

        key_properties = vtk.vtkInformation()
        key_properties.Set(vtk.vtkShadowMapBakerPass.OCCLUDER(),0) #// dummy val.
        key_properties.Set(vtk.vtkShadowMapBakerPass.RECEIVER(),0) #// dummy val.

        actor.SetPropertyKeys(key_properties)
        actor.SetVisibility(1)

        self.renderer.ResetCamera()
        cam = self.renderer.GetActiveCamera()

        cam_pos = cam.GetPosition()
        cam_f =  cam.GetFocalPoint()

        vcam_pos = numpy.array([float(cam_pos[0]), float(cam_pos[1]), float(cam_pos[2])])
        vcam_f = numpy.array([float(cam_f[0]),float(cam_f[1]),float(cam_f[2])])

        v = vcam_f - vcam_pos 
        d = numpy.linalg.norm(v)
        vn = v/d

        ap = vtk.vtkAppendPolyData()
        dist_fringes = cam_pos - vn * -250

        for x in xrange(-220, 220):
            cube_source= vtk.vtkCubeSource()
            cube_source.SetXLength(0.20)
            cube_source.SetYLength(80)
            cube_source.SetZLength(0.1)

            xfm = vtk.vtkTransform()
            xfm.Translate(float(x) * 0.40, 0, 0) 

            xfmPd = vtk.vtkTransformPolyDataFilter()
            xfmPd.SetInput(cube_source.GetOutput())
            xfmPd.SetTransform(xfm)

            ap.AddInput(xfmPd.GetOutput())

        ap.Update()


        xfm = vtk.vtkTransform()
        xfm.Translate(200, dist_fringes[1], dist_fringes[2])

        xfmPd = vtk.vtkTransformPolyDataFilter()
        xfmPd.SetInput(ap.GetOutput())
        xfmPd.SetTransform(xfm)

        cube_mapper=vtk.vtkPolyDataMapper()
        cube_mapper.SetInput(xfmPd.GetOutput())


        fringes_actor = vtk.vtkActor()
        fringes_actor.SetMapper(cube_mapper)
        fringes_actor.GetProperty().SetColor(1,0,0)

        fringesKeyProperties=vtk.vtkInformation()
        fringesKeyProperties.Set(vtk.vtkShadowMapBakerPass.OCCLUDER(),0) #// dummy val.
        fringesKeyProperties.Set(vtk.vtkShadowMapBakerPass.RECEIVER(),0) #// dummy val.
        fringes_actor.SetPropertyKeys(fringesKeyProperties)

        self.renderer.AddActor(fringes_actor)
        
        self.renderer.LightFollowCameraOff()
        self.renderer.AutomaticLightCreationOff()
        self.renderer.RemoveAllLights()
        self.renderer.UpdateLights()

        l = vtk.vtkLight()
        l.SetLightTypeToSceneLight()

        dist_light = cam_pos - vn * 6

        l.SetFocalPoint(vcam_f[0], vcam_f[1], vcam_f[2])
        l.SetPosition(220, dist_light[1], dist_light[2])
        l.PositionalOn()
        self.renderer.AddLight(l)
    
        self.renderer.Render()

        wf = vtk.vtkWindowToImageFilter()
        wf.SetInput(self.ren_win)
        wf.Update()

        png = vtk.vtkPNGWriter()
        png.SetFileName(file_output + ".png")
        png.SetInput(wf.GetOutput())
        png.Write()

def main():
    ply_file = sys.argv[1]
    png_file = sys.argv[2]

    fp = FringeProjection()
    fp.FringeSimulator(ply_file, png_file)

if __name__ == '__main__':
    main()
