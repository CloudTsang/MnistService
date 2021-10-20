
from PIL import  Image,ImageDraw
import math


def draw_split(jsdata):
    textdata=[]
    rectdata=[]
    onedata=[]
    rs=[]
    rs_len=0
    draw_set=[]
    for _,v in enumerate(jsdata):
        left=-1
        top=-1
        right=1
        bottom=1
        # print("v=",v)
        for i2,v2 in enumerate(v):
            x=v2[0]
            y=v2[1]
            if left==-1:
                left=x
                top=y
                right=x
                bottom=y
            if x<left:
                left=x
            if x>right:
                right=x
            if y<top:
                top=y
            if y>bottom:
                bottom=y
        draw_set.append((v,left,top,right,bottom))
    sort_set= sorted(draw_set ,key=lambda student: student[1] )
    
    last_rect=[0,0,0,0]
    last_v=sort_set[0]
    for i,v in enumerate(sort_set):
        if i==0:
            last_v=v
            onedata.append(v[0])
            last_rect=[v[1],v[2],v[3],v[4]]
            continue
        
        if last_rect[2]<v[1]:
            # right > left
            textdata.append(onedata)
            rectdata.append(last_rect)
            onedata=[v[0]]
            last_rect=[v[1],v[2],v[3],v[4]]
        else:
            #update
            if v[1]<last_rect[0]:
                #left
                last_rect[0]=v[1]
            if v[2]<last_rect[1]:
                #top
                last_rect[1]=v[2]
            if v[3]>last_rect[2]:
                #right
                last_rect[2]=v[3]
            if v[4]>last_rect[3]:
                #bottom
                last_rect[3]=v[4]
            onedata.append(v[0])
        last_v=v


    if len(onedata)>0:
        textdata.append(onedata)
        rectdata.append(last_rect)
    # print("last:",textdata)
    return textdata,rectdata

def draw_trim(jsdata):
    left=-1
    top=-1
    right=1
    bottom=1
    for _,v in enumerate(jsdata):
        for i2,v2 in enumerate(v):
            x=v2[0]
            y=v2[1]
            if left==-1:
                left=x
                top=y
                right=x
                bottom=y
            if x<left:
                left=x
            if x>right:
                right=x
            if y<top:
                top=y
            if y>bottom:
                bottom=y
    h2=bottom-top
    w2=right-left
    # print("trim:",w2,h2)
    side_len=w2
    if h2>w2:
        side_len=h2
    # print("side_len:",side_len)
    margin=math.ceil(side_len*0.05)

    left2=left-math.ceil((side_len-w2)/2)-margin
    top2=top-math.ceil((side_len-h2)/2)-margin
    w2=side_len+margin*2
    h2=side_len+margin*2
    for i1,v in enumerate(jsdata):
        for i2,v2 in enumerate(v):
            jsdata[i1][i2]=(v2[0]-left2,v2[1]-top2)
    return w2,h2,jsdata

def drawimg(w,h,draw_x,draw_y,jsdata,size):


    if size<=0:
        size=1
    if size>80:
        size=80
    scale=1.0

    max_w=300
    max_h=300

    Offset = int((size-1)/2)

    if w>max_w:
        scale=max_w/w
        w=max_w
        h=int(h*scale)
    if h>max_h:
        scale2=max_h/h
        h=max_h
        w=int(scale2*w)
        scale=scale*scale2

    # print("scale:",scale,w,h)
    image = Image.new("L",[w,h],'white') #Image.open(image_path)
    #创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(image)
    for _,v in enumerate(jsdata):
         
        for i2,v2 in enumerate(v):
            # print("v2=",v2)
            x1=int(scale*float(v2[0]+draw_x))
            x2=int(scale*float(v2[1]+draw_y))
            v[i2]=(x1,x2)
            # print(v[i2])
            draw.ellipse((x1-Offset,x2-Offset,x1+Offset,x2+Offset), fill='black')
        # print("draw v=",v)
        draw.line(v, fill="black", width=size)
        # draw.polygon(v, outline=(0,0,0),fill=1)
    image.show()
    return image



if __name__ == "__main__":
    # drawimg(1000,1200,[[(100,100),(200,20),(300,60),(500,999)],[(600,20),(200,800),(999,500)]],8)

    # w,h,jsdata=draw_trim(1000,1200,[[(50,50),(300,60),(300,80),(50,180),(40,220),(300,220)]])
    # drawimg(w,h,jsdata,4)
    # datas=draw_split([[(50,50),(300,60),(300,380),(50,380),(40,420),(300,420)],[(500,50),(700,50),(600,600),(500,600),(500,50)]])

    # datas=draw_split([[[72,221],[70,223],[69,227],[68,235],[66,245],[65,260],[61,273],[59,289],[56,313],[56,330],[53,346],[53,357],[53,363],[50,366],[50,369],[50,371],[50,373],[50,374],[49,376]],[[118,347],[120,347],[122,347],[125,347],[126,347],[129,348],[129,349],[132,350],[132,351],[133,351],[133,352],[133,354],[134,357],[135,357],[136,357]],[[212,252],[212,251],[216,251],[221,251],[226,251],[234,251],[238,251],[244,251],[248,251],[252,251],[255,251],[257,251],[258,252],[258,256],[260,259],[260,263],[260,267],[260,270],[260,274],[260,280],[260,285],[258,292],[258,297],[251,313],[241,330],[238,335],[235,339],[233,342],[230,344],[228,347],[227,348],[226,347],[224,349],[223,350],[223,351],[224,351],[225,351],[227,351],[230,351],[235,352],[242,353],[246,353],[256,353],[265,353],[268,353],[275,353],[287,353],[293,353],[298,353],[301,353]]])
    # datas=draw_split([[[118,347],[120,347],[122,347],[125,347],[126,347],[129,348],[129,349],[132,350],[132,351],[133,351],[133,352],[133,354],[134,357],[135,357],[136,357]],[[212,252],[212,251],[216,251],[221,251],[226,251],[234,251],[238,251],[244,251],[248,251],[252,251],[255,251],[257,251],[258,252],[258,256],[260,259],[260,263],[260,267],[260,270],[260,274],[260,280],[260,285],[258,292],[258,297],[251,313],[241,330],[238,335],[235,339],[233,342],[230,344],[228,347],[227,348],[226,347],[224,349],[223,350],[223,351],[224,351],[225,351],[227,351],[230,351],[235,352],[242,353],[246,353],[256,353],[265,353],[268,353],[275,353],[287,353],[293,353],[298,353],[301,353]],[[72,221],[70,223],[69,227],[68,235],[66,245],[65,260],[61,273],[59,289],[56,313],[56,330],[53,346],[53,357],[53,363],[50,366],[50,369],[50,371],[50,373],[50,374],[49,376]]])
    # datas=draw_split([[[405,196],[406,196],[406,212],[383,278],[371,302],[368,314],[368,318],[368,320],[368,321],[370,322],[373,322],[376,323],[381,323],[388,323],[401,323],[432,322],[456,319],[484,313],[508,310],[528,308],[538,307],[542,306]],[[476,224],[476,226],[473,241],[469,262],[464,298],[463,310],[456,348],[454,361],[448,395],[446,415],[446,430],[446,442],[446,449],[446,455],[446,457],[446,459]]])
    # datas=draw_split([[[311,151],[311,153],[309,174],[306,191],[302,209],[300,218],[293,242],[289,257],[284,273],[280,290],[277,305],[272,320],[271,330],[268,339],[267,340],[266,345],[266,346],[266,347],[266,348],[270,348],[282,348],[350,336],[410,328],[475,321],[549,318],[614,318],[642,318],[682,317],[691,314]],[[528,146],[528,147],[521,204],[516,257],[513,286],[507,359],[504,407],[499,445],[499,460],[495,495],[495,520],[495,523],[497,531],[497,536],[497,537]]])
    datas,rects=draw_split([[[253,60],[253,66],[253,154],[253,217],[253,269],[253,307],[253,324],[253,382]],[[311,285],[314,285],[326,289],[336,295],[341,297],[363,312],[367,316]],[[458,119],[459,118],[466,118],[473,118],[481,118],[491,123],[499,127],[508,133],[511,137],[516,147],[518,155],[488,281],[464,330],[440,368],[406,414],[402,420],[401,421],[413,425],[428,425],[474,425],[488,425],[501,425],[505,425],[506,425],[507,425]],[[614,259],[619,258],[628,258],[654,258],[676,258],[697,258],[717,258],[731,258],[734,257]]])
    last_h=0
    last_w=0
    h_i=0
    for v in datas:
        w,h,jsdata=draw_trim(v)
        start_x=0
        start_y=0
        draw_w=w
        draw_h=h

        if h_i>0:
            cur_top=rects[h_i][1]
            last_top=rects[h_i-1][1]
            if h<last_h*0.5 and cur_top>(last_top+last_h*0.5):
                start_x=math.ceil((last_w-w)/2)
                start_y=math.ceil((last_h-h))
                draw_w=last_w
                draw_h=last_h
        drawimg(draw_w,draw_h,start_x,start_y,jsdata,4)
        last_h=h
        last_w=w
        h_i+=1
        