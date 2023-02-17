import numpy as np
import pygame
import random
from PIL import Image
BLACK=(0,0,0)
WHITE=(255,255,255)
def AveragePixels(pixels):
        RA=[i.Get()[0]for i in pixels]
        R=sum (RA)//len(RA)
        GA=[i.Get()[1]for i in pixels]
        G=sum (GA)//len(GA)
        BA=[i.Get()[2]for i in pixels]
        B=sum (BA)//len(BA)
        return(R,G,B)
def EncloseIn256(val):
    if val<0:
        val=0
    if val>255:
        val=255
    return val
class Pixel:
    def __init__(self,rgb):
        self.RGB=rgb
        self.Weight = sum(rgb)//3
    def Set(self,rgb):
        if len(rgb)==3:
            self.RGB=rgb
            self.Weight = sum(rgb)//3
        else:
            print("Error")
    def CheckRGB(self):
        self.RGB=(EncloseIn256(self.RGB[0]),EncloseIn256(self.RGB[1]),EncloseIn256(self.RGB[2]))
    def Get(self):
        return self.RGB
    def GetGrey(self):
        return (self.Weight,self.Weight,self.Weight)
    def Lightness(self,percent):
        self.RGB=(round(self.RGB[0]*percent/100),round(self.RGB[1]*percent/100),round(self.RGB[2]*percent/100))
        self.CheckRGB()
    
class IMG:
    def __init__(self,size_x=0,size_y=0):
        self.pixels=[]
        self.size_x=size_x
        self.size_y=size_y
        for i in range(size_x):
            for i in range(size_y):
                self.pixels.append(Pixel(WHITE))
    def Show(self):
        pygame.init()
        SCREEN = pygame.display.set_mode((self.size_x, self.size_y))
        SCREEN.fill((125,125,125))
        block_size = 1
        for x in range(self.size_x):
            for y in range(self.size_y):
                rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
                #pygame.draw.rect(SCREEN, ((x*y)%256,(x**y)%256,(x-y)%256), rect)              predobra slika!!
                pygame.draw.rect(SCREEN, (self.pixels[x+y*self.size_x].Get()), rect)
        pygame.display.update()
    def SwapValues(self):
        self.size_x,self.size_y=self.size_y,self.size_x
    def Resize(self,x,y,setPixels=True):
        self.size_x=x
        self.size_y=y
        if (setPixels):
            self.pixels=[]
            for i in range(self.size_x):
                for i in range(self.size_y):
                    self.pixels.append(Pixel(WHITE))  #--- Razmisli bili resize funkcija tribala resetirat pixele ili mozda provjeravat jel broj pixela jos uvik visina * sirina
    def GenerateFromJPG(self,name):
        img2=Image.open(name)
        list_of_pixels = list(img2.getdata())
        cnt=0
        self.Resize(img2.size[0],img2.size[1])
        for pixel in list_of_pixels:
            self.pixels[cnt].Set(pixel)
            cnt+=1
    def ShowBlackAndWhite(self):
        pygame.init()
        SCREEN = pygame.display.set_mode((self.size_x, self.size_y))
        SCREEN.fill((125,125,125))
        block_size = 1
        for x in range(self.size_x):
            for y in range(self.size_y):
                rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
                pygame.draw.rect(SCREEN, (self.pixels[x+y*self.size_x].GetGrey()), rect)
        pygame.display.update()
    
        
    def CutHeight(self):
        B = np.reshape(self.pixels, (self.size_y, self.size_x))
        self.pixels=[]
        for i in range(0,len(B),2):
            for j in range(len(B[i])):
                avg=AveragePixels((B[i][j],B[i+1][j]))
                newPixel=Pixel(avg)
                self.pixels.append(newPixel)
        self.Resize(self.size_x,self.size_y//2,False)
    def CutWidth(self):
        new=[]
        for i in range(0,len(self.pixels),2):
            avg=AveragePixels((self.pixels[i],self.pixels[i+1]))
            newPixel=Pixel(avg)
            new.append(newPixel)
        self.pixels=new
        self.Resize(self.size_x//2,self.size_y,False)

                
    def Turn270(self): ## Nekako umisto 90 okrice za 270
        matrix = []
        B = np.reshape(self.pixels, (self.size_y, self.size_x))  #Pretvaranje arraya u matricu 
        self.pixels=[]
        new_matrix = [[B[j][i] for j in range(len(B))] for i in range(len(B[0])-1,-1,-1)] #Okrecanje matrice za 90 stupnjeva
        for row in new_matrix:
            for pixel in row:
                self.pixels.append(pixel)
        self.SwapValues() # Okrecanje size_x i size_y
    def Turn180(self):
        self.Turn270()
        self.Turn270()
    def Turn90(self):
        self.Turn180()
        self.Turn270()
    def Brighten(self,percent):
        for pixel in self.pixels:
            pixel.Lightness(100+percent)
    def Darken(self,percent):
        for pixel in self.pixels:
            pixel.Lightness(100-percent)



def main():       
    img = IMG()
    img.GenerateFromJPG('image.jpg')
    img.Show()
    img.Brighten(70)
    img.Darken(58)
    img.Show()

if __name__=='__main__':
    main()

