# -*- coding: utf-8 -*-
import pygame
from pygame.locals import QUIT
from pygame.locals import KEYDOWN
from pygame.locals import K_ESCAPE
from pygame.locals import MOUSEBUTTONDOWN
from pygame.locals import MOUSEMOTION
from pygame.locals import MOUSEBUTTONUP
import math
import requests
import time
import random
import sys

# pip install pywin32
# pip install PyInstaller


class Brush:
    def __init__(self, screen):
        self.screen = screen
        self.color = (0, 0, 0)
        self.size = 9
        self.drawing = False
        self.last_pos = None
        self.style = False
        self.brush = pygame.image.load("data/img/brush.png").convert_alpha()
        self.brush_now = self.brush.subsurface((0, 0), (self.size, self.size))
        pygame.font.init()
        self.fontObj = pygame.font.Font('data/simkai.ttf', 16)  # 通过字体文件获得字体对象
        self.count=1
        self.url='http://192.168.20.211'

    def start_draw(self, pos):
        self.drawing = True
        self.last_pos = pos

    def end_draw(self):
        self.drawing = False

    def set_brush_style(self, style):
        print("* set brush style to", style)
        self.style = style

    def get_brush_style(self):
        return self.style

    def get_current_brush(self):
        return self.brush_now

    def set_size(self, size):
        if size < 1:
            size = 1
        elif size > 32:
            size = 32
        print("* set brush size to", size)
        self.size = size
        self.brush_now = self.brush.subsurface((0, 0), (size*2, size*2))

    def get_size(self):
        return self.size

    def set_color(self, color):
        self.color = color
        for i in range(self.brush.get_width()):
            for j in range(self.brush.get_height()):
                self.brush.set_at((i, j),
                                  color + (self.brush.get_at((i, j)).a,))

    def get_color(self):
        return self.color

    def draw(self, pos):
        if self.drawing:
            for p in self._get_points(pos):
                if self.style:
                    self.screen.blit(self.brush_now, p)
                else:
                    pygame.draw.circle(self.screen, self.color, p, self.size)
            self.last_pos = pos

    def _get_points(self, pos):
        points = [(self.last_pos[0], self.last_pos[1])]
        len_x = pos[0] - self.last_pos[0]
        len_y = pos[1] - self.last_pos[1]
        length = math.sqrt(len_x**2 + len_y**2)
        step_x = len_x / length
        step_y = len_y / length
        for i in range(int(length)):
            points.append((points[-1][0] + step_x, points[-1][1] + step_y))
        points = map(lambda x: (int(0.5 + x[0]), int(0.5 + x[1])), points)
        return list(set(points))

    def drawText(self,text,posx,posy,fontColor=(0,0,0),backgroudColor=(255,255,255)):
       
        textSurfaceObj = self.fontObj.render(text, True,fontColor,backgroudColor)  # 配置要显示的文字
        textRectObj = textSurfaceObj.get_rect()  # 获得要显示的对象的rect
        textRectObj.x = posx
        textRectObj.y = posy  # 设置显示对象的坐标
        self.screen.blit(textSurfaceObj, textRectObj)  # 绘制字

    def clear(self):
        print("clear!")
        self.screen.fill((255, 255, 255))
        self.drawText("",80,570)
    
    def set_url(self,url):
        self.url=url
    def send_to_server(self):
        print("send_to_server Test!")
        # print(self.screen)
        # self.drawText("",80,570)
        self.count+=1
        str_time=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+"_"+str(random.randint(100,999))

        fname = "output/num_%s.png" % str_time
        # newimg = pygame.transform.chop(self.screen, (80, 0, 710, 600))
        newimg = pygame.transform.chop(self.screen, (0, 0, 80, 0))
        
        # w1=0
        # ar = pygame.PixelArray(newimg)

        gw=pygame.Surface.get_width(newimg)
        gh=pygame.Surface.get_height(newimg)

        newimg = newimg.subsurface((0 , 0, gw, gh-80))

        gw=pygame.Surface.get_width(newimg)
        gh=pygame.Surface.get_height(newimg)

        # print("gw",gw)
        # print("gh",gh)
        top=0
        find=False
        for h in range(gh) :
            if find:
                break
            for w in range(gw):
                # print(w,h)
                color=newimg.get_at((w,h))
                if (color.r==255 and color.g==255 and color.b==255) :
                    pass
                else:
                    find=True
                    break

            if not find:
                top+=1
        # print("top",top)
        bottom=0
        find=False
        for h in range(gh-1,top,-1) :
            if find:
                break
            for w in range(gw):
                # print(w,h)
                color=newimg.get_at((w,h))
                if (color.r==255 and color.g==255 and color.b==255) :
                   pass
                else:
                    find=True
                    break
            if not find:
                bottom+=1
        # print("bottom=",bottom)
        
        left=0
        find=False
        for w in range(gw) :
            if find:
                break
            for h in range(top,gh-bottom):
                color=newimg.get_at((w,h))
                if (color.r==255 and color.g==255 and color.b==255) :
                   pass
                else:
                    find=True
                    break
            if not find:
                left+=1
        # print("left=",left)
        right=0
        find=False
        for w in range(gw-1,left,-1) :
            if find:
                break
            for h in range(top,gh-bottom):
                color=newimg.get_at((w,h))
                if (color.r==255 and color.g==255 and color.b==255) :
                    pass
                else:
                    # print("w,h=",w,h)
                    find=True
                    break
            if not find:
                right+=1
        # print("right=",right)

        # cropedimg=cropped.blit(newimg, (0, 0), (30, 30, 80, 80))

        min=5
        if left>min :
            left-=min
        if right>min :
            right-=min
        if top>min :
            top-=min
        if bottom>min :
            bottom-=min



        crop_w=gw-right-left
        crop_h=gh-bottom-top
        ddn=int(abs(crop_h-crop_w)/2)
        if crop_h>crop_w:
            left-=ddn
            right-=ddn
            if left<0:
                left=0
            if right<0:
                right=0
        else:
            top-=ddn
            bottom-=ddn
            if top<0:
                top=0
            if bottom<0:
                bottom=0

        crop_w=gw-right-left
        crop_h=gh-bottom-top

        # print("crop_w=",crop_w)
        # print("crop_h=",crop_h)

        print("final left=",left)

        croped_img = newimg.subsurface((left , top, crop_w, crop_h))

        newimg2 = pygame.transform.scale(croped_img, (28, 28))

        # newimg2.blit(buttonStates, (0, 0), (30, 30, 80, 80))

        # subsurface = newimg2.subsurface((x, y, width, height))

        pygame.image.save(newimg2, fname)
        # pygame.image.save(newimg, fname+"1.png")
        # pygame.image.save(croped_img, fname+"2.png")
        print("save:",fname)
        self.clear()
        payload = {'path': fname}
        # server_url='http://192.168.20.211'
        # print("server_url:",self.url)
        try:
            files={'file':('test.png',open(fname,'rb'),'image/png')}
            r = requests.post(self.url, params=payload,files=files)
            print(r.text)
            self.drawText(r.text,80,570)
        except IOError:
            print("Error: IOError :",self.url)
        else:
            print("request ok.")



class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.brush = None
        self.colors = [
            (0xff, 0x00, 0xff), (0x80, 0x00, 0x80),
            (0x00, 0x00, 0xff), (0x00, 0x00, 0x80),
            (0x00, 0xff, 0xff), (0x00, 0x80, 0x80),
            (0x00, 0xff, 0x00), (0x00, 0x80, 0x00),
            (0xff, 0xff, 0x00), (0x80, 0x80, 0x00),
            (0xff, 0x00, 0x00), (0x80, 0x00, 0x00),
            (0xc0, 0xc0, 0xc0), (0xff, 0xff, 0xff),
            (0x00, 0x00, 0x00), (0x80, 0x80, 0x80),
        ]
        self.colors_rect = []
        for (i, rgb) in enumerate(self.colors):
            rect = pygame.Rect(10 + i % 2 * 32, 254 + (i - i % 2) * 16, 32, 32)
            self.colors_rect.append(rect)
        self.pens = [
            pygame.image.load("data/img/pen1.png").convert_alpha(),
            pygame.image.load("data/img/pen2.png").convert_alpha(),
        ]
        self.pens_rect = []
        for (i, img) in enumerate(self.pens):
            rect = pygame.Rect(10, 10 + i * 64, 64, 64)
            self.pens_rect.append(rect)

        self.sizes = [
            pygame.image.load("data/img/big.png").convert_alpha(),
            pygame.image.load("data/img/small.png").convert_alpha()
        ]
        self.sizes_rect = []
        for (i, img) in enumerate(self.sizes):
            rect = pygame.Rect(10 + i * 32, 138, 32, 32)
            self.sizes_rect.append(rect)

        self.tools = [
            pygame.image.load("data/img/clear.png").convert_alpha(),
            pygame.image.load("data/img/test.png").convert_alpha()
        ]
        self.tools_rect = []
        self.tools_rect.append(pygame.Rect(10, 530, 60, 30))
        self.tools_rect.append(pygame.Rect(10, 560, 60, 30))
        self.url='http://192.168.20.211'

    def set_brush(self, brush):
        self.brush = brush
        self.brush.set_url(self.url)

    def set_url(self,url):
        self.url=url

        if self.brush is not None:
            self.brush.set_url(url)
    def draw(self):
        for (i, img) in enumerate(self.pens):
            self.screen.blit(img, self.pens_rect[i].topleft)
        for (i, img) in enumerate(self.sizes):
            self.screen.blit(img, self.sizes_rect[i].topleft)
        for (i, img) in enumerate(self.tools):
            self.screen.blit(img, self.tools_rect[i].topleft)

        self.screen.fill((255, 255, 255), (10, 180, 64, 64))
        pygame.draw.rect(self.screen, (0, 0, 0), (10, 180, 64, 64), 1)
        size = self.brush.get_size()
        x = 10 + 32
        y = 180 + 32
        if self.brush.get_brush_style():
            x = x - size
            y = y - size
            self.screen.blit(self.brush.get_current_brush(), (x, y))
        else:
            pygame.draw.circle(self.screen,
                               self.brush.get_color(), (x, y), size)
        for (i, rgb) in enumerate(self.colors):
            pygame.draw.rect(self.screen, rgb, self.colors_rect[i])


    def click_button(self, pos):
        for (i, rect) in enumerate(self.tools_rect):
            if rect.collidepoint(pos):
                # print("tools click:",i)
                if i==0:
                    # clear
                    self.brush.clear()
                    pass
                else:
                    # test
                    self.brush.send_to_server()
                    pass
                return True

        for (i, rect) in enumerate(self.pens_rect):
            if rect.collidepoint(pos):
                self.brush.set_brush_style(bool(i))
                return True
        for (i, rect) in enumerate(self.sizes_rect):
            if rect.collidepoint(pos):
                if i:
                    self.brush.set_size(self.brush.get_size() - 1)
                else:
                    self.brush.set_size(self.brush.get_size() + 1)
                return True
        for (i, rect) in enumerate(self.colors_rect):
            if rect.collidepoint(pos):
                self.brush.set_color(self.colors[i])
                return True
        return False


class Painter:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Painter")
        self.clock = pygame.time.Clock()
        self.brush = Brush(self.screen)
        self.menu = Menu(self.screen)
        self.menu.set_brush(self.brush)
        
    def set_url(self,url):
        self.menu.set_url(url)
    def run(self):
        self.screen.fill((255, 255, 255))
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.screen.fill((255, 255, 255))
                elif event.type == MOUSEBUTTONDOWN:
                    if event.pos[0] <= 74 and self.menu.click_button(event.pos):
                        # 点击菜单
                        # print("点击菜单")
                        pass
                    else:
                        self.brush.start_draw(event.pos)
                elif event.type == MOUSEMOTION:
                    self.brush.draw(event.pos)
                elif event.type == MOUSEBUTTONUP:
                    self.brush.end_draw()
            self.menu.draw()
            pygame.display.update()


def main():
    app = Painter()
    if len(sys.argv)>1:
        print("server ip=",sys.argv[1])
        ip=sys.argv[1]
        url="http://"+ip
        app.set_url(url)
    app.run()

if __name__ == '__main__':

    main()