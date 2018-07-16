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

        self.templates.append(Template("Zig-Zag", [
            Point(307, 216), Point(333, 186), Point(356, 215), Point(375, 186), Point(399, 216), Point(418, 186)
        ]))

        self.templates.append(Template("Rectangle", [
            Point(78, 149), Point(78, 153), Point(78, 157), Point(78, 160), Point(79, 162),
            Point(79, 164), Point(79, 167), Point(79, 169), Point(79, 173), Point(79, 178),
            Point(79, 183), Point(80, 189), Point(80, 193), Point(80, 198), Point(80, 202),
            Point(81, 208), Point(81, 210), Point(81, 216), Point(82, 222), Point(82, 224),
            Point(82, 227), Point(83, 229), Point(83, 231), Point(85, 230), Point(88, 232),
            Point(90, 233), Point(92, 232), Point(94, 233), Point(99, 232), Point(102, 233),
            Point(106, 233), Point(109, 234), Point(117, 235), Point(123, 236), Point(126, 236),
            Point(135, 237), Point(142, 238), Point(145, 238), Point(152, 238), Point(154, 239),
            Point(165, 238), Point(174, 237), Point(179, 236), Point(186, 235), Point(191, 235),
            Point(195, 233), Point(197, 233), Point(200, 233), Point(201, 235), Point(201, 233),
            Point(199, 231), Point(198, 226), Point(198, 220), Point(196, 207), Point(195, 195),
            Point(195, 181), Point(195, 173), Point(195, 163), Point(194, 155), Point(192, 145),
            Point(192, 143), Point(192, 138), Point(191, 135), Point(191, 133), Point(191, 130),
            Point(190, 128), Point(188, 129), Point(186, 129), Point(181, 132), Point(173, 131),
            Point(162, 131), Point(151, 132), Point(149, 132), Point(138, 132), Point(136, 132),
            Point(122, 131), Point(120, 131), Point(109, 130), Point(107, 130), Point(90, 132),
            Point(81, 133), Point(76, 133)
        ]))

        self.templates.append(Template("Circle", [
            Point(127, 141), Point(124, 140), Point(120, 139),  Point(118, 139), Point(116, 139),
            Point(111, 140), Point(109, 141), Point(104, 144), Point(100, 147), Point(96, 152),
            Point(93, 157), Point(90, 163), Point(87, 169), Point(85, 175), Point(83, 181),
            Point(82, 190), Point(82, 195), Point(83, 200), Point(84, 205), Point(88, 213),
            Point(91, 216), Point(96, 219), Point(103, 222), Point(108, 224), Point(111, 224),
            Point(120, 224), Point(133, 223), Point(142, 222), Point(152, 218), Point(160, 214),
            Point(167, 210), Point(173, 204), Point(178, 198), Point(179, 196), Point(182, 188),
            Point(182, 177), Point(178, 167), Point(170, 150), Point(163, 138), Point(152, 130),
            Point(143, 129), Point(140, 131), Point(129, 136), Point(126, 139)
        ]))

        self.templates.append(Template("Check", [
            Point(91, 185), Point(93, 185), Point(95, 185), Point(97, 185), Point(100, 188),
            Point(102, 189), Point(104, 190), Point(106, 193), Point(108, 195), Point(110, 198),
            Point(112, 201), Point(114, 204), Point(115, 207), Point(117, 210), Point(118, 212),
            Point(120, 214), Point(121, 217), Point(122, 219), Point(123, 222), Point(124, 224),
            Point(126, 226), Point(127, 229), Point(129, 231), Point(130, 233), Point(129, 231),
            Point(129, 228), Point(129, 226), Point(129, 224), Point(129, 221), Point(129, 218),
            Point(129, 212), Point(129, 208), Point(130, 198), Point(132, 189), Point(134, 182),
            Point(137, 173), Point(143, 164), Point(147, 157), Point(151, 151), Point(155, 144),
            Point(161, 137), Point(165, 131), Point(171, 122), Point(174, 118), Point(176, 114),
            Point(177, 112), Point(177, 114), Point(175, 116), Point(173, 118)
        ]))

        self.templates.append(Template("Caret", [
            Point(79, 245), Point(79, 242), Point(79, 239), Point(80, 237), Point(80, 234),
            Point(81, 232), Point(82, 230), Point(84, 224), Point(86, 220), Point(86, 218),
            Point(87, 216), Point(88, 213), Point(90, 207), Point(91, 202), Point(92, 200),
            Point(93, 194), Point(94, 192), Point(96, 189), Point(97, 186), Point(100, 179),
            Point(102, 173), Point(105, 165), Point(107, 160), Point(109, 158), Point(112, 151),
            Point(115, 144), Point(117, 139), Point(119, 136), Point(119, 134), Point(120, 132),
            Point(121, 129), Point(122, 127), Point(124, 125), Point(126, 124), Point(129, 125),
            Point(131, 127), Point(132, 130), Point(136, 139), Point(141, 154), Point(145, 166),
            Point(151, 182), Point(156, 193), Point(157, 196), Point(161, 209), Point(162, 211),
            Point(167, 223), Point(169, 229), Point(170, 231), Point(173, 237), Point(176, 242),
            Point(177, 244), Point(179, 250), Point(181, 255), Point(182, 257)
        ]))

        self.templates.append(Template("V", [
            Point(89, 164), Point(90, 162), Point(92, 162), Point(94, 164), Point(95, 166),
            Point(96, 169), Point(97, 171), Point(99, 175), Point(101, 178), Point(103, 182),
            Point(106, 189), Point(108, 194), Point(111, 199), Point(114, 204), Point(117, 209),
            Point(119, 214), Point(122, 218), Point(124, 222), Point(126, 225), Point(128, 228),
            Point(130, 229), Point(133, 233), Point(134, 236), Point(136, 239), Point(138, 240),
            Point(139, 242), Point(140, 244), Point(142, 242), Point(142, 240), Point(142, 237),
            Point(143, 235), Point(143, 233), Point(145, 229), Point(146, 226), Point(148, 217),
            Point(149, 208), Point(149, 205), Point(151, 196), Point(151, 193), Point(153, 182),
            Point(155, 172), Point(157, 165), Point(159, 160), Point(162, 155), Point(164, 150),
            Point(165, 148), Point(166, 146)
        ]))

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
