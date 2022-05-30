from django.core.files.storage import FileSystemStorage


def ConvertFileToUrl(filedata, id, modeldir):
    if str(filedata).endswith(('.png', '.jpg', '.jpeg', '.pdf', '.odcx')):
        fs = FileSystemStorage()
        img = filedata
        imgname = modeldir + "/" + id + "/" + img.name
        name = fs.save(imgname, img)
        imgUrl = fs.url(name)
        return imgUrl
    else:
        raise ValueError("not valid data")
