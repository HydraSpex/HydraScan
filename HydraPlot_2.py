#Library import -------------------------------------------------------
#Matplotlib imports
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator, LinearLocator, FormatStrFormatter
from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation
import matplotlib.animation as animation
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.font_manager as fm
import matplotlib as mpl
import numpy as np

import math


class PlotMesh(FigureCanvas, TimedAnimation):
        def __init__(self, FilePath, DataStart, XCol, YCol, PlotCol, Color, Plotname, Filename, Range, ScaleBar, Fontsize, Fontcolor, FontWeight, ScaleBarSize, ScaleBarSizeVertical, ScaleBarPosition, ScaleBarOffset, XAxis, YAxis, ZAxis, InvertX, InvertY, Zoom, XStart, XStop, YStart, YStop, UseLimits, LowerLimit, UpperLimit):
                super().__init__(self)
                self.file = FilePath
                self.datastart = DataStart
                self.colors = Color
                self.Plotname = Plotname
                self.DateTime4 = Filename
                print(self.DateTime4)

                self.ScaleBar = ScaleBar
                self.Fontsize = Fontsize
                self.Fontcolor = Fontcolor
                #self.ScaleBarSize = 11.5
                self.ScaleBarSize = ScaleBarSize                                        #in Pixel
                self.ScaleBarSizeVertical = ScaleBarSizeVertical                        #in Pixel
                
                self.Range = Range

                self.FontWeight = FontWeight                                            #or "normal"
                self.ScaleBarPosition = ScaleBarPosition                                #or "upper", "center", "right"
                self.ScaleBarOffset = ScaleBarOffset                                    #in Pixel

                self.XAxis = XAxis
                self.YAxis = YAxis
                self.ZAxis = ZAxis
                self.InvertX = InvertX
                self.InvertY = InvertY

                self.Zoom = Zoom
                self.XStart = XStart
                self.XStop = XStop
                self.YStart = YStart
                self.YStop = YStop

                self.XCol = XCol
                self.YCol = YCol
                self.PlotCol = int(PlotCol)

                self.UseLimits = UseLimits
                self.LowerLimit = LowerLimit
                self.UpperLimit = UpperLimit
                if self.UseLimits == False or self.UpperLimit <= self.LowerLimit:
                        self.LowerLimit = 0
                        self.UpperLimit = 0
                print("Colorbar-Limits: " + str(self.LowerLimit) + " x " + str(self.UpperLimit))

                #Scalebar calculation
                self.Scale = 0
                try:
                #if self.Range == True:
                        f = open(self.file, "r")
                        Line1 = f.readline()
                        Line2 = f.readline()
                        Line3 = f.readline()
                        Line4 = f.readline()
                        
                        i = 0
                        control = 0
                        BitValueRead = []
                        while i < len(Line4):
                                #print(Line4[i])
                                if Line4[i]=="\t":
                                        #print("Tab")
                                        control = 1
                                if Line4[i]==" ":
                                        #print("Space")
                                        control = 0
                                if control == 1 and Line4[i]!="\t":
                                        BitValueRead.append(Line4[i])
                                i += 1
                        i = 0
                        BitValText = ""
                        while i < len(BitValueRead):
                                BitValText += str(BitValueRead[i])
                                i += 1
                        print(BitValText)
                        BitValInt = int(BitValText)
                        print(str(BitValInt) + " Pixel")

                        
                        Line5 = f.readline()
                        control = 0
                        index = 0
                        i = 0
                        control = 0
                        RangeXRead = []
                        RangeYRead = []
                        while i < len(Line5):
                                #print(Line5[i])
                                if Line5[i]=="\t":
                                        #print("Tab")
                                        control = 1
                                if Line5[i]==" ":
                                        #print("Space")
                                        control = 0
                                        index += 1
                                if control == 1 and index == 0 and Line5[i]!="\t":
                                        RangeXRead.append(Line5[i])
                                if control == 1 and index == 0 and Line5[i]!="\t":
                                        RangeYRead.append(Line5[i])
                                i += 1
                        i = 0
                        RangeXText = ""
                        while i < len(RangeXRead):
                                RangeXText += str(RangeXRead[i])
                                i += 1
                        RangeXFloat = float(RangeXText)
                        print(str(RangeXFloat) + " nm")

                        i = 0
                        RangeYText = ""
                        while i < len(RangeYRead):
                                RangeYText += str(RangeYRead[i])
                                i += 1
                        RangeYFloat = float(RangeYText)
                        print(str(RangeYFloat) + " nm")
                        
                        f.close()
                        self.XBitWidth = ((RangeXFloat/1000)/BitValInt)
                        self.YBitWidth = ((RangeYFloat/1000)/BitValInt)
                        self.Scale = self.ScaleBarSize / self.XBitWidth
                        #print(str(RangeXFloat) + "\t" + str(self.XBitWidth) + "\t" + str(RangeYFloat) + "\t" + str(self.YBitWidth) + "\t" + str(self.ScaleBarSize) + "\t" + str(self.XBitWidth) + "\t" + str(self.Scale))
                except:
                #else:
                        self.ScaleBar = False
                        self.Range = False
                        print("Flase")
                self.ScaleText = str(self.ScaleBarSize) + " \u03BCm"                                #Text under Bar


                self.run()
                        
        def run(self):  
                print("Plot start")                

                fontprops = fm.FontProperties(size=self.Fontsize, weight=self.FontWeight)

                #Open File ---------------------------------------------------------------------------------------------
                data_file = np.loadtxt(self.file, delimiter='\t', skiprows=self.datastart)
                xRaw = data_file[:,self.XCol]
                yRaw = data_file[:,self.YCol]
                zRaw = data_file[:,self.PlotCol]

                xstart = xRaw[0]
                ystart = yRaw[0]
                xstop = xRaw[len(xRaw)-1] + 1
                ystop = yRaw[len(yRaw)-1] + 1
                self.ystop = ystop
                self.ystart = ystart
                
                print(str(xstart) + " x " + str(xstop))
                print(str(ystart) + " x " + str(ystop))
                print(self.roundup(np.amax(zRaw)))

                
                #Grid Setup
                if self.Zoom == True:
                        xstart = self.XStart
                        xstop = self.XStop + 1
                        ystart = self.YStart
                        ystop = self.YStop + 1
                        xges = xstop - xstart
                        yges = ystop - ystart
                        
                        if yges < xges:
                                dif = xges - yges
                                if (ystop + dif) <= self.ystop:
                                        ystop = ystop + dif
                                elif (ystart - dif) >= self.ystart:
                                        ystart = ystart - dif
                                elif (ystop + math.ceil(dif/2)) <= self.ystop and (ystart - math.floor(dif/2)) >= self.ystart:
                                        ystop = ystop + math.ceil(dif/2)
                                        ystart = ystart - math.floor(dif/2)
                                        
                X = np.arange(xstart, xstop, 1)
                Y = np.arange(ystart, ystop, 1)

                if self.Range == True:
                        i = 0
                        XNew = []
                        while i < len(X):
                                XNew.append(X[i] * self.XBitWidth)
                                i += 1
                        X = XNew
                        
                        i = 0
                        YNew = []
                        while i < len(Y):
                                YNew.append(Y[i] * self.YBitWidth)
                                i += 1
                        Y = YNew
                        self.Scale = self.ScaleBarSize
                        

                X, Y = np.meshgrid(X, Y)

                i = 0
                zPart = []
                Z = []
                xval = xstart
                yval = ystart
                while xval < xstop:
                        while yval < ystop:
                                zPart.append(zRaw[i])
                                i = i + 1
                                yval = yval + 1
                        Z.append(zPart)
                        zPart = []
                        xval = xval + 1
                        yval = ystart
    
                #Style Setup
                if self.colors == 1:
                        cmap = plt.get_cmap('Spectral_r')                                                                                               #Spektralfarben
                elif self.colors == 2:
                        cmap = plt.get_cmap('gray_r')                                                                                                   #Graustufen
                elif self.colors == 3:
                        cmap = plt.get_cmap('bone')                                                                                                     #Blau zu Grün
                elif self.colors == 4:
                        cmap = plt.get_cmap('Wistia')                                                                                                   #Gelb zu Rot
                elif self.colors == 5:
                        cmap = plt.get_cmap('copper')                                                                                                   #Lila zu Gelb
                elif self.colors == 6:
                        cmap = plt.get_cmap('gist_heat')                                                                                                        #Graustufen
                elif self.colors == 7:
                        cmap = plt.get_cmap('winter')                                                                                                   #Blau zu Grün
                elif self.colors == 8:
                        cmap = plt.get_cmap('spring')                                                                                                   #Gelb zu Rot
                elif self.colors == 9:
                        cmap = plt.get_cmap('summer')                                                                                                   #Lila zu Gelb
                elif self.colors == 10:
                        cmap = plt.get_cmap('autumn')                                                                                                   #Graustufen
                elif self.colors == 11:
                        cmap = plt.get_cmap('hot_r')                                                                                                    #Blau zu Grün
                elif self.colors == 12:
                        cmap = plt.get_cmap('cool')                                                                                                    #Graustufen
                elif self.colors == 13:
                        cmap = plt.get_cmap('gist_ncar')                                                                                                    #Blau zu Grün
                elif self.colors == 14:
                        cmap = plt.get_cmap('nipy_spectral')                                                                                                  #Blau zu Grün
                elif self.colors == 15:
                        cmap = plt.get_cmap('Reds')                                                                                            #Lila zu Gelb

                #levels = MaxNLocator(nbins=998).tick_values(0, 998)
                #levels = MaxNLocator(nbins=self.roundup(np.amax(zRaw))).tick_values(0, self.roundup(np.amax(zRaw)))                                                                             #characterizes the bar right
                #norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)                                  
                #norm = mpl.colors.Normalize(vmin=0, vmax=self.roundup(np.amax(zRaw)))
                #Figure Setup
                fig, ax0  = plt.subplots()                                                                                                      #Adds the plot to the figure

                #if self.UseLimits == False:
                im1 = ax0.pcolormesh(X, Y, Z, cmap=cmap)
                #else:
                        #im1 = ax0.pcolormesh(X, Y, Z, cmap=cmap, vmin=self.LowerLimit, vmax=self.UpperLimit)

            
                cbar = plt.colorbar(im1)
                cbar.set_label(self.ZAxis)
                
                ax0.set_title(self.Plotname)

                if self.ScaleBar == True:
                        scalebar = AnchoredSizeBar(ax0.transData,
                                   self.Scale, self.ScaleText, self.ScaleBarPosition, 
                                   pad=self.ScaleBarOffset,
                                   color=self.Fontcolor,
                                   frameon=False,
                                   size_vertical=self.ScaleBarSizeVertical,
                                   fontproperties=fontprops)
                        ax0.add_artist(scalebar)


                ax0.set_xlabel(self.XAxis)
                ax0.set_ylabel(self.YAxis)
                ax0.set_label('Some Units')

                if self.InvertX == True:
                        ax0.invert_xaxis()
                if self.InvertY == True:
                        ax0.invert_yaxis()                                                                                                                  #invertiert die y-Achse
                ax0.xaxis.tick_top() 
                self.fig.canvas.draw()                                                                                                           #setzt die x-Achse nach oben


                #Plot and Save -----------------------------------------------------------------------------------------
                try:
                        plt.savefig(self.DateTime4)
                except:
                        print("Saving Plot not possible")

                #plt.show()
                try:
                        plt.show()                                                                                                                          #Plot
                except:
                        print("Plot not posible")
                plt.show()

                #Ende --------------------------------------------------------------------------------------------------
                self.killBrian()

        def roundup(self, val):
                val = val + 5
                return int(math.ceil(val / 10.0)) * 10

        def killBrian(self):                                                                     
                print("Brian dead")


class PlotContour3D:
        def __init__(self, FilePath, DataStart, XCol, YCol, PlotCol, Color, Plotname, Filename, Range, ScaleBar, Fontsize, Fontcolor, FontWeight, ScaleBarSize, ScaleBarSizeVertical, ScaleBarPosition, ScaleBarOffset, XAxis, YAxis, ZAxis, InvertX, InvertY, Zoom, XStart, XStop, YStart, YStop, UseLimits, LowerLimit, UpperLimit):
                self.file = FilePath
                self.datastart = DataStart
                self.colors = Color
                self.Plotname = Plotname
                self.DateTime4 = Filename
                print(self.DateTime4)

                self.ScaleBar = ScaleBar
                self.Fontsize = Fontsize
                self.Fontcolor = Fontcolor
                #self.ScaleBarSize = 11.5
                self.ScaleBarSize = ScaleBarSize                                        #in Pixel
                self.ScaleBarSizeVertical = ScaleBarSizeVertical                        #in Pixel
                
                self.Range = Range

                self.FontWeight = FontWeight                                            #or "normal"
                self.ScaleBarPosition = ScaleBarPosition                                #or "upper", "center", "right"
                self.ScaleBarOffset = ScaleBarOffset                                    #in Pixel

                self.XAxis = XAxis
                self.YAxis = YAxis
                self.ZAxis = ZAxis
                self.InvertX = InvertX
                self.InvertY = InvertY

                self.Zoom = Zoom
                self.XStart = XStart
                self.XStop = XStop
                self.YStart = YStart
                self.YStop = YStop

                self.XCol = XCol
                self.YCol = YCol
                self.PlotCol = int(PlotCol)

                self.UseLimits = UseLimits
                self.LowerLimit = LowerLimit
                self.UpperLimit = UpperLimit
                if self.UseLimits == False or self.UpperLimit <= self.LowerLimit:
                        self.LowerLimit = 0
                        self.UpperLimit = 0
                print("Colorbar-Limits: " + str(self.LowerLimit) + " x " + str(self.UpperLimit))


                #Scalebar calculation
                self.Scale = 0
                try:
                #if self.Range == True:
                        f = open(self.file, "r")
                        Line1 = f.readline()
                        Line2 = f.readline()
                        Line3 = f.readline()
                        Line4 = f.readline()
                        
                        i = 0
                        control = 0
                        BitValueRead = []
                        while i < len(Line4):
                                #print(Line4[i])
                                if Line4[i]=="\t":
                                        #print("Tab")
                                        control = 1
                                if Line4[i]==" ":
                                        #print("Space")
                                        control = 0
                                if control == 1 and Line4[i]!="\t":
                                        BitValueRead.append(Line4[i])
                                i += 1
                        i = 0
                        BitValText = ""
                        while i < len(BitValueRead):
                                BitValText += str(BitValueRead[i])
                                i += 1
                        print(BitValText)
                        BitValInt = int(BitValText)
                        print(str(BitValInt) + " Pixel")

                        
                        Line5 = f.readline()
                        control = 0
                        index = 0
                        i = 0
                        control = 0
                        RangeXRead = []
                        RangeYRead = []
                        while i < len(Line5):
                                #print(Line5[i])
                                if Line5[i]=="\t":
                                        #print("Tab")
                                        control = 1
                                if Line5[i]==" ":
                                        #print("Space")
                                        control = 0
                                        index += 1
                                if control == 1 and index == 0 and Line5[i]!="\t":
                                        RangeXRead.append(Line5[i])
                                if control == 1 and index == 0 and Line5[i]!="\t":
                                        RangeYRead.append(Line5[i])
                                i += 1
                        i = 0
                        RangeXText = ""
                        while i < len(RangeXRead):
                                RangeXText += str(RangeXRead[i])
                                i += 1
                        RangeXFloat = float(RangeXText)
                        print(str(RangeXFloat) + " nm")

                        i = 0
                        RangeYText = ""
                        while i < len(RangeYRead):
                                RangeYText += str(RangeYRead[i])
                                i += 1
                        RangeYFloat = float(RangeYText)
                        print(str(RangeYFloat) + " nm")
                        
                        f.close()
                        self.XBitWidth = ((RangeXFloat/1000)/BitValInt)
                        self.YBitWidth = ((RangeYFloat/1000)/BitValInt)
                        self.Scale = self.ScaleBarSize / self.XBitWidth
                        print(str(RangeXFloat) + "\t" + str(self.XBitWidth) + "\t" + str(RangeYFloat) + "\t" + str(self.YBitWidth) + "\t" + str(self.ScaleBarSize) + "\t" + str(self.XBitWidth) + "\t" + str(self.Scale))
                except:
                #else:
                        self.ScaleBar = False
                        self.Range = False
                        print("Flase")
                self.ScaleText = str(self.ScaleBarSize) + " \u03BCm"                                #Text under Bar

                self.run()
                        
        def run(self):  
                print("Plot start")                

                fontprops = fm.FontProperties(size=self.Fontsize, weight=self.FontWeight)

                #Open File ---------------------------------------------------------------------------------------------
                data_file = np.loadtxt(self.file, delimiter='\t', skiprows=self.datastart)
                xRaw = data_file[:,self.XCol]
                yRaw = data_file[:,self.YCol]
                zRaw = data_file[:,self.PlotCol]
                
                xstart = xRaw[0]
                ystart = yRaw[0]
                xstop = xRaw[len(xRaw)-1] + 1
                ystop = yRaw[len(yRaw)-1] + 1
                self.ystop = ystop
                self.ystart = ystart
                
                print(str(xstart) + " x " + str(xstop))
                print(str(ystart) + " x " + str(ystop))
                print(self.roundup(np.amax(zRaw)))

                
                #Grid Setup
                if self.Zoom == True:
                        xstart = self.XStart
                        xstop = self.XStop + 1
                        ystart = self.YStart
                        ystop = self.YStop + 1
                        xges = xstop - xstart
                        yges = ystop - ystart
                        
                        if yges < xges:
                                dif = xges - yges
                                if (ystop + dif) <= self.ystop:
                                        ystop = ystop + dif
                                elif (ystart - dif) >= self.ystart:
                                        ystart = ystart - dif
                                elif (ystop + math.ceil(dif/2)) <= self.ystop and (ystart - math.floor(dif/2)) >= self.ystart:
                                        ystop = ystop + math.ceil(dif/2)
                                        ystart = ystart - math.floor(dif/2)
                
                print(str(xstart) + " x " + str(xstop))
                print(str(ystart) + " x " + str(ystop))
                print(self.roundup(np.amax(zRaw)))

                
                #Grid Setup                
                X = np.arange(xstart, xstop, 1)
                Y = np.arange(ystart, ystop, 1)

                if self.Range == True:
                        i = 0
                        XNew = []
                        while i < len(X):
                                XNew.append(X[i] * self.XBitWidth)
                                i += 1
                        X = XNew
                        
                        i = 0
                        YNew = []
                        while i < len(Y):
                                YNew.append(Y[i] * self.YBitWidth)
                                i += 1
                        Y = YNew
                        self.Scale = self.ScaleBarSize
                
                X, Y = np.meshgrid(X, Y)

                i = 0
                zPart = []
                Z = []
                xval = xstart
                yval = ystart
                while xval < xstop:
                        while yval < ystop:
                                zPart.append(zRaw[i])
                                i = i + 1
                                yval = yval + 1
                        Z.append(zPart)
                        zPart = []
                        xval = xval + 1
                        yval = ystart

                print(Z)
                Znp = np.array(Z)
                print(Znp)
                print(Znp.ndim)
                        
                #Style Setup
                if self.colors == 1:
                        cmap = plt.get_cmap('Spectral_r')                                                                                               #Spektralfarben
                elif self.colors == 2:
                        cmap = plt.get_cmap('gray_r')                                                                                                   #Graustufen
                elif self.colors == 3:
                        cmap = plt.get_cmap('bone')                                                                                                     #Blau zu Grün
                elif self.colors == 4:
                        cmap = plt.get_cmap('Wistia')                                                                                                   #Gelb zu Rot
                elif self.colors == 5:
                        cmap = plt.get_cmap('copper')                                                                                                   #Lila zu Gelb
                elif self.colors == 6:
                        cmap = plt.get_cmap('gist_heat')                                                                                                        #Graustufen
                elif self.colors == 7:
                        cmap = plt.get_cmap('winter')                                                                                                   #Blau zu Grün
                elif self.colors == 8:
                        cmap = plt.get_cmap('spring')                                                                                                   #Gelb zu Rot
                elif self.colors == 9:
                        cmap = plt.get_cmap('summer')                                                                                                   #Lila zu Gelb
                elif self.colors == 10:
                        cmap = plt.get_cmap('autumn')                                                                                                   #Graustufen
                elif self.colors == 11:
                        cmap = plt.get_cmap('hot_r')                                                                                                    #Blau zu Grün
                elif self.colors == 12:
                        cmap = plt.get_cmap('cool')                                                                                                    #Graustufen
                elif self.colors == 13:
                        cmap = plt.get_cmap('gist_ncar')                                                                                                    #Blau zu Grün
                elif self.colors == 14:
                        cmap = plt.get_cmap('nipy_spectral')                                                                                                  #Blau zu Grün
                elif self.colors == 15:
                        cmap = plt.get_cmap('Reds')                                                                                            #Lila zu Gelb

                levels = MaxNLocator(nbins=self.roundup(np.amax(zRaw))).tick_values(0, self.roundup(np.amax(zRaw)))                                                                              #characterizes the bar right
                norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)                                  

                #Figure Setup
                fig = plt.figure()
                ax = fig.gca(projection='3d')
                #surf = ax.plot_surface(X, Y, Znp, cmap=cm.coolwarm,
                #                       linewidth=0, antialiased=False)
                ax.plot_surface(X, Y, Znp, rstride=1, cstride=1, alpha=0.7)
                cset = ax.contour(X, Y, Znp, zdir='z', offset=-5, cmap=cm.coolwarm)
                cset = ax.contour(X, Y, Znp, zdir='x', offset=-5, cmap=cm.coolwarm)
                cset = ax.contour(X, Y, Znp, zdir='y', offset=-5, cmap=cm.coolwarm)

                # Customize the z axis.
                ax.set_xlim(xstart, xstop)
                ax.set_ylim(ystart, ystop)
                ax.set_zlim(0, self.roundup(np.amax(zRaw)))
                ax.set_xlabel(self.XAxis)
                ax.set_ylabel(self.YAxis)
                ax.set_zlabel(self.ZAxis)

                if self.InvertX == True:
                        ax.invert_xaxis()
                if self.InvertY == True:
                        ax.invert_yaxis()  

                # Add a color bar which maps values to colors.
                #fig.colorbar(surf, shrink=0.5, aspect=5)

                #ax.invert_yaxis()              


                #Plot and Save -----------------------------------------------------------------------------------------
                try:
                        plt.savefig(self.DateTime4)
                except:
                        print("Saving Plot not possible")

                try:
                        plt.show()                                                                                                                          #Plot
                except:
                        print("Plot not posible")


                #Ende --------------------------------------------------------------------------------------------------
                self.killBrian()

        def roundup(self, val):
                return int(math.ceil(val / 10.0)) * 10

        def killBrian(self):                                                                     
                print("Brian dead")

class PlotContourFill3D:
        def __init__(self, FilePath, DataStart, XCol, YCol, PlotCol, Color, Plotname, Filename, Range, ScaleBar, Fontsize, Fontcolor, FontWeight, ScaleBarSize, ScaleBarSizeVertical, ScaleBarPosition, ScaleBarOffset, XAxis, YAxis, ZAxis, InvertX, InvertY, Zoom, XStart, XStop, YStart, YStop, UseLimits, LowerLimit, UpperLimit):
                self.file = FilePath
                self.datastart = DataStart
                self.colors = Color
                self.Plotname = Plotname
                self.DateTime4 = Filename
                print(self.DateTime4)

                self.ScaleBar = ScaleBar
                self.Fontsize = Fontsize
                self.Fontcolor = Fontcolor
                #self.ScaleBarSize = 11.5
                self.ScaleBarSize = ScaleBarSize                                        #in Pixel
                self.ScaleBarSizeVertical = ScaleBarSizeVertical                        #in Pixel
                
                self.Range = Range

                self.FontWeight = FontWeight                                            #or "normal"
                self.ScaleBarPosition = ScaleBarPosition                                #or "upper", "center", "right"
                self.ScaleBarOffset = ScaleBarOffset                                    #in Pixel

                self.XAxis = XAxis
                self.YAxis = YAxis
                self.ZAxis = ZAxis
                self.InvertX = InvertX
                self.InvertY = InvertY

                self.Zoom = Zoom
                self.XStart = XStart
                self.XStop = XStop
                self.YStart = YStart
                self.YStop = YStop

                self.XCol = XCol
                self.YCol = YCol
                self.PlotCol = int(PlotCol)

                self.UseLimits = UseLimits
                self.LowerLimit = LowerLimit
                self.UpperLimit = UpperLimit
                if self.UseLimits == False or self.UpperLimit <= self.LowerLimit:
                        self.LowerLimit = 0
                        self.UpperLimit = 0
                print("Colorbar-Limits: " + str(self.LowerLimit) + " x " + str(self.UpperLimit))


                #Scalebar calculation
                self.Scale = 0
                try:
                #if self.Range == True:
                        f = open(self.file, "r")
                        Line1 = f.readline()
                        Line2 = f.readline()
                        Line3 = f.readline()
                        Line4 = f.readline()
                        
                        i = 0
                        control = 0
                        BitValueRead = []
                        while i < len(Line4):
                                #print(Line4[i])
                                if Line4[i]=="\t":
                                        #print("Tab")
                                        control = 1
                                if Line4[i]==" ":
                                        #print("Space")
                                        control = 0
                                if control == 1 and Line4[i]!="\t":
                                        BitValueRead.append(Line4[i])
                                i += 1
                        i = 0
                        BitValText = ""
                        while i < len(BitValueRead):
                                BitValText += str(BitValueRead[i])
                                i += 1
                        print(BitValText)
                        BitValInt = int(BitValText)
                        print(str(BitValInt) + " Pixel")

                        
                        Line5 = f.readline()
                        control = 0
                        index = 0
                        i = 0
                        control = 0
                        RangeXRead = []
                        RangeYRead = []
                        while i < len(Line5):
                                #print(Line5[i])
                                if Line5[i]=="\t":
                                        #print("Tab")
                                        control = 1
                                if Line5[i]==" ":
                                        #print("Space")
                                        control = 0
                                        index += 1
                                if control == 1 and index == 0 and Line5[i]!="\t":
                                        RangeXRead.append(Line5[i])
                                if control == 1 and index == 0 and Line5[i]!="\t":
                                        RangeYRead.append(Line5[i])
                                i += 1
                        i = 0
                        RangeXText = ""
                        while i < len(RangeXRead):
                                RangeXText += str(RangeXRead[i])
                                i += 1
                        RangeXFloat = float(RangeXText)
                        print(str(RangeXFloat) + " nm")

                        i = 0
                        RangeYText = ""
                        while i < len(RangeYRead):
                                RangeYText += str(RangeYRead[i])
                                i += 1
                        RangeYFloat = float(RangeYText)
                        print(str(RangeYFloat) + " nm")
                        
                        f.close()
                        self.XBitWidth = ((RangeXFloat/1000)/BitValInt)
                        self.YBitWidth = ((RangeYFloat/1000)/BitValInt)
                        self.Scale = self.ScaleBarSize / self.XBitWidth
                        print(str(RangeXFloat) + "\t" + str(self.XBitWidth) + "\t" + str(RangeYFloat) + "\t" + str(self.YBitWidth) + "\t" + str(self.ScaleBarSize) + "\t" + str(self.XBitWidth) + "\t" + str(self.Scale))
                except:
                #else:
                        self.ScaleBar = False
                        self.Range = False
                        print("Flase")
                self.ScaleText = str(self.ScaleBarSize) + " \u03BCm"                                #Text under Bar

                self.run()
                        
        def run(self):  
                print("Plot start")                

                fontprops = fm.FontProperties(size=self.Fontsize, weight=self.FontWeight)

                #Open File ---------------------------------------------------------------------------------------------
                data_file = np.loadtxt(self.file, delimiter='\t', skiprows=self.datastart)
                xRaw = data_file[:,self.XCol]
                yRaw = data_file[:,self.YCol]
                zRaw = data_file[:,self.PlotCol]

                xstart = xRaw[0]
                ystart = yRaw[0]
                xstop = xRaw[len(xRaw)-1] + 1
                ystop = yRaw[len(yRaw)-1] + 1
                self.ystop = ystop
                self.ystart = ystart
                
                print(str(xstart) + " x " + str(xstop))
                print(str(ystart) + " x " + str(ystop))
                print(self.roundup(np.amax(zRaw)))

                
                #Grid Setup
                if self.Zoom == True:
                        xstart = self.XStart
                        xstop = self.XStop + 1
                        ystart = self.YStart
                        ystop = self.YStop + 1
                        xges = xstop - xstart
                        yges = ystop - ystart
                        
                        if yges < xges:
                                dif = xges - yges
                                if (ystop + dif) <= self.ystop:
                                        ystop = ystop + dif
                                elif (ystart - dif) >= self.ystart:
                                        ystart = ystart - dif
                                elif (ystop + math.ceil(dif/2)) <= self.ystop and (ystart - math.floor(dif/2)) >= self.ystart:
                                        ystop = ystop + math.ceil(dif/2)
                                        ystart = ystart - math.floor(dif/2)
                
                print(str(xstart) + " x " + str(xstop))
                print(str(ystart) + " x " + str(ystop))
                print(self.roundup(np.amax(zRaw)))

                
                #Grid Setup                
                X = np.arange(xstart, xstop, 1)
                Y = np.arange(ystart, ystop, 1)

                if self.Range == True:
                        i = 0
                        XNew = []
                        while i < len(X):
                                XNew.append(X[i] * self.XBitWidth)
                                i += 1
                        X = XNew
                        
                        i = 0
                        YNew = []
                        while i < len(Y):
                                YNew.append(Y[i] * self.YBitWidth)
                                i += 1
                        Y = YNew
                        self.Scale = self.ScaleBarSize
                
                X, Y = np.meshgrid(X, Y)

                i = 0
                zPart = []
                Z = []
                xval = xstart
                yval = ystart
                while xval < xstop:
                        while yval < ystop:
                                zPart.append(zRaw[i])
                                i = i + 1
                                yval = yval + 1
                        Z.append(zPart)
                        zPart = []
                        xval = xval + 1
                        yval = ystart

                print(Z)
                Znp = np.array(Z)
                print(Znp)
                print(Znp.ndim)
                        
                #Style Setup
                if self.colors == 1:
                        cmap = plt.get_cmap('Spectral_r')                                                                                               #Spektralfarben
                elif self.colors == 2:
                        cmap = plt.get_cmap('gray_r')                                                                                                   #Graustufen
                elif self.colors == 3:
                        cmap = plt.get_cmap('bone')                                                                                                     #Blau zu Grün
                elif self.colors == 4:
                        cmap = plt.get_cmap('Wistia')                                                                                                   #Gelb zu Rot
                elif self.colors == 5:
                        cmap = plt.get_cmap('copper')                                                                                                   #Lila zu Gelb
                elif self.colors == 6:
                        cmap = plt.get_cmap('gist_heat')                                                                                                        #Graustufen
                elif self.colors == 7:
                        cmap = plt.get_cmap('winter')                                                                                                   #Blau zu Grün
                elif self.colors == 8:
                        cmap = plt.get_cmap('spring')                                                                                                   #Gelb zu Rot
                elif self.colors == 9:
                        cmap = plt.get_cmap('summer')                                                                                                   #Lila zu Gelb
                elif self.colors == 10:
                        cmap = plt.get_cmap('autumn')                                                                                                   #Graustufen
                elif self.colors == 11:
                        cmap = plt.get_cmap('hot_r')                                                                                                    #Blau zu Grün
                elif self.colors == 12:
                        cmap = plt.get_cmap('cool')                                                                                                    #Graustufen
                elif self.colors == 13:
                        cmap = plt.get_cmap('gist_ncar')                                                                                                    #Blau zu Grün
                elif self.colors == 14:
                        cmap = plt.get_cmap('nipy_spectral')                                                                                                  #Blau zu Grün
                elif self.colors == 15:
                        cmap = plt.get_cmap('Reds')                                                                                            #Lila zu Gelb

                levels = MaxNLocator(nbins=self.roundup(np.amax(zRaw))).tick_values(0, self.roundup(np.amax(zRaw)))                                                                              #characterizes the bar right
                norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)                                  

                #Figure Setup
                fig = plt.figure()
                ax = fig.gca(projection='3d')
                #surf = ax.plot_surface(X, Y, Znp, cmap=cm.coolwarm,
                #                       linewidth=0, antialiased=False)
                ax.plot_surface(X, Y, Znp, rstride=1, cstride=1, alpha=0.7)
                cset = ax.contourf(X, Y, Znp, zdir='z', offset=-5, cmap=cm.coolwarm)
                cset = ax.contourf(X, Y, Znp, zdir='x', offset=-5, cmap=cm.coolwarm)
                cset = ax.contourf(X, Y, Znp, zdir='y', offset=-5, cmap=cm.coolwarm)

                # Customize the z axis.
                ax.set_xlim(xstart, xstop)
                ax.set_ylim(ystart, ystop)
                ax.set_zlim(0, self.roundup(np.amax(zRaw)))
                
                ax.set_xlabel(self.XAxis)
                ax.set_ylabel(self.YAxis)
                ax.set_zlabel(self.ZAxis)

                if self.InvertX == True:
                        ax.invert_xaxis()
                if self.InvertY == True:
                        ax.invert_yaxis()  

                # Add a color bar which maps values to colors.
                #fig.colorbar(surf, shrink=0.5, aspect=5)

                #ax.invert_yaxis()              


                #Plot and Save -----------------------------------------------------------------------------------------
                try:
                        plt.savefig(self.DateTime4)
                except:
                        print("Saving Plot not possible")

                try:
                        plt.show()                                                                                                                          #Plot
                except:
                        print("Plot not posible")


                #Ende --------------------------------------------------------------------------------------------------
                self.killBrian()

        def roundup(self, val):
                return int(math.ceil(val / 10.0)) * 10

        def killBrian(self):                                                                     
                print("Brian dead")


class Plot3D:
        def __init__(self, FilePath, DataStart, XCol, YCol, PlotCol, Color, Plotname, Filename, Range, ScaleBar, Fontsize, Fontcolor, FontWeight, ScaleBarSize, ScaleBarSizeVertical, ScaleBarPosition, ScaleBarOffset, XAxis, YAxis, ZAxis, InvertX, InvertY, Zoom, XStart, XStop, YStart, YStop, UseLimits, LowerLimit, UpperLimit):
                self.file = FilePath
                self.datastart = DataStart
                self.colors = Color
                self.Plotname = Plotname
                self.DateTime4 = Filename
                print(self.DateTime4)

                self.ScaleBar = ScaleBar
                self.Fontsize = Fontsize
                self.Fontcolor = Fontcolor
                #self.ScaleBarSize = 11.5
                self.ScaleBarSize = ScaleBarSize                                        #in Pixel
                self.ScaleBarSizeVertical = ScaleBarSizeVertical                        #in Pixel
                
                self.Range = Range

                self.FontWeight = FontWeight                                            #or "normal"
                self.ScaleBarPosition = ScaleBarPosition                                #or "upper", "center", "right"
                self.ScaleBarOffset = ScaleBarOffset                                    #in Pixel

                self.XAxis = XAxis
                self.YAxis = YAxis
                self.ZAxis = ZAxis
                self.InvertX = InvertX
                self.InvertY = InvertY

                self.Zoom = Zoom
                self.XStart = XStart
                self.XStop = XStop
                self.YStart = YStart
                self.YStop = YStop

                self.XCol = XCol
                self.YCol = YCol
                self.PlotCol = int(PlotCol)

                self.UseLimits = UseLimits
                self.LowerLimit = LowerLimit
                self.UpperLimit = UpperLimit
                if self.UseLimits == False or self.UpperLimit <= self.LowerLimit:
                        self.LowerLimit = 0
                        self.UpperLimit = 0
                print("Colorbar-Limits: " + str(self.LowerLimit) + " x " + str(self.UpperLimit))


                #Scalebar calculation
                self.Scale = 0
                try:
                #if self.Range == True:
                        f = open(self.file, "r")
                        Line1 = f.readline()
                        Line2 = f.readline()
                        Line3 = f.readline()
                        Line4 = f.readline()
                        
                        i = 0
                        control = 0
                        BitValueRead = []
                        while i < len(Line4):
                                #print(Line4[i])
                                if Line4[i]=="\t":
                                        #print("Tab")
                                        control = 1
                                if Line4[i]==" ":
                                        #print("Space")
                                        control = 0
                                if control == 1 and Line4[i]!="\t":
                                        BitValueRead.append(Line4[i])
                                i += 1
                        i = 0
                        BitValText = ""
                        while i < len(BitValueRead):
                                BitValText += str(BitValueRead[i])
                                i += 1
                        print(BitValText)
                        BitValInt = int(BitValText)
                        print(str(BitValInt) + " Pixel")

                        
                        Line5 = f.readline()
                        control = 0
                        index = 0
                        i = 0
                        control = 0
                        RangeXRead = []
                        RangeYRead = []
                        while i < len(Line5):
                                #print(Line5[i])
                                if Line5[i]=="\t":
                                        #print("Tab")
                                        control = 1
                                if Line5[i]==" ":
                                        #print("Space")
                                        control = 0
                                        index += 1
                                if control == 1 and index == 0 and Line5[i]!="\t":
                                        RangeXRead.append(Line5[i])
                                if control == 1 and index == 0 and Line5[i]!="\t":
                                        RangeYRead.append(Line5[i])
                                i += 1
                        i = 0
                        RangeXText = ""
                        while i < len(RangeXRead):
                                RangeXText += str(RangeXRead[i])
                                i += 1
                        RangeXFloat = float(RangeXText)
                        print(str(RangeXFloat) + " nm")

                        i = 0
                        RangeYText = ""
                        while i < len(RangeYRead):
                                RangeYText += str(RangeYRead[i])
                                i += 1
                        RangeYFloat = float(RangeYText)
                        print(str(RangeYFloat) + " nm")
                        
                        f.close()
                        self.XBitWidth = ((RangeXFloat/1000)/BitValInt)
                        self.YBitWidth = ((RangeYFloat/1000)/BitValInt)
                        self.Scale = self.ScaleBarSize / self.XBitWidth
                        print(str(RangeXFloat) + "\t" + str(self.XBitWidth) + "\t" + str(RangeYFloat) + "\t" + str(self.YBitWidth) + "\t" + str(self.ScaleBarSize) + "\t" + str(self.XBitWidth) + "\t" + str(self.Scale))
                except:
                #else:
                        self.ScaleBar = False
                        self.Range = False
                        print("Flase")
                self.ScaleText = str(self.ScaleBarSize) + " \u03BCm"                                #Text under Bar

                self.run()
                        
        def run(self):  
                print("Plot start")                

                fontprops = fm.FontProperties(size=self.Fontsize, weight=self.FontWeight)

                #Open File ---------------------------------------------------------------------------------------------
                data_file = np.loadtxt(self.file, delimiter='\t', skiprows=self.datastart)
                xRaw = data_file[:,self.XCol]
                yRaw = data_file[:,self.YCol]
                zRaw = data_file[:,self.PlotCol]

                xstart = xRaw[0]
                ystart = yRaw[0]
                xstop = xRaw[len(xRaw)-1] + 1
                ystop = yRaw[len(yRaw)-1] + 1
                self.ystop = ystop
                self.ystart = ystart
                
                print(str(xstart) + " x " + str(xstop))
                print(str(ystart) + " x " + str(ystop))
                print(self.roundup(np.amax(zRaw)))

                
                #Grid Setup
                if self.Zoom == True:
                        xstart = self.XStart
                        xstop = self.XStop + 1
                        ystart = self.YStart
                        ystop = self.YStop + 1
                        xges = xstop - xstart
                        yges = ystop - ystart
                        
                        if yges < xges:
                                dif = xges - yges
                                if (ystop + dif) <= self.ystop:
                                        ystop = ystop + dif
                                elif (ystart - dif) >= self.ystart:
                                        ystart = ystart - dif
                                elif (ystop + math.ceil(dif/2)) <= self.ystop and (ystart - math.floor(dif/2)) >= self.ystart:
                                        ystop = ystop + math.ceil(dif/2)
                                        ystart = ystart - math.floor(dif/2)
                                        
                print(str(xstart) + " x " + str(xstop))
                print(str(ystart) + " x " + str(ystop))
                print(self.roundup(np.amax(zRaw)))

                
                #Grid Setup                
                X = np.arange(xstart, xstop, 1)
                Y = np.arange(ystart, ystop, 1)

                if self.Range == True:
                        i = 0
                        XNew = []
                        while i < len(X):
                                XNew.append(X[i] * self.XBitWidth)
                                i += 1
                        X = XNew
                        
                        i = 0
                        YNew = []
                        while i < len(Y):
                                YNew.append(Y[i] * self.YBitWidth)
                                i += 1
                        Y = YNew
                        self.Scale = self.ScaleBarSize
                
                X, Y = np.meshgrid(X, Y)

                i = 0
                zPart = []
                Z = []
                xval = xstart
                yval = ystart
                while xval < xstop:
                        while yval < ystop:
                                zPart.append(zRaw[i])
                                i = i + 1
                                yval = yval + 1
                        Z.append(zPart)
                        zPart = []
                        xval = xval + 1
                        yval = ystart

                print(Z)
                Znp = np.array(Z)
                print(Znp)
                print(Znp.ndim)
                        
                #Style Setup
                if self.colors == 1:
                        cmap = plt.get_cmap('Spectral_r')                                                                                               #Spektralfarben
                elif self.colors == 2:
                        cmap = plt.get_cmap('gray_r')                                                                                                   #Graustufen
                elif self.colors == 3:
                        cmap = plt.get_cmap('bone')                                                                                                     #Blau zu Grün
                elif self.colors == 4:
                        cmap = plt.get_cmap('Wistia')                                                                                                   #Gelb zu Rot
                elif self.colors == 5:
                        cmap = plt.get_cmap('copper')                                                                                                   #Lila zu Gelb
                elif self.colors == 6:
                        cmap = plt.get_cmap('gist_heat')                                                                                                        #Graustufen
                elif self.colors == 7:
                        cmap = plt.get_cmap('winter')                                                                                                   #Blau zu Grün
                elif self.colors == 8:
                        cmap = plt.get_cmap('spring')                                                                                                   #Gelb zu Rot
                elif self.colors == 9:
                        cmap = plt.get_cmap('summer')                                                                                                   #Lila zu Gelb
                elif self.colors == 10:
                        cmap = plt.get_cmap('autumn')                                                                                                   #Graustufen
                elif self.colors == 11:
                        cmap = plt.get_cmap('hot_r')                                                                                                    #Blau zu Grün
                elif self.colors == 12:
                        cmap = plt.get_cmap('cool')                                                                                                    #Graustufen
                elif self.colors == 13:
                        cmap = plt.get_cmap('gist_ncar')                                                                                                    #Blau zu Grün
                elif self.colors == 14:
                        cmap = plt.get_cmap('nipy_spectral')                                                                                                  #Blau zu Grün
                elif self.colors == 15:
                        cmap = plt.get_cmap('Reds')                                                                                            #Lila zu Gelb

                levels = MaxNLocator(nbins=self.roundup(np.amax(zRaw))).tick_values(0, self.roundup(np.amax(zRaw)))                                                                              #characterizes the bar right
                norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)                                  

                #Figure Setup
                fig = plt.figure()
                ax = fig.gca(projection='3d')
                #surf = ax.plot_surface(X, Y, Znp, cmap=cm.coolwarm,
                #                       linewidth=0, antialiased=False)
                surf = ax.plot_surface(X, Y, Znp, cmap=cmap,
                                       linewidth=0, antialiased=False)

                # Customize the z axis.
                ax.set_zlim(0, self.roundup(np.amax(zRaw)))
                ax.zaxis.set_major_locator(LinearLocator(10))
                ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
                ax.set_xlabel(self.XAxis)
                ax.set_ylabel(self.YAxis)
                ax.set_zlabel(self.ZAxis)

                # Add a color bar which maps values to colors.
                fig.colorbar(surf, shrink=0.5, aspect=5)

                #ax.invert_yaxis()              


                #Plot and Save -----------------------------------------------------------------------------------------
                try:
                        plt.savefig(self.DateTime4)
                except:
                        print("Saving Plot not possible")

                try:
                        plt.show()                                                                                                                          #Plot
                except:
                        print("Plot not posible")


                #Ende --------------------------------------------------------------------------------------------------
                self.killBrian()

        def roundup(self, val):
                return int(math.ceil(val / 10.0)) * 10

        def killBrian(self):                                                                     
                print("Brian dead")


class PlotMeshCont:
        def __init__(self, FilePath, DataStart, XCol, YCol, PlotCol, Color, Plotname, Filename, Range, ScaleBar, Fontsize, Fontcolor, FontWeight, ScaleBarSize, ScaleBarSizeVertical, ScaleBarPosition, ScaleBarOffset, XAxis, YAxis, ZAxis, InvertX, InvertY, Zoom, XStart, XStop, YStart, YStop, UseLimits, LowerLimit, UpperLimit):
                self.file = FilePath
                self.datastart = DataStart
                self.colors = Color
                self.Plotname = Plotname
                self.DateTime4 = Filename
                print(self.DateTime4)

                self.ScaleBar = ScaleBar
                self.Fontsize = Fontsize
                self.Fontcolor = Fontcolor
                #self.ScaleBarSize = 11.5
                self.ScaleBarSize = ScaleBarSize                                        #in Pixel
                self.ScaleBarSizeVertical = ScaleBarSizeVertical                        #in Pixel
                
                self.Range = Range

                self.FontWeight = FontWeight                                            #or "normal"
                self.ScaleBarPosition = ScaleBarPosition                                #or "upper", "center", "right"
                self.ScaleBarOffset = ScaleBarOffset                                    #in Pixel

                self.XAxis = XAxis
                self.YAxis = YAxis
                self.ZAxis = ZAxis
                self.InvertX = InvertX
                self.InvertY = InvertY

                self.Zoom = Zoom
                self.XStart = XStart
                self.XStop = XStop
                self.YStart = YStart
                self.YStop = YStop

                self.XCol = XCol
                self.YCol = YCol
                self.PlotCol = int(PlotCol)

                self.UseLimits = UseLimits
                self.LowerLimit = LowerLimit
                self.UpperLimit = UpperLimit
                if self.UseLimits == False or self.UpperLimit <= self.LowerLimit:
                        self.LowerLimit = 0
                        self.UpperLimit = 0
                print("Colorbar-Limits: " + str(self.LowerLimit) + " x " + str(self.UpperLimit))


                #Scalebar calculation
                self.Scale = 0
                try:
                #if self.Range == True:
                        f = open(self.file, "r")
                        Line1 = f.readline()
                        Line2 = f.readline()
                        Line3 = f.readline()
                        Line4 = f.readline()
                        
                        i = 0
                        control = 0
                        BitValueRead = []
                        while i < len(Line4):
                                #print(Line4[i])
                                if Line4[i]=="\t":
                                        #print("Tab")
                                        control = 1
                                if Line4[i]==" ":
                                        #print("Space")
                                        control = 0
                                if control == 1 and Line4[i]!="\t":
                                        BitValueRead.append(Line4[i])
                                i += 1
                        i = 0
                        BitValText = ""
                        while i < len(BitValueRead):
                                BitValText += str(BitValueRead[i])
                                i += 1
                        print(BitValText)
                        BitValInt = int(BitValText)
                        print(str(BitValInt) + " Pixel")

                        
                        Line5 = f.readline()
                        control = 0
                        index = 0
                        i = 0
                        control = 0
                        RangeXRead = []
                        RangeYRead = []
                        while i < len(Line5):
                                #print(Line5[i])
                                if Line5[i]=="\t":
                                        #print("Tab")
                                        control = 1
                                if Line5[i]==" ":
                                        #print("Space")
                                        control = 0
                                        index += 1
                                if control == 1 and index == 0 and Line5[i]!="\t":
                                        RangeXRead.append(Line5[i])
                                if control == 1 and index == 0 and Line5[i]!="\t":
                                        RangeYRead.append(Line5[i])
                                i += 1
                        i = 0
                        RangeXText = ""
                        while i < len(RangeXRead):
                                RangeXText += str(RangeXRead[i])
                                i += 1
                        RangeXFloat = float(RangeXText)
                        print(str(RangeXFloat) + " nm")

                        i = 0
                        RangeYText = ""
                        while i < len(RangeYRead):
                                RangeYText += str(RangeYRead[i])
                                i += 1
                        RangeYFloat = float(RangeYText)
                        print(str(RangeYFloat) + " nm")
                        
                        f.close()
                        self.XBitWidth = ((RangeXFloat/1000)/BitValInt)
                        self.YBitWidth = ((RangeYFloat/1000)/BitValInt)
                        self.Scale = self.ScaleBarSize / self.XBitWidth
                        print(str(RangeXFloat) + "\t" + str(self.XBitWidth) + "\t" + str(RangeYFloat) + "\t" + str(self.YBitWidth) + "\t" + str(self.ScaleBarSize) + "\t" + str(self.XBitWidth) + "\t" + str(self.Scale))
                except:
                #else:
                        self.ScaleBar = False
                        self.Range = False
                        print("Flase")
                self.ScaleText = str(self.ScaleBarSize) + " \u03BCm"                                #Text under Bar

                self.run()
                        
        def run(self):  
                print("Plot start")                

                fontprops = fm.FontProperties(size=self.Fontsize, weight=self.FontWeight)

                #Open File ---------------------------------------------------------------------------------------------
                data_file = np.loadtxt(self.file, delimiter='\t', skiprows=self.datastart)
                xRaw = data_file[:,self.XCol]
                yRaw = data_file[:,self.YCol]
                zRaw = data_file[:,self.PlotCol]

                xstart = xRaw[0]
                ystart = yRaw[0]
                xstop = xRaw[len(xRaw)-1] + 1
                ystop = yRaw[len(yRaw)-1] + 1
                self.ystop = ystop
                self.ystart = ystart
                
                print(str(xstart) + " x " + str(xstop))
                print(str(ystart) + " x " + str(ystop))
                print(self.roundup(np.amax(zRaw)))

                
                #Grid Setup
                if self.Zoom == True:
                        xstart = self.XStart
                        xstop = self.XStop + 1
                        ystart = self.YStart
                        ystop = self.YStop + 1
                        xges = xstop - xstart
                        yges = ystop - ystart
                        
                        if yges < xges:
                                dif = xges - yges
                                if (ystop + dif) <= self.ystop:
                                        ystop = ystop + dif
                                elif (ystart - dif) >= self.ystart:
                                        ystart = ystart - dif
                                elif (ystop + math.ceil(dif/2)) <= self.ystop and (ystart - math.floor(dif/2)) >= self.ystart:
                                        ystop = ystop + math.ceil(dif/2)
                                        ystart = ystart - math.floor(dif/2)
                
                print(str(xstart) + " x " + str(xstop))
                print(str(ystart) + " x " + str(ystop))
                print(self.roundup(np.amax(zRaw)))

                
                #Grid Setup                
                X = np.arange(xstart, xstop, 1)
                Y = np.arange(ystart, ystop, 1)

                if self.Range == True:
                        i = 0
                        XNew = []
                        while i < len(X):
                                XNew.append(X[i] * self.XBitWidth)
                                i += 1
                        X = XNew
                        
                        i = 0
                        YNew = []
                        while i < len(Y):
                                YNew.append(Y[i] * self.YBitWidth)
                                i += 1
                        Y = YNew
                        self.Scale = self.ScaleBarSize
                
                X, Y = np.meshgrid(X, Y)

                i = 0
                zPart = []
                Z = []
                xval = xstart
                yval = ystart
                while xval < xstop:
                        while yval < ystop:
                                zPart.append(zRaw[i])
                                i = i + 1
                                yval = yval + 1
                        Z.append(zPart)
                        zPart = []
                        xval = xval + 1
                        yval = ystart


                #Style Setup
                if self.colors == 1:
                        cmap = plt.get_cmap('Spectral_r')                                                                                               #Spektralfarben
                elif self.colors == 2:
                        cmap = plt.get_cmap('gray_r')                                                                                                   #Graustufen
                elif self.colors == 3:
                        cmap = plt.get_cmap('bone')                                                                                                     #Blau zu Grün
                elif self.colors == 4:
                        cmap = plt.get_cmap('Wistia')                                                                                                   #Gelb zu Rot
                elif self.colors == 5:
                        cmap = plt.get_cmap('copper')                                                                                                   #Lila zu Gelb
                elif self.colors == 6:
                        cmap = plt.get_cmap('gist_heat')                                                                                                        #Graustufen
                elif self.colors == 7:
                        cmap = plt.get_cmap('winter')                                                                                                   #Blau zu Grün
                elif self.colors == 8:
                        cmap = plt.get_cmap('spring')                                                                                                   #Gelb zu Rot
                elif self.colors == 9:
                        cmap = plt.get_cmap('summer')                                                                                                   #Lila zu Gelb
                elif self.colors == 10:
                        cmap = plt.get_cmap('autumn')                                                                                                   #Graustufen
                elif self.colors == 11:
                        cmap = plt.get_cmap('hot_r')                                                                                                    #Blau zu Grün
                elif self.colors == 12:
                        cmap = plt.get_cmap('cool')                                                                                                    #Graustufen
                elif self.colors == 13:
                        cmap = plt.get_cmap('gist_ncar')                                                                                                    #Blau zu Grün
                elif self.colors == 14:
                        cmap = plt.get_cmap('nipy_spectral')                                                                                                  #Blau zu Grün
                elif self.colors == 15:
                        cmap = plt.get_cmap('Reds')                                                                                            #Lila zu Gelb

                levels = MaxNLocator(nbins=self.roundup(np.amax(zRaw))).tick_values(0, self.roundup(np.amax(zRaw)))                                                                              #characterizes the bar right
                norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)                                  

                #Figure Setup
                fig, (ax0, ax1)  = plt.subplots(nrows=2)                                                                                                      #Adds the plot to the figure

                im1 = ax0.pcolormesh(X, Y, Z, cmap=cmap, norm=norm)         

                cbar = plt.colorbar(im1)
                cbar.set_label(self.ZAxis)
            
                #fig.colorbar(im1, ax=ax0)
                #fig.set_label(self.ZAxis)
                ax0.set_title(self.Plotname)

                if self.ScaleBar == True:
                        scalebar = AnchoredSizeBar(ax0.transData,
                                   self.Scale, self.ScaleText, self.ScaleBarPosition, 
                                   pad=self.ScaleBarOffset,
                                   color=self.Fontcolor,
                                   frameon=False,
                                   size_vertical=self.ScaleBarSizeVertical,
                                   fontproperties=fontprops)
                        ax0.add_artist(scalebar)

                
                if self.InvertX == True:
                        ax0.invert_xaxis()
                if self.InvertY == True:
                        ax0.invert_yaxis()                                                                                                                  #invertiert die y-Achse


                ax0.set_xlabel(self.XAxis)
                ax0.set_ylabel(self.YAxis)
                ax0.xaxis.tick_top()                                                                                                            #setzt die x-Achse nach oben


                cf = ax1.contourf(X, Y, Z, levels=levels, cmap=cmap)

                cbar2 = plt.colorbar(cf)
                cbar2.set_label(self.ZAxis)
                
                ax1.set_title(self.Plotname)

                if self.ScaleBar == True:
                        scalebar = AnchoredSizeBar(ax1.transData,
                                   self.Scale, self.ScaleText, self.ScaleBarPosition, 
                                   pad=self.ScaleBarOffset,
                                   color=self.Fontcolor,
                                   frameon=False,
                                   size_vertical=self.ScaleBarSizeVertical,
                                   fontproperties=fontprops)
                        ax1.add_artist(scalebar)

                
                if self.InvertX == True:
                        ax1.invert_xaxis()
                if self.InvertY == True:
                        ax1.invert_yaxis()                                                                                                                  #invertiert die y-Achse


                ax1.set_xlabel(self.XAxis)
                ax1.set_ylabel(self.YAxis)
                ax1.xaxis.tick_top() 

                # adjust spacing between subplots so `ax1` title and `ax0` tick labels
                # don't overlap
                fig.tight_layout()

                #Plot and Save -----------------------------------------------------------------------------------------
                try:
                        plt.savefig(self.DateTime4)
                except:
                        print("Saving Plot not possible")

                try:
                        plt.show()                                                                                                                          #Plot
                except:
                        print("Plot not posible")


                #Ende --------------------------------------------------------------------------------------------------
                self.killBrian()

        def roundup(self, val):
                return int(math.ceil(val / 10.0)) * 10

        def killBrian(self):                                                                     
                print("Brian dead")


class PlotCont:
        def __init__(self, FilePath, DataStart, XCol, YCol, PlotCol, Color, Plotname, Filename, Range, ScaleBar, Fontsize, Fontcolor, FontWeight, ScaleBarSize, ScaleBarSizeVertical, ScaleBarPosition, ScaleBarOffset, XAxis, YAxis, ZAxis, InvertX, InvertY, Zoom, XStart, XStop, YStart, YStop, UseLimits, LowerLimit, UpperLimit):
                self.file = FilePath
                self.datastart = DataStart
                self.colors = Color
                self.Plotname = Plotname
                self.DateTime4 = Filename
                print(self.DateTime4)

                self.ScaleBar = ScaleBar
                self.Fontsize = Fontsize
                self.Fontcolor = Fontcolor
                #self.ScaleBarSize = 11.5
                self.ScaleBarSize = ScaleBarSize                                        #in Pixel
                self.ScaleBarSizeVertical = ScaleBarSizeVertical                        #in Pixel
                
                self.Range = Range

                self.FontWeight = FontWeight                                            #or "normal"
                self.ScaleBarPosition = ScaleBarPosition                                #or "upper", "center", "right"
                self.ScaleBarOffset = ScaleBarOffset                                    #in Pixel

                self.XAxis = XAxis
                self.YAxis = YAxis
                self.ZAxis = ZAxis
                self.InvertX = InvertX
                self.InvertY = InvertY

                self.Zoom = Zoom
                self.XStart = XStart
                self.XStop = XStop
                self.YStart = YStart
                self.YStop = YStop

                self.XCol = XCol
                self.YCol = YCol
                self.PlotCol = int(PlotCol)

                self.UseLimits = UseLimits
                self.LowerLimit = LowerLimit
                self.UpperLimit = UpperLimit
                if self.UseLimits == False or self.UpperLimit <= self.LowerLimit:
                        self.LowerLimit = 0
                        self.UpperLimit = 0
                print("Colorbar-Limits: " + str(self.LowerLimit) + " x " + str(self.UpperLimit))


                #Scalebar calculation
                self.Scale = 0
                try:
                #if self.Range == True:
                        f = open(self.file, "r")
                        Line1 = f.readline()
                        Line2 = f.readline()
                        Line3 = f.readline()
                        Line4 = f.readline()
                        
                        i = 0
                        control = 0
                        BitValueRead = []
                        while i < len(Line4):
                                #print(Line4[i])
                                if Line4[i]=="\t":
                                        #print("Tab")
                                        control = 1
                                if Line4[i]==" ":
                                        #print("Space")
                                        control = 0
                                if control == 1 and Line4[i]!="\t":
                                        BitValueRead.append(Line4[i])
                                i += 1
                        i = 0
                        BitValText = ""
                        while i < len(BitValueRead):
                                BitValText += str(BitValueRead[i])
                                i += 1
                        print(BitValText)
                        BitValInt = int(BitValText)
                        print(str(BitValInt) + " Pixel")

                        
                        Line5 = f.readline()
                        control = 0
                        index = 0
                        i = 0
                        control = 0
                        RangeXRead = []
                        RangeYRead = []
                        while i < len(Line5):
                                #print(Line5[i])
                                if Line5[i]=="\t":
                                        #print("Tab")
                                        control = 1
                                if Line5[i]==" ":
                                        #print("Space")
                                        control = 0
                                        index += 1
                                if control == 1 and index == 0 and Line5[i]!="\t":
                                        RangeXRead.append(Line5[i])
                                if control == 1 and index == 0 and Line5[i]!="\t":
                                        RangeYRead.append(Line5[i])
                                i += 1
                        i = 0
                        RangeXText = ""
                        while i < len(RangeXRead):
                                RangeXText += str(RangeXRead[i])
                                i += 1
                        RangeXFloat = float(RangeXText)
                        print(str(RangeXFloat) + " nm")

                        i = 0
                        RangeYText = ""
                        while i < len(RangeYRead):
                                RangeYText += str(RangeYRead[i])
                                i += 1
                        RangeYFloat = float(RangeYText)
                        print(str(RangeYFloat) + " nm")
                        
                        f.close()
                        self.XBitWidth = ((RangeXFloat/1000)/BitValInt)
                        self.YBitWidth = ((RangeYFloat/1000)/BitValInt)
                        self.Scale = self.ScaleBarSize / self.XBitWidth
                        print(str(RangeXFloat) + "\t" + str(self.XBitWidth) + "\t" + str(RangeYFloat) + "\t" + str(self.YBitWidth) + "\t" + str(self.ScaleBarSize) + "\t" + str(self.XBitWidth) + "\t" + str(self.Scale))
                except:
                #else:
                        self.ScaleBar = False
                        self.Range = False
                        print("Flase")
                self.ScaleText = str(self.ScaleBarSize) + " \u03BCm"                                #Text under Bar

                self.run()
                        
        def run(self):  
                print("Plot start")                

                fontprops = fm.FontProperties(size=self.Fontsize, weight=self.FontWeight)

                #Open File ---------------------------------------------------------------------------------------------
                data_file = np.loadtxt(self.file, delimiter='\t', skiprows=self.datastart)
                xRaw = data_file[:,self.XCol]
                yRaw = data_file[:,self.YCol]
                zRaw = data_file[:,self.PlotCol]

                xstart = xRaw[0]
                ystart = yRaw[0]
                xstop = xRaw[len(xRaw)-1] + 1
                ystop = yRaw[len(yRaw)-1] + 1
                self.ystop = ystop
                self.ystart = ystart
                
                print(str(xstart) + " x " + str(xstop))
                print(str(ystart) + " x " + str(ystop))
                print(self.roundup(np.amax(zRaw)))

                
                #Grid Setup
                if self.Zoom == True:
                        xstart = self.XStart
                        xstop = self.XStop + 1
                        ystart = self.YStart
                        ystop = self.YStop + 1
                        xges = xstop - xstart
                        yges = ystop - ystart
                        
                        if yges < xges:
                                dif = xges - yges
                                if (ystop + dif) <= self.ystop:
                                        ystop = ystop + dif
                                elif (ystart - dif) >= self.ystart:
                                        ystart = ystart - dif
                                elif (ystop + math.ceil(dif/2)) <= self.ystop and (ystart - math.floor(dif/2)) >= self.ystart:
                                        ystop = ystop + math.ceil(dif/2)
                                        ystart = ystart - math.floor(dif/2)

                
                #Grid Setup                
                X = np.arange(xstart, xstop, 1)
                Y = np.arange(ystart, ystop, 1)

                if self.Range == True:
                        i = 0
                        XNew = []
                        while i < len(X):
                                XNew.append(X[i] * self.XBitWidth)
                                i += 1
                        X = XNew
                        
                        i = 0
                        YNew = []
                        while i < len(Y):
                                YNew.append(Y[i] * self.YBitWidth)
                                i += 1
                        Y = YNew
                        self.Scale = self.ScaleBarSize
                
                X, Y = np.meshgrid(X, Y)

                i = 0
                zPart = []
                Z = []
                xval = xstart
                yval = ystart
                while xval < xstop:
                        while yval < ystop:
                                zPart.append(zRaw[i])
                                i = i + 1
                                yval = yval + 1
                        Z.append(zPart)
                        zPart = []
                        xval = xval + 1
                        yval = ystart


                #Style Setup
                if self.colors == 1:
                        cmap = plt.get_cmap('Spectral_r')                                                                                               #Spektralfarben
                elif self.colors == 2:
                        cmap = plt.get_cmap('gray_r')                                                                                                   #Graustufen
                elif self.colors == 3:
                        cmap = plt.get_cmap('bone')                                                                                                     #Blau zu Grün
                elif self.colors == 4:
                        cmap = plt.get_cmap('Wistia')                                                                                                   #Gelb zu Rot
                elif self.colors == 5:
                        cmap = plt.get_cmap('copper')                                                                                                   #Lila zu Gelb
                elif self.colors == 6:
                        cmap = plt.get_cmap('gist_heat')                                                                                                        #Graustufen
                elif self.colors == 7:
                        cmap = plt.get_cmap('winter')                                                                                                   #Blau zu Grün
                elif self.colors == 8:
                        cmap = plt.get_cmap('spring')                                                                                                   #Gelb zu Rot
                elif self.colors == 9:
                        cmap = plt.get_cmap('summer')                                                                                                   #Lila zu Gelb
                elif self.colors == 10:
                        cmap = plt.get_cmap('autumn')                                                                                                   #Graustufen
                elif self.colors == 11:
                        cmap = plt.get_cmap('hot_r')                                                                                                    #Blau zu Grün
                elif self.colors == 12:
                        cmap = plt.get_cmap('cool')                                                                                                    #Graustufen
                elif self.colors == 13:
                        cmap = plt.get_cmap('gist_ncar')                                                                                                    #Blau zu Grün
                elif self.colors == 14:
                        cmap = plt.get_cmap('nipy_spectral')                                                                                                  #Blau zu Grün
                elif self.colors == 15:
                        cmap = plt.get_cmap('Reds')                                                                                            #Lila zu Gelb

                levels = MaxNLocator(nbins=self.roundup(np.amax(zRaw))).tick_values(0, self.roundup(np.amax(zRaw)))                                                                              #characterizes the bar right
                norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)                                  

                #Figure Setup
                fig, ax1  = plt.subplots()                                                                                                            #setzt die x-Achse nach oben


                cf = ax1.contourf(X, Y, Z, levels=levels, cmap=cmap)
                
                cbar = plt.colorbar(cf)
                cbar.set_label(self.ZAxis)
                ax1.set_title(self.Plotname)

                if self.ScaleBar == True:
                        scalebar = AnchoredSizeBar(ax1.transData,
                                   self.Scale, self.ScaleText, self.ScaleBarPosition, 
                                   pad=self.ScaleBarOffset,
                                   color=self.Fontcolor,
                                   frameon=False,
                                   size_vertical=self.ScaleBarSizeVertical,
                                   fontproperties=fontprops)
                        ax1.add_artist(scalebar)

                
                if self.InvertX == True:
                        ax1.invert_xaxis()
                if self.InvertY == True:
                        ax1.invert_yaxis()                                                                                                                 #invertiert die y-Achse


                ax1.set_xlabel(self.XAxis)
                ax1.set_ylabel(self.YAxis)
                ax1.xaxis.tick_top() 

                # adjust spacing between subplots so `ax1` title and `ax0` tick labels
                # don't overlap

                #Plot and Save -----------------------------------------------------------------------------------------
                try:
                        plt.savefig(self.DateTime4)
                except:
                        print("Saving Plot not possible")

                try:
                        plt.show()                                                                                                                          #Plot
                except:
                        print("Plot not posible")


                #Ende --------------------------------------------------------------------------------------------------
                self.killBrian()

        def roundup(self, val):
                return int(math.ceil(val / 10.0)) * 10

        def killBrian(self):                                                                     
                print("Brian dead")

class PlotScatter:
        def __init__(self, FilePath, DataStart, XCol, YCol, PlotCol, Color, Plotname, Filename, Range, ScaleBar, Fontsize, Fontcolor, FontWeight, ScaleBarSize, ScaleBarSizeVertical, ScaleBarPosition, ScaleBarOffset, XAxis, YAxis, ZAxis, InvertX, InvertY, Zoom, XStart, XStop, YStart, YStop, UseLimits, LowerLimit, UpperLimit):
                self.file = FilePath
                self.datastart = DataStart
                self.colors = Color
                self.Plotname = Plotname
                self.DateTime4 = Filename
                print(self.DateTime4)

                self.ScaleBar = ScaleBar
                self.Fontsize = Fontsize
                self.Fontcolor = Fontcolor
                #self.ScaleBarSize = 11.5
                self.ScaleBarSize = ScaleBarSize                                        #in Pixel
                self.ScaleBarSizeVertical = ScaleBarSizeVertical                        #in Pixel
                
                self.Range = Range

                self.FontWeight = FontWeight                                            #or "normal"
                self.ScaleBarPosition = ScaleBarPosition                                #or "upper", "center", "right"
                self.ScaleBarOffset = ScaleBarOffset                                    #in Pixel

                self.XAxis = XAxis
                self.YAxis = YAxis
                self.ZAxis = ZAxis
                self.InvertX = InvertX
                self.InvertY = InvertY

                self.Zoom = Zoom
                self.XStart = XStart
                self.XStop = XStop
                self.YStart = YStart
                self.YStop = YStop

                self.XCol = XCol
                self.YCol = YCol
                self.PlotCol = int(PlotCol)

                self.UseLimits = UseLimits
                self.LowerLimit = LowerLimit
                self.UpperLimit = UpperLimit
                if self.UseLimits == False or self.UpperLimit <= self.LowerLimit:
                        self.LowerLimit = 0
                        self.UpperLimit = 0
                print("Colorbar-Limits: " + str(self.LowerLimit) + " x " + str(self.UpperLimit))


                #Scalebar calculation
                self.Scale = 0
                try:
                #if self.Range == True:
                        f = open(self.file, "r")
                        Line1 = f.readline()
                        Line2 = f.readline()
                        Line3 = f.readline()
                        Line4 = f.readline()
                        
                        i = 0
                        control = 0
                        BitValueRead = []
                        while i < len(Line4):
                                #print(Line4[i])
                                if Line4[i]=="\t":
                                        #print("Tab")
                                        control = 1
                                if Line4[i]==" ":
                                        #print("Space")
                                        control = 0
                                if control == 1 and Line4[i]!="\t":
                                        BitValueRead.append(Line4[i])
                                i += 1
                        i = 0
                        BitValText = ""
                        while i < len(BitValueRead):
                                BitValText += str(BitValueRead[i])
                                i += 1
                        print(BitValText)
                        BitValInt = int(BitValText)
                        print(str(BitValInt) + " Pixel")

                        
                        Line5 = f.readline()
                        control = 0
                        index = 0
                        i = 0
                        control = 0
                        RangeXRead = []
                        RangeYRead = []
                        while i < len(Line5):
                                #print(Line5[i])
                                if Line5[i]=="\t":
                                        #print("Tab")
                                        control = 1
                                if Line5[i]==" ":
                                        #print("Space")
                                        control = 0
                                        index += 1
                                if control == 1 and index == 0 and Line5[i]!="\t":
                                        RangeXRead.append(Line5[i])
                                if control == 1 and index == 0 and Line5[i]!="\t":
                                        RangeYRead.append(Line5[i])
                                i += 1
                        i = 0
                        RangeXText = ""
                        while i < len(RangeXRead):
                                RangeXText += str(RangeXRead[i])
                                i += 1
                        RangeXFloat = float(RangeXText)
                        print(str(RangeXFloat) + " nm")

                        i = 0
                        RangeYText = ""
                        while i < len(RangeYRead):
                                RangeYText += str(RangeYRead[i])
                                i += 1
                        RangeYFloat = float(RangeYText)
                        print(str(RangeYFloat) + " nm")
                        
                        f.close()
                        self.XBitWidth = ((RangeXFloat/1000)/BitValInt)
                        self.YBitWidth = ((RangeYFloat/1000)/BitValInt)
                        self.Scale = self.ScaleBarSize / self.XBitWidth
                        print(str(RangeXFloat) + "\t" + str(self.XBitWidth) + "\t" + str(RangeYFloat) + "\t" + str(self.YBitWidth) + "\t" + str(self.ScaleBarSize) + "\t" + str(self.XBitWidth) + "\t" + str(self.Scale))
                except:
                #else:
                        self.ScaleBar = False
                        self.Range = False
                        print("Flase")
                self.ScaleText = str(self.ScaleBarSize) + " \u03BCm"                                #Text under Bar

                self.run()
                        
        def run(self):  
                print("Plot start")                

                fontprops = fm.FontProperties(size=self.Fontsize, weight=self.FontWeight)

                #Open File ---------------------------------------------------------------------------------------------
                data_file = np.loadtxt(self.file, delimiter='\t', skiprows=self.datastart)
                xRaw = data_file[:,self.XCol]
                yRaw = data_file[:,self.YCol]
                zRaw = data_file[:,self.PlotCol]

                xstart = xRaw[0]
                ystart = yRaw[0]
                xstop = xRaw[len(xRaw)-1] + 1
                ystop = yRaw[len(yRaw)-1] + 1
                self.ystop = ystop
                self.ystart = ystart
                
                print(str(xstart) + " x " + str(xstop))
                print(str(ystart) + " x " + str(ystop))
                print(self.roundup(np.amax(zRaw)))

                
                #Grid Setup
                if self.Zoom == True:
                        xstart = self.XStart
                        xstop = self.XStop + 1
                        ystart = self.YStart
                        ystop = self.YStop + 1
                        xges = xstop - xstart
                        yges = ystop - ystart
                        
                        if yges < xges:
                                dif = xges - yges
                                if (ystop + dif) <= self.ystop:
                                        ystop = ystop + dif
                                elif (ystart - dif) >= self.ystart:
                                        ystart = ystart - dif
                                elif (ystop + math.ceil(dif/2)) <= self.ystop and (ystart - math.floor(dif/2)) >= self.ystart:
                                        ystop = ystop + math.ceil(dif/2)
                                        ystart = ystart - math.floor(dif/2)

                #Style Setup
                if self.colors == 1:
                        cmap = plt.get_cmap('Spectral_r')                                                                                               #Spektralfarben
                elif self.colors == 2:
                        cmap = plt.get_cmap('gray_r')                                                                                                   #Graustufen
                elif self.colors == 3:
                        cmap = plt.get_cmap('bone')                                                                                                     #Blau zu Grün
                elif self.colors == 4:
                        cmap = plt.get_cmap('Wistia')                                                                                                   #Gelb zu Rot
                elif self.colors == 5:
                        cmap = plt.get_cmap('copper')                                                                                                   #Lila zu Gelb
                elif self.colors == 6:
                        cmap = plt.get_cmap('gist_heat')                                                                                                        #Graustufen
                elif self.colors == 7:
                        cmap = plt.get_cmap('winter')                                                                                                   #Blau zu Grün
                elif self.colors == 8:
                        cmap = plt.get_cmap('spring')                                                                                                   #Gelb zu Rot
                elif self.colors == 9:
                        cmap = plt.get_cmap('summer')                                                                                                   #Lila zu Gelb
                elif self.colors == 10:
                        cmap = plt.get_cmap('autumn')                                                                                                   #Graustufen
                elif self.colors == 11:
                        cmap = plt.get_cmap('hot_r')                                                                                                    #Blau zu Grün
                elif self.colors == 12:
                        cmap = plt.get_cmap('cool')                                                                                             #Lila zu Gelb
                              

                #Figure Setup
                fig, ax1  = plt.subplots()                                                                                                      #Adds the plot to the figure
              
                im1 = ax1.scatter(xRaw, yRaw, c=zRaw, cmap=cmap, s=200, marker='s')
            
                fig.colorbar(im1, ax=ax1)
                ax1.set_title(self.Plotname)

                if self.InvertX == True:
                        ax1.invert_xaxis()
                if self.InvertY == True:
                        ax1.invert_yaxis()                                                                                                                 #invertiert die y-Achse


                ax1.set_xlabel(self.XAxis)
                ax1.set_ylabel(self.YAxis)                                                                                                                #invertiert die y-Achse
                ax1.xaxis.tick_top()                                                                                                            #setzt die x-Achse nach oben


                #Plot and Save -----------------------------------------------------------------------------------------
                try:
                        plt.savefig(self.DateTime4)
                except:
                        print("Saving Plot not possible")

                try:
                        plt.show()                                                                                                                          #Plot
                except:
                        print("Plot not posible")


                #Ende --------------------------------------------------------------------------------------------------
                self.killBrian()

        def roundup(self, val):
                return int(math.ceil(val / 10.0)) * 10

        def killBrian(self):                                                                     
                print("Brian dead")


class PlotNormal:
        def __init__(self, FilePath, DataStart, XCol, YCol, PlotCol, Color, Plotname, Filename, Range, ScaleBar, Fontsize, Fontcolor, FontWeight, ScaleBarSize, ScaleBarSizeVertical, ScaleBarPosition, ScaleBarOffset, XAxis, YAxis, ZAxis, InvertX, InvertY, Zoom, XStart, XStop, YStart, YStop, UseLimits, LowerLimit, UpperLimit):
                self.file = FilePath
                self.datastart = DataStart
                self.colors = Color
                self.Plotname = Plotname
                self.DateTime4 = Filename
                print(self.DateTime4)

                self.ScaleBar = ScaleBar
                self.Fontsize = Fontsize
                self.Fontcolor = Fontcolor
                #self.ScaleBarSize = 11.5
                self.ScaleBarSize = ScaleBarSize                                        #in Pixel
                self.ScaleBarSizeVertical = ScaleBarSizeVertical                        #in Pixel
                
                self.Range = Range

                self.FontWeight = FontWeight                                            #or "normal"
                self.ScaleBarPosition = ScaleBarPosition                                #or "upper", "center", "right"
                self.ScaleBarOffset = ScaleBarOffset                                    #in Pixel

                self.XAxis = XAxis
                self.YAxis = YAxis
                self.ZAxis = ZAxis
                self.InvertX = InvertX
                self.InvertY = InvertY

                self.Zoom = Zoom
                self.XStart = XStart
                self.XStop = XStop
                self.YStart = YStart
                self.YStop = YStop

                self.XCol = XCol
                self.YCol = YCol
                self.PlotCol = int(PlotCol)

                #Scalebar calculation
                self.Scale = 0
                try:
                #if self.Range == True:
                        f = open(self.file, "r")
                        Line1 = f.readline()
                        Line2 = f.readline()
                        Line3 = f.readline()
                        Line4 = f.readline()
                        
                        i = 0
                        control = 0
                        BitValueRead = []
                        while i < len(Line4):
                                print(Line4[i])
                                if Line4[i]=="\t":
                                        print("Tab")
                                        control = 1
                                if Line4[i]==" ":
                                        print("Space")
                                        control = 0
                                if control == 1 and Line4[i]!="\t":
                                        BitValueRead.append(Line4[i])
                                i += 1
                        i = 0
                        BitValText = ""
                        while i < len(BitValueRead):
                                BitValText += str(BitValueRead[i])
                                i += 1
                        print(BitValText)
                        BitValInt = int(BitValText)
                        print(str(BitValInt) + " Pixel")

                        
                        Line5 = f.readline()
                        control = 0
                        index = 0
                        i = 0
                        control = 0
                        RangeXRead = []
                        RangeYRead = []
                        while i < len(Line5):
                                print(Line5[i])
                                if Line5[i]=="\t":
                                        print("Tab")
                                        control = 1
                                if Line5[i]==" ":
                                        print("Space")
                                        control = 0
                                        index += 1
                                if control == 1 and index == 0 and Line5[i]!="\t":
                                        RangeXRead.append(Line5[i])
                                if control == 1 and index == 0 and Line5[i]!="\t":
                                        RangeYRead.append(Line5[i])
                                i += 1
                        i = 0
                        RangeXText = ""
                        while i < len(RangeXRead):
                                RangeXText += str(RangeXRead[i])
                                i += 1
                        RangeXFloat = float(RangeXText)
                        print(str(RangeXFloat) + " nm")

                        i = 0
                        RangeYText = ""
                        while i < len(RangeYRead):
                                RangeYText += str(RangeYRead[i])
                                i += 1
                        RangeYFloat = float(RangeYText)
                        print(str(RangeYFloat) + " nm")
                        
                        f.close()
                        self.XBitWidth = ((RangeXFloat/1000)/BitValInt)
                        self.YBitWidth = ((RangeYFloat/1000)/BitValInt)
                        self.Scale = self.ScaleBarSize / self.XBitWidth
                        print(str(RangeXFloat) + "\t" + str(self.XBitWidth) + "\t" + str(RangeYFloat) + "\t" + str(self.YBitWidth) + "\t" + str(self.ScaleBarSize) + "\t" + str(self.XBitWidth) + "\t" + str(self.Scale))
                except:
                #else:
                        self.ScaleBar = False
                        self.Range = False
                        print("Flase")
                self.ScaleText = str(self.ScaleBarSize) + " \u03BCm"                                #Text under Bar

                self.run()
                        
        def run(self):  
                print("Plot start")                

                fontprops = fm.FontProperties(size=self.Fontsize, weight=self.FontWeight)

                #Open File ---------------------------------------------------------------------------------------------
                data_file = np.loadtxt(self.file, delimiter='\t', skiprows=self.datastart)
                xRaw = data_file[:,self.XCol]
                yRaw = data_file[:,self.YCol]
                zRaw = data_file[:,self.PlotCol]

                xstart = xRaw[0]
                ystart = yRaw[0]
                xstop = xRaw[len(xRaw)-1] + 1
                ystop = yRaw[len(yRaw)-1] + 1
                self.ystop = ystop
                self.ystart = ystart
                
                print(str(xstart) + " x " + str(xstop))
                print(str(ystart) + " x " + str(ystop))
                print(self.roundup(np.amax(zRaw)))

                
                #Grid Setup
                if self.Zoom == True:
                        xstart = self.XStart
                        xstop = self.XStop + 1
                        ystart = self.YStart
                        ystop = self.YStop + 1
                        xges = xstop - xstart
                        yges = ystop - ystart
                        
                        if yges < xges:
                                dif = xges - yges
                                if (ystop + dif) <= self.ystop:
                                        ystop = ystop + dif
                                elif (ystart - dif) >= self.ystart:
                                        ystart = ystart - dif
                                elif (ystop + math.ceil(dif/2)) <= self.ystop and (ystart - math.floor(dif/2)) >= self.ystart:
                                        ystop = ystop + math.ceil(dif/2)
                                        ystart = ystart - math.floor(dif/2)

                #Define Plot -------------------------------------------------------------------------------------------                                                     
                plt.plot(x,y, 'ro')                                                         
                plt.plot(x,z, 'b.')
                plt.legend(['Yval','Zval'], loc='best')
                plt.xlabel('x [nm]')
                plt.ylabel('y [counts]')

                #Plot and Save -----------------------------------------------------------------------------------------
                try:
                        plt.savefig(self.DateTime4)
                except:
                        print("Saving Plot not possible")

                try:
                        plt.show()                                                                                                                          #Plot
                except:
                        print("Plot not posible")


                #Ende --------------------------------------------------------------------------------------------------
                self.killBrian()

        def killBrian(self):                                                                     
                print("Brian dead")


#PlotMesh()
