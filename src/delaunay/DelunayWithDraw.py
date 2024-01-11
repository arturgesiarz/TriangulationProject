from src.delaunay.LineFunction import LineFunction
from src.delaunay.Point import Point
from src.delaunay.Triangle import Triangle
from collections import deque
from math import sqrt

# testy
from Testy import *

# dodatkowe importy - na potrzeby testow dzialania
from copy import deepcopy
from src.visualizer.main import Visualizer  # narzedzie do wizualizacji


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

def createSetEdges(triagleSol: set[Triangle]):
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


# def printTraianglesWithPoints(triangleMap: set[Triangle], polygon: list, actPoint):
#     vis = Visualizer()
#     lineSegments = []
#
#     for triangle in triangleMap:
#         segmentAB = ((triangle.a.x, triangle.a.y), (triangle.b.x, triangle.b.y))
#         segmentBC = ((triangle.b.x, triangle.b.y), (triangle.c.x, triangle.c.y))
#         segmentAC = ((triangle.a.x, triangle.a.y), (triangle.c.x, triangle.c.y))
#         lineSegments.append(segmentAB)
#         lineSegments.append(segmentBC)
#         lineSegments.append(segmentAC)
#
#     polygonCopy = deepcopy(polygon)
#     polygonCopy.remove(actPoint)
#
#     vis.add_point(polygonCopy, color = "blue")
#     vis.add_point(actPoint, color = "red")
#     vis.add_line_segment(lineSegments)
#
#     vis.show()

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
    triangleMap = inicializeWithStartTriangle(pointTab,zeroTriangle)  # mapa aktualnie znajdujacych sie trojkatow w triangulacji
    printTriangles(triangleMap, visDelunay,E, D)

    for i in range(1, n):  # przegladam nasze kolejne punkty
        visDelunay.add_point((pointTab[i].x,pointTab[i].y), color = "red")  # koloruje aktualnie przegladany punkt
        triangleFind = findPointInTriangle(triangleMap, pointTab[i], visDelunay,E,G)

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

    triangleSol = deletedBorder(triangleMap,zeroTriangle)
    visDelunay.remove_figure(D.pop())
    printTriangles(triangleSol, visDelunay, E, D)

    return createListEdges(createSetEdges(triangleSol)), visDelunay

if __name__ == '__main__':
    pass