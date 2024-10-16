"""
    Klasa sluzy do przechowywania dla danego punktu sasiedniego trojkata
"""
from delaunay.LineFunction import LineFunction
from delaunay.Triangle import Triangle


class Point:
    def __init__(self, x: float, y: float, idPoint: int = -1):
        self.x = x
        self.y = y
        self.idPoint = idPoint


    def toNormalPoint(self):
        return self.x,self.y

    def doesPointContainedWithinTheCircle(self, other: Triangle):
        """
        Metoda sprawdza czy nasz punkt zawiera sie w okregu opisanym na danym trojkacie
        :param other: Obiekt klasy Triangle
        :return: True/False w zaleznosci czy punkt nalezy okregu opisanym na trojkacie
        """
        middleCircle, radiusOfCircleToSquare = other.desribeTheCircleOnTriangle()
        middleCirclePoint = Point(middleCircle[0], middleCircle[1])
        if (self.x - middleCirclePoint.x) ** 2 + (self.y - middleCirclePoint.y) ** 2 <= radiusOfCircleToSquare:
            return True
        return False

    def doesPointBelongToThisTriangle(self, other: Triangle):
        """
        Metoda sprawdza czy nasz punkt nalezy do danego trojkata,
        :param other: Obiekt klasy Triangle
        :return: True/False w zaleznosci czy punkt nalezy do trojkata
        """
        lineAB = LineFunction(other.a, other.b)
        lineAC = LineFunction(other.a, other.c)
        lineBC = LineFunction(other.b, other.c)

        verticalCounter = 0

        if lineAB.vertical:
            verticalCounter += 1

        if lineAC.vertical:
            verticalCounter += 1

        if lineBC.vertical:
            verticalCounter += 1

        if verticalCounter > 1:  # znaczy to ze ze nie dosyc ze nawet nie isteniej trojkat ale i punkt w nim takto tez nie moze istniec !
            return False

        if lineAB.isPointBelongsToSegment(self.x) and lineAC.isPointBelongsToSegment(self.x):  # punkt x znajduje sie miedzy prostymi AB oraz AC
           if not lineAC.vertical and not lineAB.vertical:
                if lineAC.calculateY(self.x) >= self.y >= lineAB.calculateY(self.x) or \
                        lineAB.calculateY(self.x) >= self.y >= lineAC.calculateY(self.x):
                    return True

           elif not lineAC.vertical and lineAB.vertical:  # przypadek kiedy prosta AC nie jest liniowa
               top_value = max(lineAC.calculateY(self.x),lineBC.calculateY(self.x))
               min_value = min(lineAC.calculateY(self.x),lineBC.calculateY(self.x))
               if top_value >= self.y >= min_value:
                   return True
               return False

           elif lineAC.vertical and not lineAB.vertical:  # przypadek kiedy prosta AB nie jest liniowa
               top_value = max(lineAB.calculateY(self.x), lineBC.calculateY(self.x))
               min_value = min(lineAB.calculateY(self.x), lineBC.calculateY(self.x))
               if top_value >= self.y >= min_value:
                   return True
               return False

        elif lineBC.isPointBelongsToSegment(self.x) and lineAB.isPointBelongsToSegment(self.x):  # punkt x znajduje sie miedzy prostymi BC oraz AB
            if not lineBC.vertical and not lineAB.vertical:
                if lineBC.calculateY(self.x) >= self.y >= lineAB.calculateY(self.x) or \
                        lineAB.calculateY(self.x) >= self.y >= lineBC.calculateY(self.x):
                    return True

            elif not lineBC.vertical and lineAB.vertical:  # przypadek kiedy prsota BC nie jest liniowa
                top_value = max(lineBC.calculateY(self.x), lineAC.calculateY(self.x))
                min_value = min(lineBC.calculateY(self.x), lineAC.calculateY(self.x))
                if top_value >= self.y >= min_value:
                    return True
                return False

            elif lineBC.vertical and not lineAB.vertical:  # przypadek kiedy prsota AB nie jest liniowa
                top_value = max(lineAB.calculateY(self.x), lineAC.calculateY(self.x))
                min_value = min(lineAB.calculateY(self.x), lineAC.calculateY(self.x))
                if top_value >= self.y >= min_value:
                    return True
                return False

        elif lineBC.isPointBelongsToSegment(self.x) and lineAC.isPointBelongsToSegment(self.x):  # punkt x znajduje sie miedzy prostymi BC oraz AC
            if not lineBC.vertical and not lineAC.vertical:
                if lineBC.calculateY(self.x) >= self.y >= lineAC.calculateY(self.x) or \
                        lineAC.calculateY(self.x) >= self.y >= lineBC.calculateY(self.x):
                    return True

            if lineBC.vertical and not lineAC.vertical:  # przypadek kiedy prsota AC nie jest liniowa
                top_value = max(lineAC.calculateY(self.x), lineAB.calculateY(self.x))
                min_value = min(lineAC.calculateY(self.x), lineAB.calculateY(self.x))
                if top_value >= self.y >= min_value:
                    return True
                return False

            if not lineBC.vertical and lineAC.vertical:  # przypadek kiedy prsota BC nie jest liniowa
                top_value = max(lineBC.calculateY(self.x), lineAB.calculateY(self.x))
                min_value = min(lineBC.calculateY(self.x), lineAB.calculateY(self.x))
                if top_value >= self.y >= min_value:
                    return True
                return False
        return False

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __lt__(self, other):
        if self.x < other.x:
            return True
        elif self.x == other.x:
            if self.y < other.y:
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        return f"({self.x},{self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

