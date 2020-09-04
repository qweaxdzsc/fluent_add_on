import os
import sys
import vtk

os.chdir(os.path.abspath(os.path.dirname(__file__)))
colors = vtk.vtkNamedColors()

r = vtk.vtkFLUENTReader()
r.SetFileName(r'G:\test\queue_test2\queue_test2.cas')
r.Update()

g = vtk.vtkCompositeDataGeometryFilter()
g.SetInputConnection(r.GetOutputPort())

stlWriter = vtk.vtkSTLWriter()
stlWriter.SetFileName(r'C:\Users\BZMBN4\Desktop\demo1.stl')
stlWriter.SetInputConnection(g.GetOutputPort())
stlWriter.Write()

# reader = vtk
reader = vtk.vtkSTLReader()
reader.SetFileName(r'C:\Users\BZMBN4\Desktop\demo1.stl')
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())
actor = vtk.vtkActor()
actor.SetMapper(mapper)

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

ren.AddActor(actor)
ren.SetBackground(colors.GetColor3d('cobalt_green'))

iren.Initialize()
renWin.SetSize(1000, 1000)
renWin.Render()
iren.Start()