from Algorithms.Shared.Utils import *
from Algorithms.Shared.Result import *

NumPoints = 64
AngleRange = 45.0
AnglePrecision = 2.0


class Template:
    def __init__(self, name, points):
        self.Points = points
        self.name = name
        self.Points = Resample(self.Points, NumPoints)
        self.Points = rotate_to_zero(self.Points)
        self.Points = ScaleTo(self.Points, SquareSize)
        self.Points = translate_to_origin(self.Points)


class DTWRecognizer:
    def __init__(self):
        self.templates = []

        '''
        self.templates.append(Template("Zig-Zag",[[387, 192],[388, 192],[388, 190],[388, 189],[388, 188],[388, 187],[388, 186],[388, 185],[388, 184],[389, 182],[389, 180],[390, 180],[390, 178],[391, 176],[392, 172],[393, 170],[395, 168],[396, 167],[398, 164],[399, 162],[400, 161],[401, 159],[403, 157],[403, 156],[404, 155],[405, 155],[406, 154],[407, 154],[408, 155],[408, 156],[410, 157],[412, 159],[414, 164],[418, 169],[421, 176],[424, 182],[426, 188],[428, 192],[430, 197],[430, 201],[432, 203],[433, 205], [433, 206],[434, 208],[434, 209],[435, 209],[435, 210],[435, 211],[436, 211],[437, 210],[438, 207],[441, 202],[445, 193],[449, 184],[454, 177],[457, 168], [459, 162],[460, 158],[461, 154],[462, 151],[463, 149],[463, 148],[464, 146],[464, 145], [464, 144],[464, 146],[464, 147],[464, 148],[464, 150],[464, 152],[464, 153],[464, 155],[464, 156],[465, 157],[465, 159], [466, 161],[466, 164],[467, 168],[467, 170],[468, 172],[469, 174],[469, 176],[469, 178],[470, 180],[470, 181],[471, 182],[471, 183],[471, 185],[471, 186],[472, 187],[473, 188],[473, 189],[473, 191],[474, 191],[474, 192],[475, 192],[475, 192],[475, 193],[476, 193],[479, 192],[479, 192],[480, 192],[480, 191],[480, 190],[480, 189],[480, 187],[481, 184],[482, 181],[484, 179],[485, 176],[486, 173],[488, 169],[489, 168],[490, 166],[490, 165],[491, 163],[491, 162],[492, 161]]))
        self.templates.append(Template("Line" ,[[430, 158],[435, 156],[440, 156],[447, 154],[456, 153],[465, 151],[476, 150],[484, 149],[495, 148],[503, 148],[510, 148],[517, 148],[520, 148],[525, 148],[530, 148],[533, 148],[535, 149],[538, 149],[539, 149],[540, 149],[541, 149],[542, 149]]))
        '''

    def add_template(self, name, points):
        self.templates.append(Template(name, points))

    def Recognize(self, points):
        points = Resample(points, NumPoints)
        points = rotate_to_zero(points)
        points = ScaleTo(points, SquareSize)
        points = translate_to_origin(points)

        b = float("inf")
        t = None

        for i, temp in enumerate(self.templates):
            Tpoints = temp
            d = DistanceAtBestAngle(points, Tpoints, -AngleRange, AngleRange, AnglePrecision)
            if d < b:
                b = d
                t = temp

        score = 1 - (b / HalfDiagonal)

        if t:
            return Result(t.name, score)
        else:
            return Result("Unrecognized.", 0.0)


def rotate_to_zero(points):
    c = Centroid(points)
    theta = math.atan2(c.Y - points[0].Y, c.X - points[0].X)
    newPoints = RotateBy(points, -theta)
    return newPoints


def translate_to_origin(points):
    c = Centroid(points)
    newpoints = []
    for p in points:
        qx, qy = p.X - c.X, p.Y - c.Y
        newpoints.append(Point(qx, qy))
    return newpoints
