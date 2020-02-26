from django.shortcuts import render
import os
from django.conf import settings
from . import inference
from PIL import Image
import uuid


def index(request):
    return render(request, 'cyclegan/index.html', context={
    })


def resize_image(img_path, new_height, new_width):
    try:
        mPath, ext = os.path.splitext(img_path)
        if ext == ".png" or ext == ".jpg" or ext == ".jpeg":
            img = Image.open(img_path)
            (width, height) = img.size

            if width != new_width:
                # new_height = int(height * new_width / width)
                new_height = new_width
                out = img.resize((new_width, new_height), Image.ANTIALIAS)
                new_file_name = '%s%s' % (mPath, ext)
                out.save(new_file_name, quality=100)
                print("图片尺寸修改为：" + str(new_width))
            else:
                print("图片尺寸正确，未修改")
        else:
            print("非图片格式")
    except Exception as e:
        print(e)


def upload(request):
    if request.method == 'POST':
        # 1.获取用户上传的文件
        files = request.FILES.getlist('files')
        # 2.判断文件列表是否存在文件
        if len(files) > 0:
            # 3. 判断上传路径是否存在,不存在则创建文件夹
            if not os.path.exists(settings.MEDIA_ROOT):
                os.makedirs(settings.MEDIA_ROOT)

            # 4. 遍历用户上传的文件列表
            images = []
            for file in files:
                # 5. 获取文件后缀名
                ext = os.path.splitext(file.name)[1]
                # 6. 通过uuid?重命名上传的文件
                name = uuid.uuid4()
                file_name = '{}{}'.format(uuid.uuid4(), ext)
                out_name = '{}{}'.format(uuid.uuid4(), ext)
                # 7. 构建文件绝对路径
                file_path = '{}{}'.format(settings.MEDIA_ROOT, file_name)
                out_path = '{}{}'.format(settings.MEDIA_ROOT, out_name)
                print(file_path)
                # 8. 将上传的文件相对路径存储到images中
                # 注意这样要构建相对路径MEDIA_URL+file_name,这里可以保存到数据库
                images.append('{}{}'.format(settings.MEDIA_URL, file_name))
                images.append('{}{}'.format(settings.MEDIA_URL, out_name))
                # 9. 保存文件
                with open(file_path, 'wb') as f:
                    for i in file.chunks():
                        f.write(i)
                        print("ok")
                resize_image(file_path, 256, 256)
                break

            if 'apple2orange' in request.POST:
                pbpath = '{}{}'.format(settings.MEDIA_ROOT, 'apple2orange.pb')
            if 'orange2apple' in request.POST:
                pbpath = '{}{}'.format(settings.MEDIA_ROOT, 'orange2apple.pb')
            if 'horse2zebra' in request.POST:
                pbpath = '{}{}'.format(settings.MEDIA_ROOT, 'horse2zebra.pb')
            if 'zebra2horse' in request.POST:
                pbpath = '{}{}'.format(settings.MEDIA_ROOT, 'zebra2horse.pb')
            if 'summer2winter' in request.POST:
                pbpath = '{}{}'.format(settings.MEDIA_ROOT, 'summer2winter.pb')
            if 'winter2summer' in request.POST:
                pbpath = '{}{}'.format(settings.MEDIA_ROOT, 'winter2summer.pb')
            inference.inference(file_path, out_path, pbpath)
            return render(request, 'cyclegan/index.html', {'images': images})
        else:
            print("没有文件")

    return render(request, 'cyclegan/index.html')
