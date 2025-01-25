from Screen import MyScreen
import math


class DistanceCalc:
    needToReset: bool = True

    oneKilometerInPixels: int = None

    firstVerticalPoint:  int = None
    secondVerticalPoint: int = None
    verticalPointXCoord: int = None

    SCREEN:MyScreen = None

    INPUTS:list = []

    def __init__(self, screen:MyScreen):
        DistanceCalc.SCREEN = screen


    @staticmethod
    def push(x:int, y:int):
        DistanceCalc.push.screen_sizes = MyScreen.get_screen_size()
        if x < 0 or y < 0 or x > DistanceCalc.push.screen_sizes[0] or y > DistanceCalc.push.screen_sizes[1]:
            return
        
        if not hasattr(DistanceCalc.push, "skip"):
            DistanceCalc.push.skip = True

        DistanceCalc.INPUTS.append([x, y])

        if len(DistanceCalc.INPUTS) <= 2:
            DistanceCalc.setVerticalPoint(x, y)
        else:
            if DistanceCalc.push.skip == True:
                DistanceCalc.push.skip = False
                return
            prev = DistanceCalc.INPUTS[-2]
            pprev = DistanceCalc.INPUTS[-1]
            DistanceCalc.drawDistanceAsLine(prev[0], prev[1], pprev[0], pprev[1])
            DistanceCalc.push.skip = True
        

    @staticmethod
    def setVerticalPoint(x: int, y: int):
        if DistanceCalc.needToReset == False:
            return
        if DistanceCalc.firstVerticalPoint is None:
            DistanceCalc.firstVerticalPoint = y
            DistanceCalc.verticalPointXCoord = x
        else:
            DistanceCalc.secondVerticalPoint = y
            DistanceCalc.oneKilometerInPixels = abs(DistanceCalc.firstVerticalPoint - DistanceCalc.secondVerticalPoint)
            # print(f"Points: {DistanceCalc.firstVerticalPoint} {DistanceCalc.secondVerticalPoint}, distance: {DistanceCalc.oneKilometerInPixels}", end="")
            # print(f" x: {DistanceCalc.verticalPointXCoord}")
            DistanceCalc.needToReset = False

            DistanceCalc.SCREEN.draw_line(
                DistanceCalc.verticalPointXCoord, DistanceCalc.firstVerticalPoint, 
                DistanceCalc.verticalPointXCoord, DistanceCalc.secondVerticalPoint,
                color = "green", width = 5
            )
            DistanceCalc.SCREEN.draw_text(
                DistanceCalc.verticalPointXCoord - 14, (DistanceCalc.firstVerticalPoint+DistanceCalc.secondVerticalPoint)/2,
                DistanceCalc.SCREEN.pixel_scale.get(), "green", 90
            )



    @staticmethod
    def triangleCalc(x1:int, y1:int, x2:int, y2:int) -> list[float, float]:
        width:int = abs(x1 - x2)
        height:int = abs(y1 - y2)
        gipotenuza = (width*width + height* height)**0.5

        if width != 0:
            angle = math.degrees(math.atan(height/width))
        else: angle = 0

        if (x1 > x2 and y1 > y2) or (x1 < x2 and y1 < y2):
            angle = -angle

        print(f"coords: {x1}, {y1}, {x2}, {y2}")
        print(f"angle: {angle}, гипотенуза: {gipotenuza}")

        return gipotenuza, angle


    
    @staticmethod
    def drawDistanceAsLine(x1:int, y1:int, x2:int, y2:int) -> None:
        distance, angle = DistanceCalc.triangleCalc(x1, y1, x2, y2)
        
        #500px = 1000m
        #200px = ?
        #        ^
        #        |
        #   normalized

        try:
            normalizedDistance = distance * DistanceCalc.SCREEN.pixel_scale.get() / DistanceCalc.oneKilometerInPixels
            DistanceCalc.SCREEN.draw_line(x1, y1, x2, y2)
            DistanceCalc.SCREEN.draw_text((x1+x2)/2, (y1+y2)/2, int(normalizedDistance), color='white', angle=angle)
        except ZeroDivisionError:
            return


    @staticmethod
    def triangleDraw(x1:int, y1:int, x2:int, y2:int) -> None:
        print(x1,y1,x2,y2)
        
        distance, angle = DistanceCalc.triangleCalc(x1,y1,x2,y2)
        
        # print(distance, angle)

        if x1 > x2:
            if y1> y2:
                print("1")
                DistanceCalc.SCREEN.draw_triangle(
                    x1, y1, x2, y2, x2, y1
                )
            else:
                print("2")
                DistanceCalc.SCREEN.draw_triangle(
                    x1, y1, x2, y2, x1, y2
                )
        else:
            if y1 > y2:
                print("3")
                DistanceCalc.SCREEN.draw_triangle(
                    x1, y1, x2, y2, x1, y2
                )
            else:
                print("4")
                DistanceCalc.SCREEN.draw_triangle(
                    x1, y1, x2, y2, x1, y2
                )

        DistanceCalc.SCREEN.draw_text((x1+x2)/2, (y1+y2)/2, distance, color='white', angle=angle)