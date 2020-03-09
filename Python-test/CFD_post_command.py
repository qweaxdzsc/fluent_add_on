import os
import numpy as np

file_dir = r"C:\Users\BZMBN4\Desktop"


file_name = "command.txt"
file_path = file_dir + "\\" + file_name


def create_plane(name, paraller_plane, X, Y, Z):
    code = """
PLANE: %s
  Apply Instancing Transform = On
  Apply Texture = Off
  Blend Texture = On
  Bound Radius = 0.5 [m]
  Colour = 0.75, 0.75, 0.75
  Colour Map = Default Colour Map
  Colour Mode = Constant
  Colour Scale = Linear
  Colour Variable = Pressure
  Colour Variable Boundary Values = Conservative
  Culling Mode = No Culling
  Direction 1 Bound = 1.0 [m]
  Direction 1 Orientation = 0 [degree]
  Direction 1 Points = 10
  Direction 2 Bound = 1.0 [m]
  Direction 2 Points = 10
  Domain List = /DOMAIN GROUP:All Domains
  Draw Faces = On
  Draw Lines = Off
  Instancing Transform = /DEFAULT INSTANCE TRANSFORM:Default Transform
  Invert Plane Bound = Off
  Lighting = On
  Line Colour = 0, 0, 0
  Line Colour Mode = Default
  Line Width = 1
  Max = 0.0 [Pa]
  Min = 0.0 [Pa]
  Normal = 1 , 0 , 0
  Option = %s Plane
  Plane Bound = None
  Plane Type = Slice
  Point = 0 [m], 0 [m], 0 [m]
  Point 1 = 0 [m], 0 [m], 0 [m]
  Point 2 = 1 [m], 0 [m], 0 [m]
  Point 3 = 0 [m], 1 [m], 0 [m]
  Range = Global
  Render Edge Angle = 0 [degree]
  Specular Lighting = On
  Surface Drawing = Smooth Shading
  Texture Angle = 0
  Texture Direction = 0 , 1 , 0
  Texture File = 
  Texture Material = Metal
  Texture Position = 0 , 0
  Texture Scale = 1
  Texture Type = Predefined
  Tile Texture = Off
  Transform Texture = Off
  Transparency = 0.0
  Visibility = On
  X = %s [m]
  Y = %s [m]
  Z = %s [m]
  OBJECT VIEW TRANSFORM: 
    Apply Reflection = Off
    Apply Rotation = Off
    Apply Scale = Off
    Apply Translation = Off
    Principal Axis = Z
    Reflection Plane Option = XY Plane
    Rotation Angle = 0.0 [degree]
    Rotation Axis From = 0 [m], 0 [m], 0 [m]
    Rotation Axis To = 0 [m], 0 [m], 0 [m]
    Rotation Axis Type = Principal Axis
    Scale Vector = 1 , 1 , 1
    Translation Vector = 0 [m], 0 [m], 0 [m]
    X = 0.0 [m]
    Y = 0.0 [m]
    Z = 0.0 [m]
  END
END

""" % (name, paraller_plane, X, Y, Z)
    return code


def create_contour(name, plane):
    code = """
CONTOUR: %s
  Apply Instancing Transform = On
  Clip Contour = Off
  Colour Map = Default Colour Map
  Colour Scale = Linear
  Colour Variable = Temperature
  Colour Variable Boundary Values = Conservative
  Constant Contour Colour = Off
  Contour Range = Local
  Culling Mode = No Culling
  Domain List = /DOMAIN GROUP:All Domains
  Draw Contours = On
  Font = Sans Serif
  Fringe Fill = On
  Instancing Transform = /DEFAULT INSTANCE TRANSFORM:Default Transform
  Lighting = On
  Line Colour = 0, 0, 0
  Line Colour Mode = Default
  Line Width = 1
  Location List = /PLANE:%s
  Max = 0.0 [K]
  Min = 0.0 [K]
  Number of Contours = 25
  Show Numbers = Off
  Specular Lighting = On
  Surface Drawing = Smooth Shading
  Text Colour = 0, 0, 0
  Text Colour Mode = Default
  Text Height = 0.024
  Transparency = 0.0
  Use Face Values = Off
  Value List = 0 [K],1 [K]
  Visibility = On
  OBJECT VIEW TRANSFORM: 
    Apply Reflection = Off
    Apply Rotation = Off
    Apply Scale = Off
    Apply Translation = Off
    Principal Axis = Z
    Reflection Plane Option = XY Plane
    Rotation Angle = 0.0 [degree]
    Rotation Axis From = 0 [m], 0 [m], 0 [m]
    Rotation Axis To = 0 [m], 0 [m], 0 [m]
    Rotation Axis Type = Principal Axis
    Scale Vector = 1 , 1 , 1
    Translation Vector = 0 [m], 0 [m], 0 [m]
    X = 0.0 [m]
    Y = 0.0 [m]
    Z = 0.0 [m]
  END
END

""" % (name, plane)
    return code


def show_hide(image_type, image_name, show_states='show'):
    code = '>%s /%s:%s' % (show_states, image_type, image_name)
    return code


def bat_contour(paraller_plane, size_min, size_max):
    plane_array = np.linspace(size_min, size_max, 10)
    X, Y, Z = 0, 0, 0
    text = ""

    for i in plane_array:
        if 'X' not in paraller_plane:
            X = i
        elif 'Y' not in paraller_plane:
            Y = i
        else:
            Z = i
        index = np.where(plane_array == i)[0][0]+1
        text += create_plane('plane%s%s' % (paraller_plane, index), paraller_plane, X, Y, Z)
        text += create_contour('contour%s%s' % (paraller_plane, index), 'plane%s%s' % (paraller_plane, index))
        text += show_hide('CONTOUR', 'contour%s%s' % (paraller_plane, index))

    return text


content = bat_contour('XY', 0.37, 0.6)

with open(file_path, 'w') as txt:
    txt.write(content)

os.system(file_path)