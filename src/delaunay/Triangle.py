"""
    Klasa slzuzy do przechowywania szczegolnych infomracji o trojkatach
"""

class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.firstNeigh = None  # lewy sasiad - inny trojkat z ktorym sasiaduje nasz trojkat
        self.secondNeigh = None  # prawy sasiad
        self.thirdNeigh = None  # trzeci somsiad

    def whetherEdgesBelongToThisTriangle(self, edge):
        """
        Metoda sprawdza czy dana krawedz nalezy do tego trojkata
        :return:
        """
        edgeCheck = (min(edge[0],edge[1]), max(edge[0],edge[1]))
        edgeAB = (min(self.a, self.b), max(self.a, self.b))
        edgeBC = (min(self.b, self.c), max(self.b, self.c))
        edgeAC = (min(self.a, self.c), max(self.a, self.c))

        if edgeCheck == edgeAB or edgeCheck == edgeBC or edgeCheck == edgeAC:
            return True
        return False

    def findNewDiagonal(self, other):
        """
        Funkcja znajduje nowa przekatna pomiedzy dwoma polaczonymi trojkatami, o ile sie da to zrobic
        :param other:
        :return:
        """
        conectionEdge = self.findTheConnectingSection(other)  # znajduje krawedz laczaca

        firstPointDiagonal = None
        secondPointDiagonal = None

        if conectionEdge is not None:  # sprawdzam czy polaczecie z danym trojaktem istenieje
            edgePointA = conectionEdge[0]
            edgePointB = conectionEdge[1]

            # dla aktualnego trojkata
            if self.a == edgePointA and self.b == edgePointB or self.b == edgePointA and self.a == edgePointB:
                firstPointDiagonal = self.c

            if self.b == edgePointA and self.c == edgePointB or self.c == edgePointA and self.b == edgePointB:
                firstPointDiagonal = self.a

            if self.a == edgePointA and self.c == edgePointB or self.c == edgePointA and self.a == edgePointB:
                firstPointDiagonal = self.b

            # dla other
            if other.a == edgePointA and other.b == edgePointB or other.b == edgePointA and other.a == edgePointB:
                secondPointDiagonal = other.c

            if other.b == edgePointA and other.c == edgePointB or other.c == edgePointA and other.b == edgePointB:
                secondPointDiagonal = other.a

            if other.a == edgePointA and other.c == edgePointB or other.c == edgePointA and other.a == edgePointB:
                secondPointDiagonal = other.b

            return (firstPointDiagonal, secondPointDiagonal, edgePointA),\
                (firstPointDiagonal, secondPointDiagonal, edgePointB)

        return None, None

    def noNeigh(self):
        """
        Metoda zliacza ile nasz trojkat ma sasiadow
        :return:
        """
        counter = 0

        if self.firstNeigh is not None:
            counter += 1
        if self.secondNeigh is not None:
            counter += 1
        if self.thirdNeigh is not None:
            counter += 1
        return counter

    def whetherVertexExist(self,d):
        """
        Metoda sprawdza czy na trojkat posiada wierzcholek d
        :param d: Obiekt klasy Point
        :return: True/False w zaleznosci czy punkt nalezy do naszego trojkata
        """
        if self.a == d or self.b == d or self.c == d:
            return True
        return False

    def whetherNeighExist(self,other):
        """
        Metoda sprawdza czy juz mamy polaczenie z danym sasiadem
        :param other:
        :return:
        """
        if (self.firstNeigh is not None and self.firstNeigh == other) or \
                (self.secondNeigh is not None and self.secondNeigh == other) or \
                (self.thirdNeigh is not None and self.thirdNeigh == other):
            return True
        return False

    def findNewPlaceForNeigh(self):
        """
        Metoda sprawdza najblizszy wolny slot na danego sasiada
        :return: String z nazwa danego atrybutu ktorego mozemy uzyc do przechowania nowego sasiada
        """
        if self.firstNeigh is None:
            return 1
        if self.secondNeigh is None:
            return 2
        if self.thirdNeigh is None:
            return 3

        return None

    def whichNeigh(self, other):
        """
        Metoda sprawdza ktorym sasiadem z kolejnosci jestesmy dla innego trojkata
        :param other: Obiekt klasy Triangle
        :return: 1/2/3 - w zaleznosci kotrym sasiadem jestesmy
        """

        if other.firstNeigh is not None and other.firstNeigh == self:
            return 1
        if other.secondNeigh is not None and other.secondNeigh == self:
            return 2
        if other.thirdNeigh is not None and other.thirdNeigh == self:
            return 3

        return None

    def findTheConnectingSection(self, other):
        """
        Metoda znajduje dwa punkty symboluzujace odcinek o ile istnieje, ktory laczy dwa trojkaty
        :return: Krotka dwoch punktow symbolizujaca odcinek
        """
        sectionAB = (min(self.a, self.b), max(self.a, self.b))
        sectionBC = (min(self.b, self.c), max(self.b, self.c))
        sectionAC = (min(self.a, self.c), max(self.a, self.c))

        sectionABprim = (min(other.a, other.b), max(other.a, other.b))
        sectionBCprim = (min(other.b, other.c), max(other.b, other.c))
        sectionACprim = (min(other.a, other.c), max(other.a, other.c))

        if sectionAB == sectionABprim or sectionAB == sectionBCprim or sectionAB == sectionACprim:
            return sectionAB

        if sectionBC == sectionACprim or sectionBC == sectionABprim or sectionBC == sectionBCprim:
            return sectionBC

        if sectionAC == sectionACprim or sectionAC == sectionABprim or sectionAC == sectionBCprim:
            return sectionAC

        return None

    def desribeTheCircleOnTriangle(self):
        """
        Metoda opisujaca okrag na trojkacie, czyli po prostu na trzech punktach
        :return: Krotka zawierajaca obiekt klasy Point, gdzie trzymane sa wsporzedne srodka punktu, oraz promien do kwadratu
        """
        numerator_x_s = (self.a.x ** 2 + self.a.y ** 2) * (self.b.y - self.c.y) + \
                        (self.b.x ** 2 + self.b.y ** 2) * (self.c.y - self.a.y) + \
                        (self.c.x ** 2 + self.c.y ** 2) * (self.a.y - self.b.y)

        denominator_x_s = self.a.x * (self.b.y - self.c.y) + self.b.x * (self.c.y - self.a.y) + \
                          self.c.x * (self.a.y - self.b.y)

        x_s = 1 / 2 * (numerator_x_s / denominator_x_s)

        numerator_y_s = (self.a.x ** 2 + self.a.y ** 2) * (self.c.x - self.b.x) + \
                        (self.b.x ** 2 + self.b.y ** 2) * (self.a.x - self.c.x) + \
                        (self.c.x ** 2 + self.c.y ** 2) * (self.b.x - self.a.x)

        denominator_y_s = self.a.x * (self.b.y - self.c.y) + self.b.x * (self.c.y - self.a.y) + \
                          self.c.x * (self.a.y - self.b.y)

        y_s = 1 / 2 * (numerator_y_s / denominator_y_s)

        radiusOfCircleToSquare = (x_s - self.a.x) ** 2 + (y_s - self.a.y) ** 2

        return (x_s, y_s), radiusOfCircleToSquare

    def __eq__(self, other):
        if self.a == other.a and self.b == other.b and self.c == other.c or \
                self.a == other.b and self.b == other.a and self.c == other.c or \
                self.a == other.b and self.b == other.c and self.c == other.a or \
                self.a == other.a and self.b == other.c and self.c == other.b or \
                self.a == other.c and self.b == other.a and self.c == other.b or \
                self.a == other.c and self.b == other.b and self.c == other.a:  # znajduje wszystkie mozliwe permutacje
            return True
        return False

    def __str__(self):
        return f"A - {self.a}; B - {self.b}; C - {self.c}"

    def __hash__(self):
        return hash((self.a, self.b, self.c))
