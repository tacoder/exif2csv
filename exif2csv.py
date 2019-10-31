import glob
import PIL
from PIL import Image
from PIL.ExifTags import TAGS
import csv

def convert_to_degress(value):

    if value is None:
        return None
    print value
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format. Forked from github.com/erans/983821"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

photos = glob.glob('*.jpg')
file = open('exifdata.csv', 'wb')
table = csv.writer(file)
table.writerow(['Photo', 'DateTime', 'Make', 'Model', 'Cutline', 'Photographer', 'Latitude', 'Longitude'])
#photos = ['IMG_20190109_223438.jpg']
for photo in photos:
    img = Image.open(photo)
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in PIL.ExifTags.TAGS
    }
    print "EXIF:", exif
    datetime = exif.get('DateTime', None)
    make = exif.get('Make', None)
    model = exif.get('Model', None)
    cutline = exif.get('ImageDescription', None)
    gpsInfo = exif.get('GPSInfo', None)
    latitude = None
    Longitude = None
    isWest = False
    photog = None
    try:
        photog = cutline[cutline.find("(")+1:cutline.find("/")]
    except:
        print "No photographer in cutline."

    try:
        print "gpsinfo is ", gpsInfo
        latitude = gpsInfo[2]
        Longitude = gpsInfo[4]
        isWest  = gpsInfo[3] == 'W'
        print latitude
        print Longitude
        latitude = convert_to_degress(latitude)
        Longitude = convert_to_degress(Longitude)
        if isWest:
            lon = lon * -1
    except:
        print "Inavlid exif data!"

    table.writerow([photo, datetime, make, model, cutline, photog, latitude, Longitude])
    print 'Extracting data for photo %s' % photo

file.close()

