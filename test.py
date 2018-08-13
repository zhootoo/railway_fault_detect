import cv2
import numpy as np

def show_img(img):
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def handle_light(img,th):
    #处理图片的反光,大于th的像素被填充为77
    ret,mask = cv2.threshold(img,th,255,cv2.THRESH_BINARY)
    inv_mask = cv2.bitwise_not(mask)
    img_h = cv2.bitwise_and(img,img,mask=inv_mask)
    img_temp1 = cv2.add(inv_mask,77)
    img_temp2 = cv2.bitwise_and(img_temp1,img_temp1,mask=mask)
    dst = cv2.add(img_temp2,img_h)
    cv2.imwrite('../data/4.jpg',dst)
    show_img(dst)

def handle(img):
    #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#转换为灰度图
    ret,mask = cv2.threshold(img,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)

def test(img):
    kernel=np.ones((8,8),np.uint8)#构造5x5卷积核
    erosion=cv2.erode(img,kernel,iterations=3) #进行5次腐蚀
    show_img(erosion)
    dilation=cv2.dilate(erosion,kernel,iterations=3)#进行5次膨胀
    show_img(dilation)
    water = img - dilation
    show_img(water)
    #二值化操作
    th1,ret1=cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    show_img(ret1)
    ret1,contours,hierarchy=cv2.findContours(ret1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#轮廓分析
    img_m = cv2.imread('../data/w.jpg')
    for cnt in contours:
        tmp = cv2.contourArea(cnt)
        tempC=cv2.arcLength(cnt,True)
        cv2.drawContours(img_m,[cnt],-1,(255,0,0,),thickness=2)
        print(tmp)#输出液滴面积
    show_img(img_m)

if __name__=='__main__':
    img = cv2.imread('../data/w.jpg',0)
    test(img)
    # th1,ret1=cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # show_img(img)
    # show_img(ret1)
