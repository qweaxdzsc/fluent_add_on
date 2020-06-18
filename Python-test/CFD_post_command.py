import numpy as np
import subprocess


class CfdPost(object):
    def __init__(self, case_path, case_name, result_path, cse_file):
        self.case_path = case_path
        self.case_name = case_name
        self.result_path = result_path
        self.cse_file = cse_file
        script_name = case_name + ".cse"
        self.script_path = case_path + '\\' + script_name

    def load_case(self):
        self.cse_file += """
DATA READER:
  Clear All Objects = false
  Append Results = false
  Edit Case Names = false
  Multi Configuration File Load Option = Last Case
  Open in New View = true
  Keep Camera Position = true
  Load Particle Tracks = true
  Multi Configuration File Load Option = Last Case
  Construct Variables From Fourier Coefficients = true
  Open to Compare = false
  Files to Compare =
END

>load filename={case_path}/{case_name}.cas, \
force_reload=true
""".format(case_path=self.case_path, case_name=self.case_name)

    def create_plane(self, name, paraller_plane, X, Y, Z):
        self.cse_file += """
PLANE: {name}
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
  Option = {dir_plane} Plane
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
  X = {X} [m]
  Y = {Y} [m]
  Z = {Z} [m]
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

# """.format(name=name, dir_plane=paraller_plane, X=X, Y=Y, Z=Z)

    def create_contour(self, name, variable, plane, range='Local', Max='0.0', Min='0.0'):
        self.cse_file += """
CONTOUR: {name}
  Apply Instancing Transform = On
  Clip Contour = Off
  Colour Map = Default Colour Map
  Colour Scale = Linear
  Colour Variable = {variable}
  Colour Variable Boundary Values = Conservative
  Constant Contour Colour = Off
  Contour Range = {range}
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
  Location List = {plane_name}
  Max = {max} [K]
  Min = {min} [K]
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

""".format(name=name, variable=variable, plane_name=plane, range=range, max=Max, min=Min)

    def create_streamline(self, name, from_where, sample_number=400, direction='Forward', range='Local', Max='0.0',
                          Min='0.0'):
        self.cse_file += """
STREAMLINE:{name}
  Absolute Tolerance = 0.0 [m]
  Apply Instancing Transform = On
  Colour = 0.75, 0.75, 0.75
  Colour Map = Default Colour Map
  Colour Mode = Use Plot Variable
  Colour Scale = Linear
  Colour Variable = Velocity
  Colour Variable Boundary Values = Conservative
  Cross Periodics = On
  Culling Mode = No Culling
  Domain List = /DOMAIN GROUP:All Domains
  Draw Faces = On
  Draw Lines = Off
  Draw Streams = On
  Draw Symbols = Off
  Grid Tolerance = 0.01
  Instancing Transform = /DEFAULT INSTANCE TRANSFORM:Default Transform
  Lighting = On
  Line Width = 1
  Location List = {from_where}
  Locator Sampling Method = Equally Spaced
  Max = {max} [m s^-1]
  Maximum Number of Items = 25
  Min = {min} [m s^-1]
  Number of Samples = {sample_number}
  Number of Sides = 8
  Range = 
  Reduction Factor = 1.0
  Reduction or Max Number = Max Number
  Sample Spacing = 0.1
  Sampling Aspect Ratio = 1
  Sampling Grid Angle = 0 [degree]
  Seed Point Type = Equally Spaced Samples
  Simplify Geometry = Off
  Specular Lighting = On
  Stream Drawing Mode = Line
  Stream Initial Direction = 0 , 0 , 0
  Stream Size = 1.0
  Stream Symbol = Ball
  Streamline Direction = {direction}
  Streamline Maximum Periods = 20
  Streamline Maximum Segments = 10000
  Streamline Maximum Time = 0.0 [s]
  Streamline Type = 3D Streamline
  Streamline Width = 2
  Surface Drawing = Smooth Shading
  Surface Streamline Direction = Forward and Backward
  Symbol Size = 1.0
  Symbol Start Time = 10.0 [s]
  Symbol Stop Time = -10.0 [s]
  Symbol Time Interval = 1.0 [s]
  Tolerance Mode = Grid Relative
  Transparency = 0.0
  Variable = Velocity
  Variable Boundary Values = Conservative
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
""".format(name=name, from_where=from_where, sample_number=sample_number, direction=direction, range=range, max=Max,
               min=Min)

    def create_vector(self, name, location_plane, range='Local', Max='0.0', Min='0.0'):
        self.cse_file += """
VECTOR: {name}
  Apply Instancing Transform = On
  Colour = 0.75, 0.75, 0.75
  Colour Map = Default Colour Map
  Colour Mode = Use Plot Variable
  Colour Scale = Linear
  Colour Variable = Velocity
  Colour Variable Boundary Values = Conservative
  Coord Frame = Global
  Culling Mode = No Culling
  Direction = X
  Domain List = /DOMAIN GROUP:All Domains
  Draw Faces = On
  Draw Lines = Off
  Instancing Transform = /DEFAULT INSTANCE TRANSFORM:Default Transform
  Lighting = On
  Line Width = 1
  Location List = {location}
  Locator Sampling Method = Vertex
  Max = {max} [m s^-1]
  Maximum Number of Items = 100
  Min = {min} [m s^-1]
  Normalized = Off
  Number of Samples = 100
  Projection Type = None
  Random Seed = 1
  Range = {range}
  Reduction Factor = 1
  Reduction or Max Number = Reduction
  Sample Spacing = 0.1
  Sampling Aspect Ratio = 1
  Sampling Grid Angle = 0 [degree]
  Specular Lighting = On
  Surface Drawing = Smooth Shading
  Symbol = Line Arrow
  Symbol Size = 0.8
  Transparency = 0.0
  Variable = Velocity
  Variable Boundary Values = Conservative
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

""".format(name=name, location=location_plane, range=range, max=Max, min=Min)

    def show_hide(self, image_type, image_name, show_states='show'):
        self.cse_file += '\n\
>%s /%s:%s, view=/VIEW:View 1\n \
                         ' % (show_states, image_type, image_name)

    def bat_contour(self, paraller_plane, variable, size_min, size_max, bat_number=10):
        plane_array = np.linspace(size_min, size_max, bat_number)
        X, Y, Z = 0, 0, 0

        for i in plane_array:
            if 'X' not in paraller_plane:
                X = i
            elif 'Y' not in paraller_plane:
                Y = i
            else:
                Z = i
            index = np.where(plane_array == i)[0][0] + 1
            self.create_plane('plane%s%s' % (paraller_plane, index), paraller_plane, X, Y, Z)
            self.create_contour('contour%s%s' % (paraller_plane, index), variable,
                                                 'plane%s%s' % (paraller_plane, index), range='Global')

    def save_avz(self, suffix=''):
        self.cse_file += """
HARDCOPY:
  Antialiasing = On
  Hardcopy Filename = {file_location}/{file_name}{suffix}.avz
  Hardcopy Format = avz
  Hardcopy Tolerance = 0.0001
  Image Height = 600
  Image Scale = 100
  Image Width = 600
  JPEG Image Quality = 80
  Screen Capture = Off
  Use Screen Size = On
  White Background = Off
END

>print
    """.format(file_location=self.result_path, file_name=self.case_name, suffix=suffix)

    def save_png(self, suffix=''):
        self.cse_file += """
HARDCOPY:
  Antialiasing = On
  Hardcopy Filename = {file_location}/{file_name}{suffix}.avz
  Hardcopy Format = png
  Hardcopy Tolerance = 0.0001
  Image Height = 600
  Image Scale = 100
  Image Width = 600
  JPEG Image Quality = 80
  Screen Capture = Off
  Use Screen Size = On
  White Background = Off
END

>print
        """.format(file_location=self.result_path, file_name=self.case_name, suffix=suffix)

    def create_view1(self):
        self.cse_file += """
VIEW:View 1
  Camera Mode = User Specified
  CAMERA:
    Option = Pivot Point and Quaternion
    Pivot Point = 0.744949, -0.00180152, 0.415949
    Scale = 3.20172
    Pan = 0.208787, -0.0921302
    Rotation Quaternion = -0.707107, 0, 0, 0.707107
  END
END
> update
        """

    def create_command_file(self):
        with open(self.script_path, 'w') as cse:
            cse.write(self.cse_file)

    def run_command(self):
        p = subprocess.Popen(
            r"cd C:\Program Files\ANSYS Inc\v191\CFD-Post\bin && cfdpost -batch %s" % self.script_path,
            shell=True, stdout=subprocess.PIPE)
        while p.poll() == None:
            line = p.stdout.readline()
            msg = line.decode()
            print(msg)




