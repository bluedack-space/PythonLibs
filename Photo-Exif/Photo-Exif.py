import logging
import exifread
from PIL import Image

def displayAllExif(path):
    im = Image.open(path)
    tags = {}
    with open(path, 'rb') as f:
        tags = exifread.process_file(f, details=False)
        for tag in tags.keys():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                print("Key:"+str(tag)+" value:"+str(tags[tag]))
                    
def get_exif_data(image_file):
    with open(image_file, 'rb') as f:
        exif_tags = exifread.process_file(f)
    return exif_tags

def get_if_exist(data, key):
    if key in data:
        return data[key]
    return None

def convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)
    return d + (m / 60.0) + (s / 3600.0)

def get_exif_location(exif_data):
    """
    Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)
    """
    lat = None
    lon = None
    
    gps_latitude      = get_if_exist(exif_data, 'GPS GPSLatitude'    )
    gps_latitude_ref  = get_if_exist(exif_data, 'GPS GPSLatitudeRef' )
    gps_longitude     = get_if_exist(exif_data, 'GPS GPSLongitude'   )
    gps_longitude_ref = get_if_exist(exif_data, 'GPS GPSLongitudeRef')
    
    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = convert_to_degress(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat = 0 - lat

        lon = convert_to_degress(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lon = 0 - lon

    return lat, lon                    

import sys

if __name__ == '__main__':
    args          = sys.argv
    fileNameImage = args[1]
    
    # [01] Display All Exif Data
    displayAllExif(fileNameImage)
    
    # [02] Get Latitude and Longitude from Exif of Photo
    lat, lon = get_exif_location(get_exif_data(fileNameImage))
    print("Latitude:" +str(lat))
    print("Longitude:"+str(lon))
    
    # [03] Get Area Name from Latitude and Longitude
    import reverse_geocoder as rg
    results = rg.search([(lat, lon)])
    area    = {t: results[0][t] for t in results[0]}
    print(area['cc'], area['admin1'], area['name'])
    
