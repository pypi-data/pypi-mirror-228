# -*- coding:utf-8 -*-
# 创建时间：2022-03-03 18:03:48
# 创建人：  Dekiven
# TODO: 自动计算图集大小，使用更好的pack算法，参考https://github.com/tulth/rect_pack (Python) https://github.com/juj/RectangleBinPack (C++)

import os
from PIL import Image
from DKVTools.Funcs import *

class ApConst( object ) :
    rotate = 'rotate'
    padding = 'padding'
    trim = 'trim'
    alignVertical = 'alignVertical'
    name = 'name'
    size = 'size'
    box = 'box'
    oriSize = 'oriSize'
    offset = 'offset'
    oriBox = 'oriBox'
    img = 'img'
    imgFormat = 'imgFormat'
    angle = 'angle'
    atlasSize = 'atlasSize'

class _ImgNode( object ) :
    ''''''
    params = {}
    def __init__( self, area, **params ) :
        super(_ImgNode, self).__init__()
        if len(area) == 2 :
            area = [0, 0, area[0], area[1]]
        self.area = area
        self.rotate = False
        self._left = None
        self._right = None
        self._hasImg = False

    @property
    def width( self ) :
        '''区域宽度，有图片时表示图片宽度'''
        return self.area[2] - self.area[0]

    @width.setter
    def width( self, value ) :
        if self.width >= value :
            self.area[2] = self.area[0] + value
        else :
            print(u'error: 设置宽度失败,区域宽度:%d，实际宽度:%d'%(self.width, value))

    @property
    def height( self ) :
        '''区域宽度，有图片时表示图片宽度'''
        return self.area[3] - self.area[1]

    @height.setter
    def height( self, value ) :
        if self.height >= value :
            self.area[3] = self.area[1] + value
        else :
            print(u'error: 设置高度失败,区域高度:%d，实际高度:%d'%(self.width, value))

    @property
    def l( self ) :
        '''最左边'''
        return self.area[0]

    @property
    def t( self ) :
        '''最上边'''
        return self.area[1]

    @property
    def r( self ) :
        '''最右边'''
        return self.area[2]

    @property
    def b( self ) :
        '''最下边'''
        return self.area[3]

    @property
    def empty( self ) :
        '''该区域是可以经放置图片'''
        return not self._hasImg

    @property
    def left( self ) :
        return self._left

    @property
    def right( self ) :
        return self._right

    def tryInsert( self, size ) :
        '''尝试插入size大小的图片'''
        rotate = _tryGetParam(_ImgNode.params, ApConst.rotate, False)
        padding = _tryGetParam(_ImgNode.params, ApConst.padding, 2)
        if self.empty :
            w, h = size
            ret = False
            if w <= self.width and h <= self.height :
                ret = True
            elif rotate and h <= self.width and w <= self.height :
                h, w = size
                self.rotate = True
                ret = True
            if ret :
                left = _ImgNode( [self.l + padding + w,  self.t, self.r, self.t + h] )
                if left.width >= 1 and left.height >= 1 :
                    self._left = left

                right = _ImgNode( [self.l,  self.t + padding + h, self.r, self.b] )
                if right.width >= 1 and right.height >= 1 :
                    self._right = right

                self.width = w
                self.height = h
                self._hasImg = True

            return ret

        return False

def trimPng( img, padding=(0, 0, 0, 0 ) ) :
    '''裁剪img透明区域。
padding是表示ltrb各边裁剪的四元组，元素为整型和None，为None表示不裁剪该边，大于0表示留出相应的宽度，小于0表示向内多裁剪的宽度
返回： img(裁剪后的img), box(裁剪区域的box (x, y, x+w, y+h))'''
    bbox = img.getbbox()
    w, h = img.size
    if bbox[2] == w-1 and bbox[3] == h-1 :
        return img, bbox
    # 计算padding后的box
    box = [0, 0, w, h]
    for i in range(4) :
        p = padding[i]
        if p is not None :
            maxV = (i % 2 == 0) and w or h
            a = (i > 1) and 1 or -1
            v = bbox[i]+p*a
            box[i] = max(min(maxV, v), 0)
    # crop函数参数为: (l, t, r, b) 即:(x, y, x+w, y+h)
    img = img.crop(box)
    return img, box

def packAtlas( infos, **params ) :
    '''将info定义的图片打包到图集
参数:
    info: 碎图信息列表，每个元素包括(图片完整路径, 保存到图集中的名称)
    params: 其他参数
        trim = False, 是否裁剪图片
        alignVertical = False, 竖直方向排不碎图
        angle = Image.ROTATE_270, 碎图的旋转角度
        imgFormat = 'RGBA', 图片格式
        atlasSize = (2048, 2048), 图集大小
返回值:
    打包的图集图片, 打包的图片信息列表
'''
    trim = _tryGetParam(params, ApConst.trim, False)
    alignVertical = _tryGetParam(params, ApConst.alignVertical, False)
    angle = _tryGetParam(params, ApConst.angle, Image.ROTATE_270)
    imgFormat = _tryGetParam(params, ApConst.imgFormat, 'RGBA')
    atlasSize = _tryGetParam(params, ApConst.atlasSize, (2048, 2048))

    _ImgNode.params = params
    frames = []
    for path, name in infos :
        img = Image.open(path).convert(imgFormat)
        oriSize = img.size
        size = img.size
        box = (0, 0) + size
        if trim :
            img, box = trimPng(img)
            size = img.size
        frames.append({
            ApConst.name : name,
            ApConst.size : size,
            ApConst.oriSize : oriSize,
            ApConst.oriBox : box,
            ApConst.img : img,
        })

    # 按图片面积的负值和图片名称排序
    frames.sort(key=lambda f : (-f.get(ApConst.size)[0] * f.get(ApConst.size)[1], f.get(ApConst.name)))
    image = Image.new(imgFormat, atlasSize)
    validImgs = []
    root = _ImgNode(atlasSize)
    walk = _walkVertical if alignVertical else _walkHorizontal
    for f in frames :
        node = walk(root, f.get(ApConst.size))
        if node is not None :
            f[ApConst.rotate] = node.rotate
            f[ApConst.box] = node.area
            img = f.get(ApConst.img)
            if node.rotate :
                img = img.transpose(angle)
            image.paste(img, node.area)
            validImgs.append(f)
        else :
            print(u'超出范围', f.get(ApConst.name))

    return image, validImgs

def packDir( path, outDir, fileName, **params ) :
    '''遍历path下所有png,打包到图集
参数：
    path: 图片所在路径
    outDir: 输出的plist和png所在路径
    fileName: 输出的plist和png的名称(不带后缀名)
    params: 其他参数
        trim = False, 是否裁剪图片
        alignVertical = False, 竖直方向排不碎图
        angle = Image.ROTATE_270, 碎图的旋转角度
        imgFormat = 'RGBA', 图片格式
        atlasSize = (2048, 2048), 图集大小
        padding = 2, 图集中碎图间隔
        rotate = False, 是否允许旋转
'''
    infos = []
    if os.path.isdir(path) :
        for d, fds, fs in os.walk(path) :
            for f in fs :
                if os.path.splitext(f)[-1].lower() == '.png' :
                    p = pathJoin(d, f)
                    n, _ = getRelativePath(p, path)
                    infos.append((p, n))

    img, frames = packAtlas(infos, **params)
    tryMakeDir(outDir)
    img.save(pathJoin(outDir, fileName+'.png'))

    atlasSize = params.get(ApConst.atlasSize)
    with openFile(pathJoin(outDir, fileName+'.plist'), 'w') as f :
        f.write(genPlist3(fileName+'.png', frames, atlasSize))

def genPlist3( fileName, frames, atlasSize ) :
    '''获取plist fromat==3的文件内容'''
    fStr = '''            <key>%s</key>
            <dict>
                <key>aliases</key>
                <array/>
                <key>spriteOffset</key>
                <string>{%s,%s}</string>
                <key>spriteSize</key>
                <string>{%d,%d}</string>
                <key>spriteSourceSize</key>
                <string>{%d,%d}</string>
                <key>textureRect</key>
                <string>{{%d,%d},{%d,%d}}</string>
                <key>textureRotated</key>
                <%s/>
            </dict>'''
    pStr = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
        <key>frames</key>
        <dict>
%s
        </dict>
        <key>metadata</key>
        <dict>
            <key>format</key>
            <integer>3</integer>
            <key>size</key>
            <string>{%d,%d}</string>
            <key>textureFileName</key>
            <string>%s</string>
            <key>premultiplyAlpha</key>
            <false/>
        </dict>
    </dict>
</plist>
'''
    # 排序，使plits中信息按图片名称排序
    frames.sort(key=lambda f : f.get(ApConst.name))
    fs = []
    for f in frames :
        info = [f.get(ApConst.name),]
        size = list(f.get(ApConst.size))
        box = list(f.get(ApConst.box)[:2]) + size
        oriSize = list(f.get(ApConst.oriSize))
        oriBox = list(f.get(ApConst.oriBox)[:2]) + oriSize
        rotate = f.get(ApConst.rotate)
        # offset 值为原图中心的位置到裁剪后的图中心(oriBox顶点 + oriSize/2)的距离，由于原点在左上角，求出的y坐标需要取其相反数
        offset = [
            oriBox[0] + (size[0] - oriSize[0]) / 2,
            -(oriBox[1] + (size[1] - oriSize[1]) / 2),
        ]
        # 这里的offset如果是小数，还是保留
        offset = [str(v if v != int(v) else int(v)) for v in offset]
        info = info + offset + size + oriSize + box
        info.append('true' if rotate else 'false')
        fs.append(fStr%tuple(info))
    return pStr%('\n'.join(fs), atlasSize[0], atlasSize[1], fileName )

def _walkHorizontal( node: _ImgNode, size ) :
    '''水平遍历'''
    if node is None :
        return
    if node.empty :
        if node.tryInsert(size) :
            return node
    else :
        ret = _walkHorizontal(node.left, size)
        if ret is not None :
            return ret
        else :
            return _walkHorizontal(node.right, size)

def _walkVertical( node: _ImgNode, size ) :
    '''竖直遍历'''
    if node is None :
        return
    if node.empty :
        if node.tryInsert(size) :
            return node
    else :
        ret = _walkHorizontal(node.right, size)
        if ret is not None :
            return ret
        else :
            return _walkHorizontal(node.left, size)

def _tryGetParam( params, key, defValue=None ) :
    '''尝试获取参数，不存在则设置默认参数'''
    v = params.get(key)
    if v is None :
        params[key] = defValue
        v = defValue
    return v

def _test( ) :
    from TkToolsD.CommonWidgets import ShowChooseDirDialog
    p = ShowChooseDirDialog()
    if p is not None :
        packDir(
            p,
            pathJoin(getDesktopPath(), 'atlasTest2'),
            'test',
            trim=True,
            padding=2,
            atlasSize=(512, 512),
            rotate=True
        )

def _testTrim( ) :
    from TkToolsD.CommonWidgets import ShowChooseFileDialog
    p = ShowChooseFileDialog()
    if p :
        img = Image.open(p)
        img, box = trimPng(img, (1,1,1,3))
        p = pathJoin(getDesktopPath(), 'atlasTest2/testTrim.png')
        tryMakeParentDir(p)
        img.save(p)

def _main( ) :
    _test()
    # _testTrim()

if __name__ == '__main__' :
    _main()
