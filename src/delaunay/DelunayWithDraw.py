from src.delaunay.LineFunction import LineFunction
from src.delaunay.Point import Point
from src.delaunay.Triangle import Triangle
from collections import deque
from math import sqrt


# dodatkowe importy - na potrzeby testow dzialania
from src.visualizer.main import Visualizer  # narzedzie do wizualizacji

from src.testy.TestsExtended import t_to_show_gifs

def extremePoints(polygon):
    """
    Funkcja wyznacza trzy skrajne punkty dla naszego wielokata prostego.
    :param polygon: tablica krotek punktów na płaszczyźnie euklidesowej podanych przeciwnie do ruchu wskazówek zegara
    :return: (a,b,c) - gdzie a,b,c sa to krotki punktow (x,y) na plaszyznie R^2 odpowiadaja odpowiednio: lewym dolnym, prawym dolnym i gornym wierzcholkiem
    """
    n = len(polygon)
    x_min = float('inf')
    x_max = float('-inf')
    y_min = float('inf')
    y_max = float('-inf')

    for a in polygon:
        if a[0] < x_min:
            x_min = a[0]
        if a[0] > x_max:
            x_max = a[0]
        if a[1] < y_min:
            y_min = a[1]
        if a[1] > y_max:
            y_max = a[1]

    a = abs(x_max - x_min)  # dlugosc boku prostokata
    b = abs(y_max - y_min)  # dlugosc boku prostokata

    left_bottom_point = Point(x_min - 2 * max(a, b), y_min - min(a, b), n)
    right_bottom_point = Point(x_max + 2 * max(a, b), y_min - min(a, b), n + 1)

    left_upper_rectangular_point = Point(x_min,y_max)  # lewy gory wierzcholek prostokata - nie daje tym punktom indeksow ponieaz sa tymczasowe
    right_upper_rectangular_point = Point(x_max, y_max)  # prawy gorny wierzcholek prostokata

    leftLine = LineFunction(left_bottom_point, left_upper_rectangular_point)
    rightLine = LineFunction(right_bottom_point, right_upper_rectangular_point)

    x = leftLine.findIntersection(rightLine)  # punkt przeciecia obu prostych

    middle_upper_point = Point(x, leftLine.calculateY(x), n + 2)

    return Triangle(left_bottom_point, right_bottom_point, middle_upper_point)


def createPointTab(polygon):
    """
    Funkcja tworzy tablice obiektow typu Point, aby moc wygodnie na nich dzialac
    :param polygon: Tablica punktow
    :return: Tablica obiektow typu Point
    """
    n = len(polygon)
    pointTab = []

    for i in range(n):
        point = polygon[i]
        newPoint = Point(point[0], point[1], i)
        pointTab.append(newPoint)

    return pointTab


def iniclizationVisited(triangleTab: set):
    """
    Funkcja sluzaca do inicializacji poczatkowej tablicy porzechowujacej informacje o tym czy bylismy w danym trojkacie
    :param triangleTab:
    :return:
    """
    visited = {}
    for triangle in triangleTab:
        visited[triangle] = False
    return visited


def bfsTriangleSearcherMapCreator(triangleMap: set, startTriangle: Triangle, startPoint: Point, visDelunay, E, K):
    """
    Funkcja przesukuje kolejne trojkaty w naszej aktualnej triangulacji aby wybrac te, ktore spelniaja warunek okregu
    :param triangleMap: Tabila trojkatow
    :param startTriangle: Trojkat od ktorego zaczynamy
    :param startPoint: Punkt z ktorym bedziemy poronywac kazdy trojkat
    :return: Mapa trojkatow na ktorych opisany okrag zawiera nasz punkt
    """
    visited = iniclizationVisited(
        triangleMap)  # slownik sluzaca do przechowywania infomracji o tym czy juz odwiedzalem dany trojkat
    toSearchTriangleMap = {startTriangle}  # slownik ktora zostanie uzupelniona trojkatami do przejzenia w przyszlosci

    Q = deque()
    Q.append(startTriangle)
    visited[startTriangle] = True

    while len(Q) > 0:
        v = Q.popleft()

        if v.firstNeigh is not None and v.firstNeigh in visited and visited[v.firstNeigh] is False:
            somethingTab = [(v.firstNeigh.a.x, v.firstNeigh.a.y), (v.firstNeigh.b.x, v.firstNeigh.b.y), (v.firstNeigh.c.x, v.firstNeigh.c.y)]
            something = visDelunay.add_polygon(somethingTab, color="yellow")
            K.append(something)

            #middleCircle, radiusOfCircleToSquare = v.firstNeigh.desribeTheCircleOnTriangle()
            #circlus = (middleCircle[0], middleCircle[1], sqrt(radiusOfCircleToSquare))
            #something = visDelunay.add_circle(circlus)
            #E.append(something)
            #K.append(something)

            if startPoint.doesPointContainedWithinTheCircle(v.firstNeigh):  # udalo sie
                visDelunay.remove_figure(K.pop())
                somethingTab = [(v.firstNeigh.a.x, v.firstNeigh.a.y), (v.firstNeigh.b.x, v.b.y), (v.firstNeigh.c.x, v.firstNeigh.c.y)]
                something = visDelunay.add_polygon(somethingTab, color="green")
                K.append(something)
                visDelunay.remove_figure(K.pop())
                toSearchTriangleMap.add(v.firstNeigh)

                visited[v.firstNeigh] = True  # interesuje mnie dodanie elementow do kolejki ktore spelniaja moje wymagania
                Q.append(v.firstNeigh)
            else:  # dodac kolor czerwony, ale tez dodac rysowanie
                visDelunay.remove_figure(K.pop())
                somethingTab = [(v.firstNeigh.a.x, v.firstNeigh.a.y), (v.firstNeigh.b.x, v.firstNeigh.b.y), (v.firstNeigh.c.x, v.firstNeigh.c.y)]
                something = visDelunay.add_polygon(somethingTab, color="red")
                K.append(something)
                visDelunay.remove_figure(K.pop())

        if v.secondNeigh is not None and v.secondNeigh in visited and visited[v.secondNeigh] is False:
            somethingTab = [(v.secondNeigh.a.x, v.secondNeigh.a.y), (v.secondNeigh.b.x, v.secondNeigh.b.y),
                            (v.secondNeigh.c.x, v.secondNeigh.c.y)]
            something = visDelunay.add_polygon(somethingTab, color="yellow")
            K.append(something)

            # middleCircle, radiusOfCircleToSquare = v.secondNeigh.desribeTheCircleOnTriangle()
            # circlus = (middleCircle[0], middleCircle[1], sqrt(radiusOfCircleToSquare))
            # something = visDelunay.add_circle(circlus)
            # E.append(something)
            # K.append(something)

            if startPoint.doesPointContainedWithinTheCircle(v.secondNeigh):
                visDelunay.remove_figure(K.pop())
                somethingTab = [(v.secondNeigh.a.x, v.secondNeigh.a.y), (v.secondNeigh.b.x, v.b.y), (v.secondNeigh.c.x, v.secondNeigh.c.y)]
                something = visDelunay.add_polygon(somethingTab, color="green")
                K.append(something)
                visDelunay.remove_figure(K.pop())
                toSearchTriangleMap.add(v.secondNeigh)

                visited[v.secondNeigh] = True
                Q.append(v.secondNeigh)

            else:
                visDelunay.remove_figure(K.pop())
                somethingTab = [(v.secondNeigh.a.x, v.secondNeigh.a.y), (v.secondNeigh.b.x, v.secondNeigh.b.y), (v.secondNeigh.c.x, v.secondNeigh.c.y)]
                something = visDelunay.add_polygon(somethingTab, color="red")
                K.append(something)
                visDelunay.remove_figure(K.pop())

        if v.thirdNeigh is not None and v.thirdNeigh in visited and visited[v.thirdNeigh] is False:
            somethingTab = [(v.thirdNeigh.a.x, v.thirdNeigh.a.y), (v.thirdNeigh.b.x, v.thirdNeigh.b.y),
                            (v.thirdNeigh.c.x, v.thirdNeigh.c.y)]
            something = visDelunay.add_polygon(somethingTab, color="yellow")
            K.append(something)

            # middleCircle, radiusOfCircleToSquare = v.thirdNeigh.desribeTheCircleOnTriangle()
            # circlus = (middleCircle[0], middleCircle[1], sqrt(radiusOfCircleToSquare))
            # something = visDelunay.add_circle(circlus)
            # E.append(something)
            # K.append(something)

            if startPoint.doesPointContainedWithinTheCircle(v.thirdNeigh):
                visDelunay.remove_figure(K.pop())
                somethingTab = [(v.thirdNeigh.a.x, v.thirdNeigh.a.y), (v.thirdNeigh.b.x, v.b.y), (v.thirdNeigh.c.x, v.thirdNeigh.c.y)]
                something = visDelunay.add_polygon(somethingTab, color="green")
                K.append(something)
                visDelunay.remove_figure(K.pop())

                toSearchTriangleMap.add(v.thirdNeigh)

                visited[v.thirdNeigh] = True
                Q.append(v.thirdNeigh)

            else:
                visDelunay.remove_figure(K.pop())
                somethingTab = [(v.thirdNeigh.a.x, v.thirdNeigh.a.y), (v.thirdNeigh.b.x, v.thirdNeigh.b.y), (v.thirdNeigh.c.x, v.thirdNeigh.c.y)]
                something = visDelunay.add_polygon(somethingTab, color="red")
                K.append(something)
                visDelunay.remove_figure(K.pop())

    return toSearchTriangleMap


def bfsTriangleEdgeRemover(triangleMap: set[Triangle], startTriangle: Triangle, startPoint: Point,
                           toSearchTriangleMap: set[Triangle], zeroTriangle: Triangle):
    """
    Funkcja sluzaca do usuwania krawedzi miedzy trojkatami a nastepnie stworzenie nowych trojkatow i zmienienie sasiadow na nowe trojkaty
    :param triangleMap:
    :param startTriangle:
    :param startPoint:
    :param toSearchTriangleMap:
    :param zeroTriangle:
    :return:
    """
    visited = iniclizationVisited(
        triangleMap)  # slownik sluzaca do przechowywania infomracji o tym czy juz odwiedzalem dany trojkat

    Q = deque()
    Q.append(startTriangle)
    visited[startTriangle] = True

    newTriangles = set()

    while len(Q) > 0:
        v = Q.popleft()
        triangleMap.remove(v)  # usuwam z mojej mapy trojaktow moj aktualny trojkat poniewaz beda zmieniane
        neighCounter = 0  # licznik ktory opisuje do ilu sasiadow moge isc

        if v.firstNeigh is not None and v.firstNeigh in visited and visited[v.firstNeigh] is False and v.firstNeigh in toSearchTriangleMap:
            visited[v.firstNeigh] = True
            Q.append(v.firstNeigh)
            neighCounter += 1

        if v.secondNeigh is not None and v.secondNeigh in visited and visited[v.secondNeigh] is False and v.secondNeigh in toSearchTriangleMap:
            visited[v.secondNeigh] = True
            Q.append(v.secondNeigh)
            neighCounter += 1

        if v.thirdNeigh is not None and v.thirdNeigh in visited and visited[v.thirdNeigh] is False and v.thirdNeigh in toSearchTriangleMap:
            visited[v.thirdNeigh] = True
            Q.append(v.thirdNeigh)
            neighCounter += 1

        if neighCounter != 3:  # znaczy ze aktualny trojkat jest brzegowym
            if v.firstNeigh is not None and not v.firstNeigh in toSearchTriangleMap:  # znaczy ze ten sasiad bede potrzebowal innego sasiada
                whichNeighWeAre = v.whichNeigh(v.firstNeigh)  # sprawdzamy ktorym sasiadem dokladnie jestesmy, aby moc to zmienic
                a, b = v.findTheConnectingSection(v.firstNeigh)  # znajduje punkty w ktorych lacza sie dane trojkaty

                newTrianlge = Triangle(a, b, startPoint)  # tworze nowy trojkat zaczynajac od laczenia
                newTrianlge.firstNeigh = v.firstNeigh  # dodaje do nowego trojkata starego sasiada - zawsze bedziemy go dodawac jako pierwszego
                triangleMap.add(newTrianlge)  # dodaje do zbioru nowo utworzony trojkat
                newTriangles.add(newTrianlge)  # dodaje do zbioru nowo utworzony trojkat tylko, ze w tym mam tylko nowo dodane trojkaty

                if whichNeighWeAre == 1:
                    v.firstNeigh.firstNeigh = newTrianlge
                if whichNeighWeAre == 2:
                    v.firstNeigh.secondNeigh = newTrianlge
                if whichNeighWeAre == 3:
                    v.firstNeigh.thirdNeigh = newTrianlge

            if v.secondNeigh is not None and not v.secondNeigh in toSearchTriangleMap:
                whichNeighWeAre = v.whichNeigh(v.secondNeigh)
                a, b = v.findTheConnectingSection(v.secondNeigh)

                newTrianlge = Triangle(a, b, startPoint)
                newTrianlge.firstNeigh = v.secondNeigh
                triangleMap.add(newTrianlge)
                newTriangles.add(newTrianlge)

                if whichNeighWeAre == 1:
                    v.secondNeigh.firstNeigh = newTrianlge
                if whichNeighWeAre == 2:
                    v.secondNeigh.secondNeigh = newTrianlge
                if whichNeighWeAre == 3:
                    v.secondNeigh.thirdNeigh = newTrianlge

            if v.thirdNeigh is not None and not v.thirdNeigh in toSearchTriangleMap:
                whichNeighWeAre = v.whichNeigh(v.thirdNeigh)
                a, b = v.findTheConnectingSection(v.thirdNeigh)

                newTrianlge = Triangle(a, b, startPoint)
                newTrianlge.firstNeigh = v.thirdNeigh
                triangleMap.add(newTrianlge)
                newTriangles.add(newTrianlge)

                if whichNeighWeAre == 1:
                    v.thirdNeigh.firstNeigh = newTrianlge
                if whichNeighWeAre == 2:
                    v.thirdNeigh.secondNeigh = newTrianlge
                if whichNeighWeAre == 3:
                    v.thirdNeigh.thirdNeigh = newTrianlge

            if v.firstNeigh is None or v.secondNeigh is None or v.thirdNeigh is None:  # znaczy ze naszym sasiadujacym trojkatem jest trojkat glowny - bo innej opcji nie ma
                a, b = v.findTheConnectingSection(zeroTriangle)

                newTrianlge = Triangle(a, b, startPoint)
                triangleMap.add(newTrianlge)
                newTriangles.add(newTrianlge)

    updateNeighOfTheTriangles(newTriangles)  # dodaje reszte sasiadow

    return triangleMap


def updateMapForOneTriangle(triangleMap: set, startPoint: Point, startTriangle: Triangle, zeroTriangle: Triangle):
    """
    Funkcja sluzy temu aby zaktualizowac mape trojkatow w przypadku kiedy ten dany trojkat spelnia jako jedyny zalozenia
    :param triangleMap: Mapa trojkatow
    :param startPoint: Punkt startowy
    :return:
    """
    triangleMap.remove(startTriangle)  # usuwam poczatkowy trojkat
    flag = False  # flaga sluzaca temu po prostu czy jaki kolwiek z warunkow nie bedzie spelniony
    newTriangles = set()

    if startTriangle.firstNeigh is not None:
        whichNeighWeAre = startTriangle.whichNeigh(startTriangle.firstNeigh)
        a, b = startTriangle.findTheConnectingSection(startTriangle.firstNeigh)

        newTrianlge = Triangle(a, b, startPoint)
        newTrianlge.firstNeigh = startTriangle.firstNeigh
        triangleMap.add(newTrianlge)
        newTriangles.add(newTrianlge)

        if whichNeighWeAre == 1:
            startTriangle.firstNeigh.firstNeigh = newTrianlge
        if whichNeighWeAre == 2:
            startTriangle.firstNeigh.secondNeigh = newTrianlge
        if whichNeighWeAre == 3:
            startTriangle.firstNeigh.thirdNeigh = newTrianlge

    else:
        flag = True

    if startTriangle.secondNeigh is not None:
        whichNeighWeAre = startTriangle.whichNeigh(startTriangle.secondNeigh)
        a, b = startTriangle.findTheConnectingSection(startTriangle.secondNeigh)

        newTrianlge = Triangle(a, b, startPoint)
        newTrianlge.firstNeigh = startTriangle.secondNeigh
        triangleMap.add(newTrianlge)
        newTriangles.add(newTrianlge)

        if whichNeighWeAre == 1:
            startTriangle.secondNeigh.firstNeigh = newTrianlge
        if whichNeighWeAre == 2:
            startTriangle.secondNeigh.secondNeigh = newTrianlge
        if whichNeighWeAre == 3:
            startTriangle.secondNeigh.thirdNeigh = newTrianlge

    else:
        flag = True

    if startTriangle.thirdNeigh is not None:
        whichNeighWeAre = startTriangle.whichNeigh(startTriangle.thirdNeigh)
        a, b = startTriangle.findTheConnectingSection(startTriangle.thirdNeigh)

        newTrianlge = Triangle(a, b, startPoint)
        newTrianlge.firstNeigh = startTriangle.thirdNeigh
        triangleMap.add(newTrianlge)
        newTriangles.add(newTrianlge)

        if whichNeighWeAre == 1:
            startTriangle.thirdNeigh.firstNeigh = newTrianlge
        if whichNeighWeAre == 2:
            startTriangle.thirdNeigh.secondNeigh = newTrianlge
        if whichNeighWeAre == 3:
            startTriangle.thirdNeigh.thirdNeigh = newTrianlge

    else:
        flag = True

    if flag:
        a, b = startTriangle.findTheConnectingSection(zeroTriangle)

        newTrianlge = Triangle(a, b, startPoint)
        triangleMap.add(newTrianlge)
        newTriangles.add(newTrianlge)

    updateNeighOfTheTriangles(newTriangles)  # dodaje reszte sasiadow do moich nowododanych trojkatow

    return triangleMap


def updateNeighOfTheTriangles(newTriangles: set[Triangle]):
    """
    Funkcja aktualizuje sasiadow naszych trojkatow aby cala reszta dzialala poprawnie
    :param newTriangles: Nowo utworzona mapa trojkatow ktora bede przegladal i patrzyl czy sie przypadkiem nie przecina
    :return: Nic, poniewaz wszystko jest zmieniane przez referencje
    """

    for triangleA in newTriangles:  # przegladam kazdego trojkata z kazdym i bede je porownywal
        for triangleB in newTriangles:
            if triangleA != triangleB:
                sectionTrangles = triangleA.findTheConnectingSection(triangleB)  # znajduje przeciecie o ile istnieje
                if sectionTrangles is not None:
                    if not triangleA.whetherNeighExist(triangleB):  # jesli nie mamy infomracji o przechowywaniu sasiada to musimy go koniecznie dodac
                        whichSlotIsFree = triangleA.findNewPlaceForNeigh()
                        if whichSlotIsFree == 1:
                            triangleA.firstNeigh = triangleB
                        if whichSlotIsFree == 2:
                            triangleA.secondNeigh = triangleB
                        if whichSlotIsFree == 3:
                            triangleA.thirdNeigh = triangleB
                    # w druga strone nie sprawdzam poniewaz i tak petla natrafie na taki przypadek


def findPointInTriangle(triangleMap, point: Point, visDelunay, E, G):
    """
    Funkcja znajduje trojkat w ktroym znajduje sie dany punkt
    :param triangleMap: Mapa obiektow klasy Trinalge
    :param point: Punkt w na ukladzie kartezianskim R^2
    :return: Obiekt klasy Triangle w ktorym znajduje sie dany punkt
    """

    for triangle in triangleMap:
        somethingTab = [(triangle.a.x,triangle.a.y),(triangle.b.x,triangle.b.y),(triangle.c.x,triangle.c.y)]
        something = visDelunay.add_polygon(somethingTab, color = "gray")
        E.append(something)
        G.append(something)

        if point.doesPointBelongToThisTriangle(triangle):
            visDelunay.remove_figure(G.pop())

            somethingTab = [(triangle.a.x,triangle.a.y),(triangle.b.x,triangle.b.y),(triangle.c.x,triangle.c.y)]
            something = visDelunay.add_polygon(somethingTab, color="orange")  # koloruje na inny kolor, zeby bylo wiadomo ze znalazlem ten punkt

            E.append(something)
            G.append(something)

            visDelunay.remove_figure(G.pop())

            return triangle

        visDelunay.remove_figure(G.pop())

    return None

def whetherCutAnyEdge(edgesSet: set[tuple[Point,Point]], edge: tuple[Point,Point]):
    """
    Funkcja sprawdza czy dany odcinek przecina jakas krawedz ze zbioru wszystkich krawedzi, danego wielokata
    :param edgesSet: Zbior krawedzi orginalnego wielokata
    :param edge: Krawedz
    :return: True jesli krawedz przecina krawedz z wielokata, False jesli nie przecina
    """

    for edgePoly in edgesSet:
        if whetherTwoEdgesCut(edgePoly, edge):  # dla kazdej krawedz sprawdzam czy nie jest przecinana
            return True

    return False

def deleteTriangle(cuttersMap: dict[tuple[Point,Point], list[Triangle]], triangle: Triangle):  # O(n)
    """
    Funkcja usuwa dla danego trojkat z cuttersMap, czyli dla kadej kraedzi ktora przecinal trzeba go usunac
    :return:
    """
    for edge in cuttersMap.keys():
        triangleList = cuttersMap[edge]
        if triangle in triangleList:
            triangleList.remove(triangle)

def updateCut(cuttersMap: dict[tuple[Point,Point], list[Triangle]], triangleFirst: Triangle, triangleSecond: Triangle):
    """
    Funkcja aktualizujaca przeciecia krawedzi poprzez dodanie dwoch nowych trojkatow
    :return:
    """
    for edge in cuttersMap.keys():
        if isCut(triangleFirst, edge):
            cuttersMap[edge].append(triangleFirst)

        if isCut(triangleSecond, edge):
            cuttersMap[edge].append(triangleSecond)

def convertCuttersEdge(cuttersMap: dict[tuple[Point,Point], list[Triangle]], triangleToDetector: set[Triangle],
                       edgesSet: set[tuple[Point,Point]]):  # O(n^2)
    """
    Funkcja zamienia przekatne danych trojkatow, ktore przecinaja krawedzie
    :param cuttersMap:
    :param triangleToDetector
    :param edgesSet
    :return:
    """
    for edge in cuttersMap.keys():  # przegladam wszystkie krawedzie
        k = len(cuttersMap[edge])
        if k > 0:  # to znaczy ze isteniaja jakies trojkaty, ktore przecinaja ta krawedz
            while len(cuttersMap[edge]) > 0:
                triangle = cuttersMap[edge][0]  # wyciagam pierwszy element z mapy

                if triangle.firstNeigh is not None and triangle.firstNeigh in cuttersMap[edge]:  # znajduje sasiada z ktrorym mam sie zamienic przekatna
                    trianglePointFirst, trianglePointSecond = triangle.findNewDiagonal(triangle.firstNeigh)

                    if trianglePointFirst is not None and trianglePointSecond is not None:

                        newDiagonal = (trianglePointFirst[0], trianglePointFirst[1])  # wyznaczam nowa przekatna

                        if not whetherCutAnyEdge(edgesSet, newDiagonal):  # znaczy to ze nie przecinam zadnej krawedzi ta zamiana

                            triangleFirst = Triangle(trianglePointFirst[0],
                                                     trianglePointFirst[1],
                                                     trianglePointFirst[2])

                            triangleSecond = Triangle(trianglePointSecond[0],
                                                      trianglePointSecond[1],
                                                      trianglePointSecond[2])

                            # dodaje sasiadow miedzy soba
                            triangleFirst.firstNeigh = triangleSecond
                            triangleSecond.firstNeigh = triangleFirst

                            if triangle.secondNeigh is not None:
                                whichNeighWeAre = triangle.whichNeigh(triangle.secondNeigh)

                                if triangle.secondNeigh.findTheConnectingSection(triangleFirst) is not None:

                                    whichSlotFree = triangleFirst.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleFirst.secondNeigh = triangle.secondNeigh
                                    if whichSlotFree == 3:
                                        triangleFirst.thirdNeigh = triangle.secondNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.secondNeigh.firstNeigh = triangleFirst
                                    if whichNeighWeAre == 2:
                                        triangle.secondNeigh.secondNeigh = triangleFirst
                                    if whichNeighWeAre == 3:
                                        triangle.secondNeigh.thirdNeigh = triangleFirst

                                elif triangle.secondNeigh.findTheConnectingSection(triangleSecond) is not None:

                                    whichSlotFree = triangleSecond.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleSecond.secondNeigh = triangle.secondNeigh
                                    if whichSlotFree == 3:
                                        triangleSecond.thirdNeigh = triangle.secondNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.secondNeigh.firstNeigh = triangleSecond
                                    if whichNeighWeAre == 2:
                                        triangle.secondNeigh.secondNeigh = triangleSecond
                                    if whichNeighWeAre == 3:
                                        triangle.secondNeigh.thirdNeigh = triangleSecond

                            if triangle.thirdNeigh is not None:
                                whichNeighWeAre = triangle.whichNeigh(triangle.thirdNeigh)

                                if triangle.thirdNeigh.findTheConnectingSection(triangleFirst) is not None:

                                    whichSlotFree = triangleFirst.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleFirst.secondNeigh = triangle.thirdNeigh
                                    if whichSlotFree == 3:
                                        triangleFirst.thirdNeigh = triangle.thirdNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.thirdNeigh.firstNeigh = triangleFirst
                                    if whichNeighWeAre == 2:
                                        triangle.thirdNeigh.secondNeigh = triangleFirst
                                    if whichNeighWeAre == 3:
                                        triangle.thirdNeigh.thirdNeigh = triangleFirst

                                elif triangle.thirdNeigh.findTheConnectingSection(triangleSecond) is not None:

                                    whichSlotFree = triangleSecond.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleSecond.secondNeigh = triangle.thirdNeigh
                                    if whichSlotFree == 3:
                                        triangleSecond.thirdNeigh = triangle.thirdNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.thirdNeigh.firstNeigh = triangleSecond
                                    if whichNeighWeAre == 2:
                                        triangle.thirdNeigh.secondNeigh = triangleSecond
                                    if whichNeighWeAre == 3:
                                        triangle.thirdNeigh.thirdNeigh = triangleSecond

                            if triangle.firstNeigh.firstNeigh is not None \
                                    and triangle.firstNeigh.firstNeigh != triangle:

                                whichNeighWeAre = triangle.firstNeigh.whichNeigh(triangle.firstNeigh.firstNeigh)

                                if triangle.firstNeigh.firstNeigh.findTheConnectingSection(triangleFirst) is not None:

                                    whichSlotFree = triangleFirst.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleFirst.secondNeigh = triangle.firstNeigh.firstNeigh
                                    if whichSlotFree == 3:
                                        triangleFirst.thirdNeigh = triangle.firstNeigh.firstNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.firstNeigh.firstNeigh.firstNeigh = triangleFirst
                                    if whichNeighWeAre == 2:
                                        triangle.firstNeigh.firstNeigh.secondNeigh = triangleFirst
                                    if whichNeighWeAre == 3:
                                        triangle.firstNeigh.firstNeigh.thirdNeigh = triangleFirst

                                elif triangle.firstNeigh.firstNeigh.findTheConnectingSection(triangleSecond) is not None:

                                    whichSlotFree = triangleSecond.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleSecond.secondNeigh = triangle.firstNeigh.firstNeigh
                                    if whichSlotFree == 3:
                                        triangleSecond.thirdNeigh = triangle.firstNeigh.firstNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.firstNeigh.firstNeigh.firstNeigh = triangleSecond
                                    if whichNeighWeAre == 2:
                                        triangle.firstNeigh.firstNeigh.secondNeigh = triangleSecond
                                    if whichNeighWeAre == 3:
                                        triangle.firstNeigh.firstNeigh.thirdNeigh = triangleSecond

                            if triangle.firstNeigh.secondNeigh is not None \
                                    and triangle.firstNeigh.secondNeigh != triangle:

                                whichNeighWeAre = triangle.firstNeigh.whichNeigh(triangle.firstNeigh.secondNeigh)

                                if triangle.firstNeigh.secondNeigh.findTheConnectingSection(triangleFirst) is not None:

                                    whichSlotFree = triangleFirst.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleFirst.secondNeigh = triangle.firstNeigh.secondNeigh
                                    if whichSlotFree == 3:
                                        triangleFirst.thirdNeigh = triangle.firstNeigh.secondNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.firstNeigh.secondNeigh.firstNeigh = triangleFirst
                                    if whichNeighWeAre == 2:
                                        triangle.firstNeigh.secondNeigh.secondNeigh = triangleFirst
                                    if whichNeighWeAre == 3:
                                        triangle.firstNeigh.secondNeigh.thirdNeigh = triangleFirst

                                elif triangle.firstNeigh.secondNeigh.findTheConnectingSection(
                                        triangleSecond) is not None:

                                    whichSlotFree = triangleSecond.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleSecond.secondNeigh = triangle.firstNeigh.secondNeigh
                                    if whichSlotFree == 3:
                                        triangleSecond.thirdNeigh = triangle.firstNeigh.secondNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.firstNeigh.secondNeigh.firstNeigh = triangleSecond
                                    if whichNeighWeAre == 2:
                                        triangle.firstNeigh.secondNeigh.secondNeigh = triangleSecond
                                    if whichNeighWeAre == 3:
                                        triangle.firstNeigh.secondNeigh.thirdNeigh = triangleSecond

                            if triangle.firstNeigh.thirdNeigh is not None \
                                    and triangle.firstNeigh.thirdNeigh != triangle:

                                whichNeighWeAre = triangle.firstNeigh.whichNeigh(triangle.firstNeigh.thirdNeigh)

                                if triangle.firstNeigh.thirdNeigh.findTheConnectingSection(triangleFirst) is not None:

                                    whichSlotFree = triangleFirst.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleFirst.secondNeigh = triangle.firstNeigh.thirdNeigh
                                    if whichSlotFree == 3:
                                        triangleFirst.thirdNeigh = triangle.firstNeigh.thirdNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.firstNeigh.thirdNeigh.firstNeigh = triangleFirst
                                    if whichNeighWeAre == 2:
                                        triangle.firstNeigh.thirdNeigh.secondNeigh = triangleFirst
                                    if whichNeighWeAre == 3:
                                        triangle.firstNeigh.thirdNeigh.thirdNeigh = triangleFirst

                                elif triangle.firstNeigh.thirdNeigh.findTheConnectingSection(
                                        triangleSecond) is not None:

                                    whichSlotFree = triangleSecond.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleSecond.secondNeigh = triangle.firstNeigh.thirdNeigh
                                    if whichSlotFree == 3:
                                        triangleSecond.thirdNeigh = triangle.firstNeigh.thirdNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.firstNeigh.thirdNeigh.firstNeigh = triangleSecond
                                    if whichNeighWeAre == 2:
                                        triangle.firstNeigh.thirdNeigh.secondNeigh = triangleSecond
                                    if whichNeighWeAre == 3:
                                        triangle.firstNeigh.thirdNeigh.thirdNeigh = triangleSecond

                            if triangle in triangleToDetector:
                                triangleToDetector.remove(triangle)

                            if triangle.firstNeigh in triangleToDetector:
                                triangleToDetector.remove(triangle.firstNeigh)

                            triangleToDetector.add(triangleFirst)
                            triangleToDetector.add(triangleSecond)

                            deleteTriangle(cuttersMap, triangle.firstNeigh)
                            deleteTriangle(cuttersMap, triangle)
                            updateCut(cuttersMap, triangleFirst, triangleSecond)

                elif triangle.secondNeigh is not None and triangle.secondNeigh in cuttersMap[edge]:
                    trianglePointFirst, trianglePointSecond = triangle.findNewDiagonal(triangle.secondNeigh)

                    if trianglePointFirst is not None and trianglePointSecond is not None:

                        newDiagonal = (trianglePointFirst[0], trianglePointFirst[1])  # wyznaczam nowa przekatna

                        if not whetherCutAnyEdge(edgesSet, newDiagonal):  # znaczy to ze nie przecinam zadnej krawedzi ta zamiana

                            triangleFirst = Triangle(trianglePointFirst[0],
                                                     trianglePointFirst[1],
                                                     trianglePointFirst[2])

                            triangleSecond = Triangle(trianglePointSecond[0],
                                                      trianglePointSecond[1],
                                                      trianglePointSecond[2])

                            # dodaje sasiadow miedzy soba
                            triangleFirst.firstNeigh = triangleSecond
                            triangleSecond.firstNeigh = triangleFirst

                            if triangle.firstNeigh is not None:
                                whichNeighWeAre = triangle.whichNeigh(triangle.firstNeigh)

                                if triangle.firstNeigh.findTheConnectingSection(triangleFirst) is not None:

                                    whichSlotFree = triangleFirst.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleFirst.secondNeigh = triangle.firstNeigh
                                    if whichSlotFree == 3:
                                        triangleFirst.thirdNeigh = triangle.firstNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.firstNeigh.firstNeigh = triangleFirst
                                    if whichNeighWeAre == 2:
                                        triangle.firstNeigh.secondNeigh = triangleFirst
                                    if whichNeighWeAre == 3:
                                        triangle.firstNeigh.thirdNeigh = triangleFirst

                                elif triangle.firstNeigh.findTheConnectingSection(triangleSecond) is not None:

                                    whichSlotFree = triangleSecond.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleSecond.secondNeigh = triangle.firstNeigh
                                    if whichSlotFree == 3:
                                        triangleSecond.thirdNeigh = triangle.firstNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.firstNeigh.firstNeigh = triangleSecond
                                    if whichNeighWeAre == 2:
                                        triangle.firstNeigh.secondNeigh = triangleSecond
                                    if whichNeighWeAre == 3:
                                        triangle.firstNeigh.thirdNeigh = triangleSecond

                            if triangle.thirdNeigh is not None:
                                whichNeighWeAre = triangle.whichNeigh(triangle.thirdNeigh)

                                if triangle.thirdNeigh.findTheConnectingSection(triangleFirst) is not None:

                                    whichSlotFree = triangleFirst.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleFirst.secondNeigh = triangle.thirdNeigh
                                    if whichSlotFree == 3:
                                        triangleFirst.thirdNeigh = triangle.thirdNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.thirdNeigh.firstNeigh = triangleFirst
                                    if whichNeighWeAre == 2:
                                        triangle.thirdNeigh.secondNeigh = triangleFirst
                                    if whichNeighWeAre == 3:
                                        triangle.thirdNeigh.thirdNeigh = triangleFirst

                                elif triangle.thirdNeigh.findTheConnectingSection(triangleSecond) is not None:

                                    whichSlotFree = triangleSecond.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleSecond.secondNeigh = triangle.thirdNeigh
                                    if whichSlotFree == 3:
                                        triangleSecond.thirdNeigh = triangle.thirdNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.thirdNeigh.firstNeigh = triangleSecond
                                    if whichNeighWeAre == 2:
                                        triangle.thirdNeigh.secondNeigh = triangleSecond
                                    if whichNeighWeAre == 3:
                                        triangle.thirdNeigh.thirdNeigh = triangleSecond

                            if triangle.secondNeigh.firstNeigh is not None \
                                    and triangle.secondNeigh.firstNeigh != triangle:

                                whichNeighWeAre = triangle.secondNeigh.whichNeigh(triangle.secondNeigh.firstNeigh)

                                if triangle.secondNeigh.firstNeigh.findTheConnectingSection(triangleFirst) is not None:

                                    whichSlotFree = triangleFirst.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleFirst.secondNeigh = triangle.secondNeigh.firstNeigh
                                    if whichSlotFree == 3:
                                        triangleFirst.thirdNeigh = triangle.secondNeigh.firstNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.secondNeigh.firstNeigh.firstNeigh = triangleFirst
                                    if whichNeighWeAre == 2:
                                        triangle.secondNeigh.firstNeigh.secondNeigh = triangleFirst
                                    if whichNeighWeAre == 3:
                                        triangle.secondNeigh.firstNeigh.thirdNeigh = triangleFirst

                                elif triangle.secondNeigh.firstNeigh.findTheConnectingSection(triangleSecond) is not None:

                                    whichSlotFree = triangleSecond.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleSecond.secondNeigh = triangle.secondNeigh.firstNeigh
                                    if whichSlotFree == 3:
                                        triangleSecond.thirdNeigh = triangle.secondNeigh.firstNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.secondNeigh.firstNeigh.firstNeigh = triangleSecond
                                    if whichNeighWeAre == 2:
                                        triangle.secondNeigh.firstNeigh.secondNeigh = triangleSecond
                                    if whichNeighWeAre == 3:
                                        triangle.secondNeigh.firstNeigh.thirdNeigh = triangleSecond

                            if triangle.secondNeigh.secondNeigh is not None \
                                    and triangle.secondNeigh.secondNeigh != triangle:

                                whichNeighWeAre = triangle.secondNeigh.whichNeigh(triangle.secondNeigh.secondNeigh)

                                if triangle.secondNeigh.secondNeigh.findTheConnectingSection(triangleFirst) is not None:

                                    whichSlotFree = triangleFirst.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleFirst.secondNeigh = triangle.secondNeigh.secondNeigh
                                    if whichSlotFree == 3:
                                        triangleFirst.thirdNeigh = triangle.secondNeigh.secondNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.secondNeigh.secondNeigh.firstNeigh = triangleFirst
                                    if whichNeighWeAre == 2:
                                        triangle.secondNeigh.secondNeigh.secondNeigh = triangleFirst
                                    if whichNeighWeAre == 3:
                                        triangle.secondNeigh.secondNeigh.thirdNeigh = triangleFirst

                                elif triangle.secondNeigh.secondNeigh.findTheConnectingSection(
                                        triangleSecond) is not None:

                                    whichSlotFree = triangleSecond.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleSecond.secondNeigh = triangle.secondNeigh.secondNeigh
                                    if whichSlotFree == 3:
                                        triangleSecond.thirdNeigh = triangle.secondNeigh.secondNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.secondNeigh.secondNeigh.firstNeigh = triangleSecond
                                    if whichNeighWeAre == 2:
                                        triangle.secondNeigh.secondNeigh.secondNeigh = triangleSecond
                                    if whichNeighWeAre == 3:
                                        triangle.secondNeigh.secondNeigh.thirdNeigh = triangleSecond

                            if triangle.secondNeigh.thirdNeigh is not None \
                                    and triangle.secondNeigh.thirdNeigh != triangle:

                                whichNeighWeAre = triangle.secondNeigh.whichNeigh(triangle.secondNeigh.thirdNeigh)

                                if triangle.secondNeigh.thirdNeigh.findTheConnectingSection(triangleFirst) is not None:

                                    whichSlotFree = triangleFirst.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleFirst.secondNeigh = triangle.secondNeigh.thirdNeigh
                                    if whichSlotFree == 3:
                                        triangleFirst.thirdNeigh = triangle.secondNeigh.thirdNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.secondNeigh.thirdNeigh.firstNeigh = triangleFirst
                                    if whichNeighWeAre == 2:
                                        triangle.secondNeigh.thirdNeigh.secondNeigh = triangleFirst
                                    if whichNeighWeAre == 3:
                                        triangle.secondNeigh.thirdNeigh.thirdNeigh = triangleFirst

                                elif triangle.secondNeigh.thirdNeigh.findTheConnectingSection(
                                        triangleSecond) is not None:

                                    whichSlotFree = triangleSecond.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleSecond.secondNeigh = triangle.secondNeigh.thirdNeigh
                                    if whichSlotFree == 3:
                                        triangleSecond.thirdNeigh = triangle.secondNeigh.thirdNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.secondNeigh.thirdNeigh.firstNeigh = triangleSecond
                                    if whichNeighWeAre == 2:
                                        triangle.secondNeigh.thirdNeigh.secondNeigh = triangleSecond
                                    if whichNeighWeAre == 3:
                                        triangle.secondNeigh.thirdNeigh.thirdNeigh = triangleSecond

                            if triangle.secondNeigh in triangleToDetector:
                                triangleToDetector.remove(triangle.secondNeigh)

                            if triangle in triangleToDetector:
                                triangleToDetector.remove(triangle)

                            triangleToDetector.add(triangleFirst)
                            triangleToDetector.add(triangleSecond)

                            deleteTriangle(cuttersMap, triangle.secondNeigh)
                            deleteTriangle(cuttersMap, triangle)
                            updateCut(cuttersMap, triangleFirst, triangleSecond)

                elif triangle.thirdNeigh is not None and triangle.thirdNeigh in cuttersMap[edge]:
                    trianglePointFirst, trianglePointSecond = triangle.findNewDiagonal(triangle.thirdNeigh)

                    if trianglePointFirst is not None and trianglePointSecond is not None:

                        newDiagonal = (trianglePointFirst[0], trianglePointFirst[1])  # wyznaczam nowa przekatna

                        if not whetherCutAnyEdge(edgesSet, newDiagonal):  # znaczy to ze nie przecinam zadnej krawedzi ta zamiana

                            triangleFirst = Triangle(trianglePointFirst[0],
                                                     trianglePointFirst[1],
                                                     trianglePointFirst[2])

                            triangleSecond = Triangle(trianglePointSecond[0],
                                                      trianglePointSecond[1],
                                                      trianglePointSecond[2])

                            # dodaje sasiadow miedzy soba
                            triangleFirst.firstNeigh = triangleSecond
                            triangleSecond.firstNeigh = triangleFirst

                            if triangle.firstNeigh is not None:
                                whichNeighWeAre = triangle.whichNeigh(triangle.firstNeigh)

                                if triangle.firstNeigh.findTheConnectingSection(triangleFirst) is not None:

                                    whichSlotFree = triangleFirst.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleFirst.secondNeigh = triangle.firstNeigh
                                    if whichSlotFree == 3:
                                        triangleFirst.thirdNeigh = triangle.firstNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.firstNeigh.firstNeigh = triangleFirst
                                    if whichNeighWeAre == 2:
                                        triangle.firstNeigh.secondNeigh = triangleFirst
                                    if whichNeighWeAre == 3:
                                        triangle.firstNeigh.thirdNeigh = triangleFirst

                                elif triangle.firstNeigh.findTheConnectingSection(triangleSecond) is not None:

                                    whichSlotFree = triangleSecond.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleSecond.secondNeigh = triangle.firstNeigh
                                    if whichSlotFree == 3:
                                        triangleSecond.thirdNeigh = triangle.firstNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.firstNeigh.firstNeigh = triangleSecond
                                    if whichNeighWeAre == 2:
                                        triangle.firstNeigh.secondNeigh = triangleSecond
                                    if whichNeighWeAre == 3:
                                        triangle.firstNeigh.thirdNeigh = triangleSecond

                            if triangle.secondNeigh is not None:
                                whichNeighWeAre = triangle.whichNeigh(triangle.secondNeigh)

                                if triangle.secondNeigh.findTheConnectingSection(triangleFirst) is not None:

                                    whichSlotFree = triangleFirst.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleFirst.secondNeigh = triangle.secondNeigh
                                    if whichSlotFree == 3:
                                        triangleFirst.thirdNeigh = triangle.secondNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.secondNeigh.firstNeigh = triangleFirst
                                    if whichNeighWeAre == 2:
                                        triangle.secondNeigh.secondNeigh = triangleFirst
                                    if whichNeighWeAre == 3:
                                        triangle.secondNeigh.thirdNeigh = triangleFirst

                                elif triangle.secondNeigh.findTheConnectingSection(triangleSecond) is not None:

                                    whichSlotFree = triangleSecond.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleSecond.secondNeigh = triangle.secondNeigh
                                    if whichSlotFree == 3:
                                        triangleSecond.thirdNeigh = triangle.secondNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.secondNeigh.firstNeigh = triangleSecond
                                    if whichNeighWeAre == 2:
                                        triangle.secondNeigh.secondNeigh = triangleSecond
                                    if whichNeighWeAre == 3:
                                        triangle.secondNeigh.thirdNeigh = triangleSecond

                            if triangle.thirdNeigh.firstNeigh is not None \
                                    and triangle.thirdNeigh.firstNeigh != triangle:

                                whichNeighWeAre = triangle.thirdNeigh.whichNeigh(triangle.thirdNeigh.firstNeigh)

                                if triangle.thirdNeigh.firstNeigh.findTheConnectingSection(triangleFirst) is not None:

                                    whichSlotFree = triangleFirst.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleFirst.secondNeigh = triangle.thirdNeigh.firstNeigh
                                    if whichSlotFree == 3:
                                        triangleFirst.thirdNeigh = triangle.thirdNeigh.firstNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.thirdNeigh.firstNeigh.firstNeigh = triangleFirst
                                    if whichNeighWeAre == 2:
                                        triangle.thirdNeigh.firstNeigh.secondNeigh = triangleFirst
                                    if whichNeighWeAre == 3:
                                        triangle.thirdNeigh.firstNeigh.thirdNeigh = triangleFirst

                                elif triangle.thirdNeigh.firstNeigh.findTheConnectingSection(triangleSecond) is not None:

                                    whichSlotFree = triangleSecond.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleSecond.secondNeigh = triangle.thirdNeigh.firstNeigh
                                    if whichSlotFree == 3:
                                        triangleSecond.thirdNeigh = triangle.thirdNeigh.firstNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.thirdNeigh.firstNeigh.firstNeigh = triangleSecond
                                    if whichNeighWeAre == 2:
                                        triangle.thirdNeigh.firstNeigh.secondNeigh = triangleSecond
                                    if whichNeighWeAre == 3:
                                        triangle.thirdNeigh.firstNeigh.thirdNeigh = triangleSecond

                            if triangle.thirdNeigh.secondNeigh is not None \
                                    and triangle.thirdNeigh.secondNeigh != triangle:

                                whichNeighWeAre = triangle.thirdNeigh.whichNeigh(triangle.thirdNeigh.secondNeigh)

                                if triangle.thirdNeigh.secondNeigh.findTheConnectingSection(triangleFirst) is not None:

                                    whichSlotFree = triangleFirst.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleFirst.secondNeigh = triangle.thirdNeigh.secondNeigh
                                    if whichSlotFree == 3:
                                        triangleFirst.thirdNeigh = triangle.thirdNeigh.secondNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.thirdNeigh.secondNeigh.firstNeigh = triangleFirst
                                    if whichNeighWeAre == 2:
                                        triangle.thirdNeigh.secondNeigh.secondNeigh = triangleFirst
                                    if whichNeighWeAre == 3:
                                        triangle.thirdNeigh.secondNeigh.thirdNeigh = triangleFirst

                                elif triangle.thirdNeigh.secondNeigh.findTheConnectingSection(
                                        triangleSecond) is not None:

                                    whichSlotFree = triangleSecond.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleSecond.secondNeigh = triangle.thirdNeigh.secondNeigh
                                    if whichSlotFree == 3:
                                        triangleSecond.thirdNeigh = triangle.thirdNeigh.secondNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.thirdNeigh.secondNeigh.firstNeigh = triangleSecond
                                    if whichNeighWeAre == 2:
                                        triangle.thirdNeigh.secondNeigh.secondNeigh = triangleSecond
                                    if whichNeighWeAre == 3:
                                        triangle.thirdNeigh.secondNeigh.thirdNeigh = triangleSecond

                            if triangle.thirdNeigh.thirdNeigh is not None \
                                    and triangle.thirdNeigh.thirdNeigh != triangle:

                                whichNeighWeAre = triangle.thirdNeigh.whichNeigh(triangle.thirdNeigh.thirdNeigh)

                                if triangle.thirdNeigh.thirdNeigh.findTheConnectingSection(triangleFirst) is not None:

                                    whichSlotFree = triangleFirst.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleFirst.secondNeigh = triangle.thirdNeigh.thirdNeigh
                                    if whichSlotFree == 3:
                                        triangleFirst.thirdNeigh = triangle.thirdNeigh.thirdNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.thirdNeigh.thirdNeigh.firstNeigh = triangleFirst
                                    if whichNeighWeAre == 2:
                                        triangle.thirdNeigh.thirdNeigh.secondNeigh = triangleFirst
                                    if whichNeighWeAre == 3:
                                        triangle.thirdNeigh.thirdNeigh.thirdNeigh = triangleFirst

                                elif triangle.thirdNeigh.thirdNeigh.findTheConnectingSection(
                                        triangleSecond) is not None:

                                    whichSlotFree = triangleSecond.findNewPlaceForNeigh()

                                    if whichSlotFree == 2:
                                        triangleSecond.secondNeigh = triangle.thirdNeigh.thirdNeigh
                                    if whichSlotFree == 3:
                                        triangleSecond.thirdNeigh = triangle.thirdNeigh.thirdNeigh

                                    if whichNeighWeAre == 1:
                                        triangle.thirdNeigh.thirdNeigh.firstNeigh = triangleSecond
                                    if whichNeighWeAre == 2:
                                        triangle.thirdNeigh.thirdNeigh.secondNeigh = triangleSecond
                                    if whichNeighWeAre == 3:
                                        triangle.thirdNeigh.thirdNeigh.thirdNeigh = triangleSecond

                            if triangle in triangleToDetector:
                                triangleToDetector.remove(triangle)

                            if triangle.thirdNeigh in triangleToDetector:
                                triangleToDetector.remove(triangle.thirdNeigh)

                            triangleToDetector.add(triangleFirst)
                            triangleToDetector.add(triangleSecond)

                            deleteTriangle(cuttersMap, triangle.thirdNeigh)
                            deleteTriangle(cuttersMap, triangle)
                            updateCut(cuttersMap, triangleFirst, triangleSecond)

                if triangle in cuttersMap[edge]:
                    cuttersMap[edge].remove(triangle)
                    cuttersMap[edge].append(triangle)

    return triangleToDetector


def dfsFindPoint_draw(triangleMap: set[Triangle], point: Point, visDelunay, E, G):
    """
    Funkcja znjadujaca trojkat na ktorym lezy nasz punkt algortem DFS, ale w kolejnosci odpowiedniej dlugosci
    :param triangleMap:
    :param point:
    :return:
    """
    visited = iniclizationVisited(triangleMap)

    found = False
    searchedTriangle = None

    def dfsStart(triangleMap: set[Triangle]):
        for triangle in triangleMap:
            if visited[triangle] is False:
                dfsVisit(triangleMap, triangle)

                if found:
                    break

    def dfsVisit(triangleMap: set[Triangle], triangle: Triangle):
        nonlocal point, searchedTriangle, found, visDelunay, E, G

        somethingTab = [(triangle.a.x, triangle.a.y), (triangle.b.x, triangle.b.y), (triangle.c.x, triangle.c.y)]
        something = visDelunay.add_polygon(somethingTab, color="gray")
        E.append(something)
        G.append(something)

        visited[triangle] = True

        if point.doesPointBelongToThisTriangle(triangle):
            visDelunay.remove_figure(G.pop())

            somethingTab = [(triangle.a.x, triangle.a.y), (triangle.b.x, triangle.b.y), (triangle.c.x, triangle.c.y)]
            something = visDelunay.add_polygon(somethingTab,
                                               color="orange")

            E.append(something)
            G.append(something)

            visDelunay.remove_figure(G.pop())

            searchedTriangle = triangle
            found = True

        if not found:

            visDelunay.remove_figure(G.pop())

            minimumPoint = None
            miniumDistance = None
            who_started = -1

            if triangle.firstNeigh is not None and visited[triangle.firstNeigh] is False:
                minimumPointAct = triangle.firstNeigh.findTheNearestPoint(point)
                distanceAct = sqrt((minimumPointAct.x - point.x) ** 2 + (minimumPointAct.y - point.y) ** 2)

                miniumDistance = distanceAct
                minimumPoint = minimumPointAct
                who_started = 1

            if triangle.secondNeigh is not None and visited[triangle.secondNeigh] is False:
                minimumPointAct = triangle.secondNeigh.findTheNearestPoint(point)
                if minimumPoint is not None:
                    distanceAct = sqrt((minimumPointAct.x - minimumPoint.x) ** 2 + (minimumPointAct.y - minimumPoint.y) ** 2)

                    if distanceAct < miniumDistance:
                        miniumDistance = distanceAct
                        minimumPoint = minimumPointAct
                        who_started = 2
                else:
                    distanceAct = sqrt((minimumPointAct.x - point.x) ** 2 + (minimumPointAct.y - point.y) ** 2)

                    miniumDistance = distanceAct
                    minimumPoint = minimumPointAct
                    who_started = 2

            if triangle.thirdNeigh is not None and visited[triangle.thirdNeigh] is False:
                minimumPointAct = triangle.secondNeigh.findTheNearestPoint(point)
                if minimumPoint is not None:
                    distanceAct = sqrt((minimumPointAct.x - minimumPoint.x) ** 2 + (minimumPointAct.y - minimumPoint.y) ** 2)

                    if distanceAct < miniumDistance:
                        who_started = 3
                else:
                    who_started = 3

            if who_started == 1 and not found:
                dfsVisit(triangleMap, triangle.firstNeigh)

            if who_started == 2 and not found:
                dfsVisit(triangleMap, triangle.secondNeigh)

            if who_started == 3 and not found:
                dfsVisit(triangleMap, triangle.thirdNeigh)

            if triangle.firstNeigh is not None and visited[triangle.firstNeigh] is False and not found:
                dfsVisit(triangleMap, triangle.firstNeigh)

            if triangle.secondNeigh is not None and visited[triangle.secondNeigh] is False and not found:
                dfsVisit(triangleMap, triangle.secondNeigh)

            if triangle.thirdNeigh is not None and visited[triangle.thirdNeigh] is False and not found:
                dfsVisit(triangleMap, triangle.thirdNeigh)

    dfsStart(triangleMap)
    return searchedTriangle


def inicializeWithStartTriangle(pointTab, zeroTriangle):
    """
    Funkcja inicializuje poczatkowe wartosci dla slownika trojkatow, ktory bedzie dalej rozwijany przez caly proces trwania naszego algortymu
    :param pointTab:
    :param zeroTriangle:
    :return:
    """
    tran1 = Triangle(zeroTriangle.a, zeroTriangle.b, pointTab[0])
    tran2 = Triangle(zeroTriangle.a, zeroTriangle.c, pointTab[0])
    tran3 = Triangle(zeroTriangle.c, zeroTriangle.b, pointTab[0])

    # ustalam sasiadow poszczegolnych trojkatow
    tran1.firstNeigh = tran2
    tran1.secondNeigh = tran3

    tran2.firstNeigh = tran3
    tran2.secondNeigh = tran1

    tran3.firstNeigh = tran2
    tran3.secondNeigh = tran1

    return {tran1, tran2, tran3}


def deletedBorder(triangleMap: set[Triangle], zeroTriangle: Triangle):
    """
    Funkcja usuuwa obramowanie
    :return:
    """
    triagleSol = set()
    for triangle in triangleMap:
        if not triangle.whetherVertexExist(zeroTriangle.a) and \
                not triangle.whetherVertexExist(zeroTriangle.b) and \
                not triangle.whetherVertexExist(zeroTriangle.c):
            triagleSol.add(triangle)

    return triagleSol
def createSetEdges_draw(pointTab: list[Point], visDelone):
    """
    Funkcja dla poczatkowego zbioru punktow, tworzy poczatkowy zbior krawedzi.
    :param pointTab:
    :return: Tablica krawedzi krotek obietkow typu Point, ktore symbolizuja dane krawedzie
    """
    n = len(pointTab)
    edgesSet = set()  # zbior krawedzi
    edges = []

    for i in range(n - 1):
        point1 = pointTab[i]
        point2 = pointTab[i + 1]

        edge = ((point1.x, point1.y), (point2.x, point2.y))
        edges.append(edge)

        edgesSet.add((point1, point2))

    point1 = pointTab[-1]
    point2 = pointTab[0]

    edge = ((point1.x, point1.y), (point2.x, point2.y))
    edges.append(edge)

    edgesSet.add((point1, point2))

    visDelone.add_line_segment(edges, color="brown")

    return edgesSet
def mat_det_2x2(a: Point, b: Point, c: Point): #wyznacznik 2x2
    return (a.x-c.x)*(b.y-c.y)-(a.y-c.y)*(b.x-c.x)

def get_orientation(actuall_orientation):
    if actuall_orientation > 0: return 1
    elif actuall_orientation < 0: return -1
    return 0
def whetherTwoEdgesCut(edgeA: tuple[Point, Point], edgeB: tuple[Point, Point]):

    if edgeA[0] == edgeB[0] or edgeA[0] == edgeB[1] or edgeA[1] == edgeB[0] or edgeA[1] == edgeB[1]: return False

    o1 = get_orientation(mat_det_2x2(edgeA[0],edgeA[1],edgeB[0]))
    o2 = get_orientation(mat_det_2x2(edgeA[0],edgeA[1],edgeB[1]))

    o3 = get_orientation(mat_det_2x2(edgeB[0],edgeB[1],edgeA[0]))
    o4 = get_orientation(mat_det_2x2(edgeB[0],edgeB[1],edgeA[1]))

    if o1 != o2 and o3 != o4:
        return True

    return False

def isCut(triangle: Triangle, edge: tuple[Point,Point]):
    """
    Funkcja odpowiada na pytania czy dany trojkat, przecina dana krawedz.
    Funkcja ta bedzie pomocna przy procedurze odzyskiwania krawedzi
    :return: True/False w zaleznosci czy dany punkt przecina dana krawedz
    """
    edgeAB = (triangle.a, triangle.b)
    edgeAC = (triangle.a, triangle.c)
    edgeBC = (triangle.b, triangle.c)

    if whetherTwoEdgesCut(edgeAB, edge) or \
            whetherTwoEdgesCut(edgeAC, edge) or \
            whetherTwoEdgesCut(edgeBC, edge):
        return True
    return False

def findCuttersEdges(edgesSet: set[tuple[Point,Point]], triangleToDetector: set[Triangle]):  # O(n)
    """
    Funkcja znajduje wszystkie trojkaty ktore przecinaja krawedzie naszej figry
    :param edgesSet:
    :param triangleToDetector:
    :return: Mapa z kluczem jako krawedz, a z wartosciami jako lista trojkatow ktore przecinaja dana krawedz
    """
    cuttersMap = dict()

    for edge in edgesSet:
        cuttersMap[edge] = []  # tworze to jako tablice aby moc latwo iterowac sie po tym

        for triangle in triangleToDetector:
            if isCut(triangle, edge):  # dany trojkat przecina dana krawedz
                cuttersMap[edge].append(triangle)

    return cuttersMap

def createSetEdgesToPrintAll(triagleSol: set[Triangle]):
    """
    Funkcja tworzy zbior krwawedzi ze wszystkich trojkatow obiektow Point
    :param triagleSol:
    :return:
    """
    edgesSet = set()
    for triangle in triagleSol:
        if not (triangle.a,triangle.b) in edgesSet and not (triangle.b,triangle.a) in edgesSet:
            edgesSet.add((triangle.a,triangle.b))

        if not (triangle.a,triangle.c) in edgesSet and not (triangle.c,triangle.a) in edgesSet:
            edgesSet.add((triangle.a,triangle.c))

        if not (triangle.b, triangle.c) in edgesSet and not (triangle.c, triangle.b) in edgesSet:
            edgesSet.add((triangle.b, triangle.c))

    return edgesSet

def createListEdges(edgesSet: set[(Point,Point)]):
    """
    Funcja przerabia zbior punktow na prawdzia liste krotek krawedzi
    :param edgesSet:
    :return:
    """
    listEdges = []

    for edges in edgesSet:
        point1 = edges[0]
        point2 = edges[1]
        listEdges.append( ((point1.x,point1.y),(point2.x,point2.y)) )

    return listEdges

def printTriangles(triangleMap: set[Triangle],visDelunay, E, D, colorMe = "black"):
    lineSegments = []

    for triangle in triangleMap:
        segmentAB = ((triangle.a.x, triangle.a.y), (triangle.b.x, triangle.b.y))
        segmentBC = ((triangle.b.x, triangle.b.y), (triangle.c.x, triangle.c.y))
        segmentAC = ((triangle.a.x, triangle.a.y), (triangle.c.x, triangle.c.y))
        lineSegments.append(segmentAB)
        lineSegments.append(segmentBC)
        lineSegments.append(segmentAC)

    something = visDelunay.add_line_segment(lineSegments, color = colorMe)
    E.append(something)
    D.append(something)


def printSolution(listEdges, polygon):
    """
    Funkcja rysujaca nasza koncowa triangulacje
    :param listEdges:
    :param polygon: Lista punktow naszego wielokata
    :return: Rysowanie naszego elementu
    """
    vis = Visualizer()
    vis.add_line_segment(listEdges, color="black")
    vis.add_point(polygon, color = "blue")
    vis.show()

def selectTriangle(triangleToDetector: set[Triangle], edgesSet: set[tuple[Point,Point]] ):
    """
    Funkcja wyznacza odpowiednie trojkaty, ktore sa brzegowe.
    :return:
    """
    toDeleteTriangles = set()  # zbior trojkatow do usuniecia
    borderTriangles = set()  # zbior brzegowych trojkatow
    for edge in edgesSet:
        for triangle in triangleToDetector:
            # sprawdzam czy dana krawedz jest boczna a natepnie czy, trojkat jest prawidlowy
            if triangle.whetherEdgesBelongToThisTriangle(edge):
                if not triangle.checkTriangleCorrect(edge):
                    toDeleteTriangles.add(triangle)
                else:
                    borderTriangles.add(triangle)

    # usuwam z glownego zbioru trojkaty ktore nie spelniaja wymogow
    for triangle in toDeleteTriangles:
        triangleToDetector.remove(triangle)

    if len(toDeleteTriangles) > 0:
        visited = iniclizationVisited(toDeleteTriangles)
        v = toDeleteTriangles.pop()

        Q = deque()
        Q.append(v)

        visited[v] = True

        while len(Q) > 0:
            triangle = Q.popleft()

            if triangle.firstNeigh is not None and not triangle.firstNeigh in borderTriangles:

                if triangle.firstNeigh in visited and visited[triangle.firstNeigh] is False:
                    visited[triangle.firstNeigh] = True
                    toDeleteTriangles.add(triangle.firstNeigh)
                    Q.append(triangle.firstNeigh)

                if not triangle.firstNeigh in visited:
                    visited[triangle.firstNeigh] = True
                    toDeleteTriangles.add(triangle.firstNeigh)
                    Q.append(triangle.firstNeigh)

            if triangle.secondNeigh is not None and not triangle.secondNeigh in borderTriangles:

                if triangle.secondNeigh in visited and visited[triangle.secondNeigh] is False:
                    visited[triangle.secondNeigh] = True
                    toDeleteTriangles.add(triangle.secondNeigh)
                    Q.append(triangle.secondNeigh)

                if not triangle.secondNeigh in visited:
                    visited[triangle.secondNeigh] = True
                    toDeleteTriangles.add(triangle.secondNeigh)
                    Q.append(triangle.secondNeigh)

            if triangle.thirdNeigh is not None and not triangle.thirdNeigh in borderTriangles:

                if triangle.thirdNeigh in visited and visited[triangle.thirdNeigh] is False:
                    visited[triangle.thirdNeigh] = True
                    toDeleteTriangles.add(triangle.thirdNeigh)
                    Q.append(triangle.thirdNeigh)

                if not triangle.thirdNeigh in visited:
                    visited[triangle.thirdNeigh] = True
                    toDeleteTriangles.add(triangle.thirdNeigh)
                    Q.append(triangle.thirdNeigh)

            # potwarzam czystki
            for triangle in toDeleteTriangles:
                if triangle in triangleToDetector:
                    triangleToDetector.remove(triangle)




def triangleToList(triangles: set[Triangle]):
    """
    Funkcja zamienia wynik trojkatow odpowiednio na zbior ktorek (a,b,c), gdzie oznaczaja one zbior trojkatow
    :return:
    """
    sol = []
    for triangle in triangles:
        sol.append((triangle.a.idPoint, triangle.b.idPoint, triangle.c.idPoint))
    return sol

def delunay_draw(polygon: list):
    """
    Funkcja oblicza triangulacji Delunay'a oraz wizualizujaca go
    :param polygon: tablica krotek punktów na płaszczyźnie euklidesowej podanych przeciwnie do ruchu wskazówek zegara - nasz wielokąt
    :return: wartość bool - true, jeśli wielokąt jest monotoniczny i false jeśli nie jest
    """
    visDelunay = Visualizer()
    visDelunay.add_grid()
    visDelunay.add_title('Triangulation Delunay algorithm')
    visDelunay.add_point(polygon, color = "blue")   # dodaje nasze punkty poczatowe

    E = []
    D = deque()  # stos sluzacy do przechowywania starego uzlozenia trojkatow
    G = deque()  # stos tymaczosowy

    n = len(polygon)

    zeroTriangle = extremePoints(polygon)  # nastepuje znalezienie trojkata, ktory obejmuje wszystkie punkty

    pointTab = createPointTab(polygon)

    # tworze zbior krawedzi razem z wizualizacja
    edgesSet = createSetEdges_draw(pointTab, visDelunay)

    triangleMap = inicializeWithStartTriangle(pointTab,zeroTriangle)  # mapa aktualnie znajdujacych sie trojkatow w triangulacji


    printTriangles(triangleMap, visDelunay,E, D)

    for i in range(1, n):  # przegladam nasze kolejne punkty
        visDelunay.add_point((pointTab[i].x,pointTab[i].y), color = "red")  # koloruje aktualnie przegladany punkt
        triangleFind = dfsFindPoint_draw(triangleMap, pointTab[i], visDelunay,E,G)

        if triangleFind is not None:
            printTriangles({triangleFind}, visDelunay, E, G, "orange")
            triangleSearchMap = bfsTriangleSearcherMapCreator(triangleMap, triangleFind, pointTab[i],visDelunay,E,G)  # znajduje wszystkie trojkaty do ktorych moge isc
            if len(triangleSearchMap) == 1:  # przypadek w ktorym tylko mamy do czynienia z jednym trojkatem
                triangleMap = updateMapForOneTriangle(triangleMap, pointTab[i], triangleFind, zeroTriangle)
            else:
                triangleMap = bfsTriangleEdgeRemover(triangleMap, triangleFind, pointTab[i], triangleSearchMap,zeroTriangle)  # aktualizuje stan trojkatow

            visDelunay.remove_figure(G.pop())

        visDelunay.add_point((pointTab[i].x, pointTab[i].y), color = "blue")  # przywracam kolor przegladanemu punktowi
        visDelunay.remove_figure(D.pop())
        printTriangles(triangleMap, visDelunay, E, D)

    triangleToDetector = triangleMap

    # dla kazdej krawedzi zawracam zbior trojkatow ktore ja przecinaja
    cutterMap = findCuttersEdges(edgesSet, triangleToDetector)

    # zamieniam przekatne az pozbede sie przeciec
    convertCuttersEdge(cutterMap, triangleToDetector, edgesSet)

    visDelunay.remove_figure(D.pop())
    printTriangles(triangleMap, visDelunay, E, D)

    # usuwam obramowania
    triangleToDetector = deletedBorder(triangleMap,zeroTriangle)

    visDelunay.remove_figure(D.pop())
    printTriangles(triangleToDetector, visDelunay, E, D)

    # usuwam pozostale trojkaty, ktore nie naleza do figury
    selectTriangle(triangleToDetector, edgesSet)

    visDelunay.remove_figure(D.pop())
    printTriangles(triangleToDetector, visDelunay, E, D)

    triangleList = triangleToList(triangleToDetector)

    return triangleList

if __name__ == '__main__':
    pass
    # # dla wersji rozszrzeonej testow
    # no_tests = 1
    # for polygon in t_to_show_gifs:
    #     vis = Visualizer()
    #     solEdges, visDelunay = delunay_draw(polygon)
    #
    #     vis.add_polygon(polygon)
    #     vis.add_point(polygon, color = "blue")
    #     vis.add_line_segment(solEdges, color = "black")
    #
    #     vis.show()
    #     # visDelunay.save_gif(f"/Users/arturgesiarz/Desktop/Algorytmy Geometryczne/projekt/gifs/prezentacja_{no_tests}", interval = 100)
    #
    #     no_tests += 1