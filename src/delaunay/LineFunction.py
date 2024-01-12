"""
    Klasa sluzy do obliczeania funkcji liniowej dwoch punktow - zakladamy ze dwa punkty nie tworza pionowego odcinka.
"""

class LineFunction:
    def __init__(self, pointA, pointB):
        self.vertical = False  # atrybut okresla czy nasza funkcja jest pionowa czyli np. x = 3
        self.factorA, self.factorB = self.calculateFactors(pointA, pointB)
        self.pointA = pointA
        self.pointB = pointB
        self.minX = min(pointA.x,pointB.x)
        self.maxX = max(pointA.x, pointB.x)
        self.minY = min(pointA.y, pointB.y)
        self.maxY = max(pointA.y, pointB.y)

    def isPointBelongsToSegment(self,x: float):
        """
        Metoda sprawdza czy dany punkt nalezy do granic naszej prostej
        :param x: Wspolrzedna x-owa danego punktu
        :return: True/False w zaleznosci od tego czy punkt sie miesci w danym przedziale
        """
        if self.maxX >= x >= self.minX:
            return True
        return False

    def calculateFactors(self, a, b):
        """
        Metoda oblicza A i B, we wzorze y = A*x + B
        :param a: Punkt na plaszczyznie R^2
        :param b: Punkt na plaszczyznie R^2
        :return: Obliczone wartosci A i B.
        """
        if a.x == b.x:  # znaczy to ze mamy do czynenia z odcinkiem pionowym - tak wiec trzeba go oznaczyc
            self.vertical = True
            return None, None
        A = (b.y - a.y) / (b.x - a.x)
        B = a.y - A * a.x
        return A, B

    def calculateY(self, x: float):
        """
        Metoda oblicza wartosc y dla danego x w naszej funkji
        :param x: Wspolrzedna x-owa danego punktu
        :return: Wartosc jaka jest osiagana dla tego punktu
        """
        if self.vertical:  # najpiew sprawdzam czy nie jest to napewno odcinek pionowy
            return None
        return x * self.factorA + self.factorB

    def findIntersection(self, other):
        """
        Metoda oblicza przeciecie miedzy dwiema prostymi
        :param other: obiekt klasy LineFunction
        :return: wartosc wspolrzednej x, gdzie sie przecinaja dane proste o ile sie przecinaja, w przeciwnym wypadku jest zwracany None
        """
        if self.vertical and not other.vertical:
            return self.pointA.x

        if not self.vertical and other.vertical:
            return other.pointA.x

        if not self.vertical and not other.vertical and self.factorA != other.factorA:  # mam do czynenia z prostymi nie pionowymi oraz nie rownoleglymi
            return (other.factorB - self.factorB) / (self.factorA - other.factorA)

        return None  # pozostale przypadki