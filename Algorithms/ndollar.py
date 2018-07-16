from Algorithms.Shared.Utils import *
from Algorithms.Shared.Result import *


# NDollarRecognizer constants
NumPoints = 96
OneDThreshold = 0.25    # customize to desired gesture set (usually 0.20 - 0.35)
StartAngleIndex = int(NumPoints / 8)   # eighth of gesture length
AngleSimilarityThreshold = Deg2Rad(30.0)


# Unistroke class: a unistroke template
class Unistroke:
    def __init__(self, name, useBoundedRotationInvariance, points):
        self.Name = name
        self.Points = Resample(points, NumPoints)
        radians = IndicativeAngle(self.Points)
        self.Points = RotateBy(self.Points, -radians)
        self.Points = ScaleTo(self.Points, SquareSize, OneDThreshold)
        if useBoundedRotationInvariance:
            self.Points = RotateBy(self.Points, +radians)
        self.Points = TranslateTo(self.Points, Origin)
        self.StartUnitVector = CalcStartUnitVector(self.Points, StartAngleIndex)
        self.Vector = Vectorize(self.Points, useBoundedRotationInvariance)


# Multistroke class: a container for unistrokes
class Multistroke:
    def __init__(self, name, useBoundedRotationInvariance, strokes):
        self.Name = name
        self.NumStrokes = len(strokes)
        order = []      # array of integer indices

        for i in range(len(strokes)):
            order.append(i)  # initialize

        orders = []  # array of integer arrays
        HeapPermute(len(strokes), order, orders)

        unistrokes = MakeUnistrokes(strokes, orders)  # returns array of point arrays
        self.Unistrokes = []  # unistrokes for this multistroke
        for j in range(0, len(unistrokes)):
            self.Unistrokes.append(Unistroke(name, useBoundedRotationInvariance, unistrokes[j]))


# NDollarRecognizer class
class NDollarRecognizer:
    def __init__(self, useBoundedRotationInvariance=True):
        # one predefined multistroke for each multistroke type
        self.Multistrokes = []

        self.Multistrokes.append(Multistroke("Zig-Zag", useBoundedRotationInvariance, [[
            Point(307, 216), Point(333, 186), Point(356, 215), Point(375, 186), Point(399, 216), Point(418, 186)
        ]]))

        self.Multistrokes.append(Multistroke("Rectangle", useBoundedRotationInvariance, [[
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
        ]]))

        self.Multistrokes.append(Multistroke("Circle", useBoundedRotationInvariance, [[
            Point(127, 141), Point(124, 140), Point(120, 139), Point(118, 139), Point(116, 139),
            Point(111, 140), Point(109, 141), Point(104, 144), Point(100, 147), Point(96, 152),
            Point(93, 157), Point(90, 163), Point(87, 169), Point(85, 175), Point(83, 181),
            Point(82, 190), Point(82, 195), Point(83, 200), Point(84, 205), Point(88, 213),
            Point(91, 216), Point(96, 219), Point(103, 222), Point(108, 224), Point(111, 224),
            Point(120, 224), Point(133, 223), Point(142, 222), Point(152, 218), Point(160, 214),
            Point(167, 210), Point(173, 204), Point(178, 198), Point(179, 196), Point(182, 188),
            Point(182, 177), Point(178, 167), Point(170, 150), Point(163, 138), Point(152, 130),
            Point(143, 129), Point(140, 131), Point(129, 136), Point(126, 139)
        ]]))

        self.Multistrokes.append(Multistroke("Check", useBoundedRotationInvariance, [[
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
        ]]))

        self.Multistrokes.append(Multistroke("Caret", useBoundedRotationInvariance, [[
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
        ]]))

        self.Multistrokes.append(Multistroke("V", useBoundedRotationInvariance, [[
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
        ]]))

        '''
        self.Multistrokes.append(Multistroke("T", useBoundedRotationInvariance, [
            [Point(30, 7), Point(103, 7)],
            [Point(66, 7), Point(66, 87)]
        ]))
        self.Multistrokes.append(Multistroke("N", useBoundedRotationInvariance, [
            [Point(177, 92), Point(177, 2)],
            [Point(182, 1), Point(246, 95)],
            [Point(247, 87), Point(247, 1)]]))
        self.Multistrokes.append(Multistroke("D", useBoundedRotationInvariance, [
            [Point(345, 9), Point(345, 87)],
            [Point(351, 8), Point(363, 8), Point(372, 9), Point(380, 11), Point(386, 14), Point(391, 17),
             Point(394, 22), Point(397, 28), Point(399, 34), Point(400, 42), Point(400, 50), Point(400, 56),
             Point(399, 61), Point(397, 66), Point(394, 70), Point(391, 74), Point(386, 78), Point(382, 81),
             Point(377, 83), Point(372, 85), Point(367, 87), Point(360, 87), Point(355, 88), Point(349, 87)]
        ]))
        self.Multistrokes.append(Multistroke("P", useBoundedRotationInvariance, [
            [Point(507, 8), Point(507, 87)],
            [Point(513, 7), Point(528, 7), Point(537, 8), Point(544, 10), Point(550, 12), Point(555, 15),
             Point(558, 18), Point(560, 22), Point(561, 27), Point(562, 33), Point(561, 37), Point(559, 42),
             Point(556, 45), Point(550, 48), Point(544, 51), Point(538, 53), Point(532, 54), Point(525, 55),
             Point(519, 55), Point(513, 55), Point(510, 55)]
        ]))
        self.Multistrokes.append(Multistroke("X", useBoundedRotationInvariance, [
            [Point(30, 146), Point(106, 222)],
            [Point(30, 225), Point(106, 146)]
        ]))
        self.Multistrokes.append(Multistroke("H", useBoundedRotationInvariance, [
            [Point(188, 137), Point(188, 225)],
            [Point(188, 180), Point(241, 180)],
            [Point(241, 137), Point(241, 225)]
        ]))
        self.Multistrokes.append(Multistroke("I", useBoundedRotationInvariance, [
            [Point(371, 149), Point(371, 221)],
            [Point(341, 149), Point(401, 149)],
            [Point(341, 221), Point(401, 221)]
        ]))
        self.Multistrokes.append(Multistroke("five-point star", useBoundedRotationInvariance, [
            [Point(177, 396), Point(223, 299), Point(262, 396), Point(168, 332), Point(278, 332), Point(184, 397)]
        ]))
        self.Multistrokes.append(Multistroke("null", useBoundedRotationInvariance, [
            [Point(382, 310), Point(377, 308), Point(373, 307), Point(366, 307), Point(360, 310), Point(356, 313),
             Point(353, 316), Point(349, 321), Point(347, 326), Point(344, 331), Point(342, 337), Point(341, 343),
             Point(341, 350), Point(341, 358), Point(342, 362), Point(344, 366), Point(347, 370), Point(351, 374),
             Point(356, 379), Point(361, 382), Point(368, 385), Point(374, 387), Point(381, 387), Point(390, 387),
             Point(397, 385), Point(404, 382), Point(408, 378), Point(412, 373), Point(416, 367), Point(418, 361),
             Point(419, 353), Point(418, 346), Point(417, 341), Point(416, 336), Point(413, 331), Point(410, 326),
             Point(404, 320), Point(400, 317), Point(393, 313), Point(392, 312)],
            [Point(418, 309), Point(337, 390)]
        ]))
        self.Multistrokes.append(Multistroke("arrowhead", useBoundedRotationInvariance, [
            [Point(506, 349), Point(574, 349)],
            [Point(525, 306), Point(584, 349), Point(525, 388)]
        ]))
        self.Multistrokes.append(Multistroke("pitchfork", useBoundedRotationInvariance, [
            [Point(38, 470), Point(36, 476), Point(36, 482), Point(37, 489), Point(39, 496), Point(42, 500),
             Point(46, 503), Point(50, 507), Point(56, 509), Point(63, 509), Point(70, 508), Point(75, 506),
             Point(79, 503), Point(82, 499), Point(85, 493), Point(87, 487), Point(88, 480), Point(88, 474),
             Point(87, 468)],
            [Point(62, 464), Point(62, 571)]
        ]))
        self.Multistrokes.append(Multistroke("six-point star", useBoundedRotationInvariance, [
            [Point(177, 554), Point(223, 476), Point(268, 554), Point(183, 554)],
            [Point(177, 490), Point(223, 568), Point(268, 490), Point(183, 490)]
        ]))
        self.Multistrokes.append(Multistroke("asterisk", useBoundedRotationInvariance, [
            [Point(325, 499), Point(417, 557)],
            [Point(417, 499), Point(325, 557)],
            [Point(371, 486), Point(371, 571)]
        ]))
        self.Multistrokes.append(Multistroke("half-note", useBoundedRotationInvariance, [
            [Point(546, 465), Point(546, 531)],
            [Point(540, 530), Point(536, 529), Point(533, 528), Point(529, 529), Point(524, 530), Point(520, 532),
             Point(515, 535), Point(511, 539), Point(508, 545), Point(506, 548), Point(506, 554), Point(509, 558),
             Point(512, 561), Point(517, 564), Point(521, 564), Point(527, 563), Point(531, 560), Point(535, 557),
             Point(538, 553), Point(542, 548), Point(544, 544), Point(546, 540), Point(546, 536)]
        ]))
        '''

    # The N$ Gesture Recognizer API begins here
    def Recognize(self, strokes, useBoundedRotationInvariance=True, requireSameNoOfStrokes=False, useProtractor=False):
        points = CombineStrokes(strokes)  # make one connected unistroke from the given strokes
        points = Resample(points, NumPoints)
        radians = IndicativeAngle(points)
        points = RotateBy(points, -radians)
        points = ScaleTo(points, SquareSize, OneDThreshold)
        if useBoundedRotationInvariance:
            points = RotateBy(points, +radians)  # restore
        points = TranslateTo(points, Origin)
        startv = CalcStartUnitVector(points, StartAngleIndex)
        vector = Vectorize(points, useBoundedRotationInvariance)  # for Protractor

        b = math.inf
        u = -1
        for i in range(len(self.Multistrokes)):  # for each multistroke
            if not requireSameNoOfStrokes or (len(strokes) == self.Multistrokes[i].NumStrokes):  # optional -- only attempt match when same # of component strokes
                for j in range(len(self.Multistrokes[i].Unistrokes)):  # each unistroke within this multistroke
                    if AngleBetweenUnitVectors(startv, self.Multistrokes[i].Unistrokes[j].StartUnitVector) <= AngleSimilarityThreshold:  # strokes start in the same direction
                        if useProtractor:  # for Protractor
                            d = OptimalCosineDistance(self.Multistrokes[i].Unistrokes[j].Vector, vector)
                        else:  # Golden Section Search (original $N)
                            d = DistanceAtBestAngle(points, self.Multistrokes[i].Unistrokes[j], -AngleRange, +AngleRange, AnglePrecision)
                        if d < b:
                            b = d  # best (least) distance
                            u = i  # multistroke owner of unistroke

        if u == -1:
            return Result("Unrecognized.", 0.0)
        else:
            if useProtractor:
                p = 1.0 / b
            else:
                p = 1.0 - b / HalfDiagonal

        return Result(self.Multistrokes[u].Name, p)

    def AddGesture(self, name, strokes, useBoundedRotationInvariance=False):
        self.Multistrokes.append(Multistroke(name, useBoundedRotationInvariance, strokes))
        num = 0
        for i in range(len(self.Multistrokes)):
            if self.Multistrokes[i].Name == name:
                num += 1

        return num


# Private helper functions from here on down
def HeapPermute(n, order,  orders):
    if n == 1:
        orders.append(order[:])     # append copy
    else:
        for i in range(n):
            HeapPermute(n - 1, order, orders)
            if n % 2 == 1:  # swap 0, n-1
                tmp = order[0]
                order[0] = order[n - 1]
                order[n - 1] = tmp
            else:   # swap i, n-1
                tmp = order[i]
                order[i] = order[n - 1]
                order[n - 1] = tmp


def MakeUnistrokes(strokes, orders):
    unistrokes = []     # array of point arrays
    for r in range(len(orders)):
        for b in range(int(math.pow(2, len(orders[r])))):    # use b's bits for directions
            unistroke = []  # array of points
            for i in range(len(orders[r])):
                if ((b >> i) & 1) == 1:  # is b's bit at index i on?
                    pts = strokes[orders[r][i]][:][::-1]   # copy and reverse
                else:
                    pts = strokes[orders[r][i]][:]    # copy
                for p in range(len(pts)):
                    unistroke.append(pts[p])  # append points

            unistrokes.append(unistroke)     # add one unistroke to set

    return unistrokes


def CombineStrokes(strokes):
    points = []
    for s in range(len(strokes)):
        for p in range(len(strokes[s])):
            points.append(Point(strokes[s][p].X, strokes[s][p].Y))

    return points


def Vectorize(points, useBoundedRotationInvariance): # for Protractor
    cos = 1.0
    sin = 0.0
    if useBoundedRotationInvariance:
        iAngle = math.atan2(points[0].Y, points[0].X)
        baseOrientation = (math.pi / 4.0) * math.floor((iAngle + math.pi / 8.0) / (math.pi / 4.0))
        cos = math.cos(baseOrientation - iAngle)
        sin = math.sin(baseOrientation - iAngle)

    sum1 = 0.0
    vector = []
    for i in range(len(points)):
        newX = points[i].X * cos - points[i].Y * sin
        newY = points[i].Y * cos + points[i].X * sin
        vector.append(newX)
        vector.append(newY)
        sum1 += newX * newX + newY * newY

    magnitude = math.sqrt(sum1)
    for i in range(len(vector)):
        vector[i] /= magnitude
    return vector


def CalcStartUnitVector(points, index):
    v = Point(points[index].X - points[0].X, points[index].Y - points[0].Y)
    len1 = math.sqrt(v.X * v.X + v.Y * v.Y)
    return Point(v.X / len1, v.Y / len1)


def AngleBetweenUnitVectors(v1, v2):  # gives acute angle between unit vectors from (0,0) to v1, and (0,0) to v2
    n = (v1.X * v2.X + v1.Y * v2.Y)
    c = max(-1.0, min(1.0, n))  # ensure [-1,+1]
    return math.acos(c)     # arc cosine of the vector dot product


