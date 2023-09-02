from datetime import datetime
from .conftest import FIXTURE_DIR
import os
import pytest
from geopic_tag_reader import writer, reader, model
from PIL import Image
import io
from PIL import ExifTags
import pytz
import math


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "1.jpg"))
def test_writePictureMetadata_capture_time(datafiles):
    capture_time = datetime(year=2023, month=6, day=1, hour=12, minute=48, second=1, tzinfo=pytz.UTC)

    with open(str(datafiles / "1.jpg"), "rb") as image_file:
        image_file_upd = writer.writePictureMetadata(image_file.read(), writer.PictureMetadata(capture_time=capture_time))

    pil_img = Image.open(io.BytesIO(image_file_upd))
    tags = reader.readPictureMetadata(pil_img)

    assert datetime.fromtimestamp(tags.ts, tz=pytz.UTC) == capture_time

    # we also check specific tags:
    pil_exif = pil_img._getexif()
    assert pil_exif[ExifTags.Base.DateTimeOriginal] == "2023-06-01 12:48:01"
    assert pil_exif[ExifTags.Base.GPSInfo][ExifTags.GPS.GPSDateStamp] == "2023-06-01"
    assert pil_exif[ExifTags.Base.GPSInfo][ExifTags.GPS.GPSTimeStamp] == (12.0, 48.0, 1.0)


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "1.jpg"))
def test_writePictureMetadata_capture_time_no_timezone(datafiles):
    capture_time = datetime(year=2023, month=6, day=1, hour=12, minute=48, second=1, tzinfo=None)

    with open(str(datafiles / "1.jpg"), "rb") as image_file:
        image_file_upd = writer.writePictureMetadata(image_file.read(), writer.PictureMetadata(capture_time=capture_time))

    pil_img = Image.open(io.BytesIO(image_file_upd))
    tags = reader.readPictureMetadata(pil_img)

    paris = pytz.timezone("Europe/Paris")
    assert datetime.fromtimestamp(tags.ts, tz=pytz.UTC) == paris.localize(capture_time).astimezone(pytz.UTC)

    pil_exif = pil_img._getexif()
    # DateTimeOriginal should be a local time, so 12:48:01 localized in Europe/Paris timezome (since it's where the picture has been taken)
    assert pil_exif[ExifTags.Base.DateTimeOriginal] == "2023-06-01 12:48:01"
    assert pil_exif[ExifTags.Base.GPSInfo][ExifTags.GPS.GPSDateStamp] == "2023-06-01"
    # GPSTimeStamp should always be in UTC
    assert pil_exif[ExifTags.Base.GPSInfo][ExifTags.GPS.GPSTimeStamp] == (10.0, 48.0, 1.0)
    assert pil_exif[ExifTags.Base.OffsetTimeOriginal] == "+02:00"


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "1.jpg"))
def test_writePictureMetadata_longitude(datafiles):
    longitude = 2.4243

    with open(str(datafiles / "1.jpg"), "rb") as image_file:
        image_file_upd = writer.writePictureMetadata(image_file.read(), writer.PictureMetadata(longitude=longitude))

    pil_img = Image.open(io.BytesIO(image_file_upd))
    tags = reader.readPictureMetadata(pil_img)

    assert math.isclose(tags.lon, longitude)

    pil_exif = pil_img._getexif()
    assert pil_exif[ExifTags.Base.GPSInfo][ExifTags.GPS.GPSLongitude] == (2.0, 25.0, 27.48)
    assert pil_exif[ExifTags.Base.GPSInfo][ExifTags.GPS.GPSLongitudeRef] == "E"


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "1.jpg"))
def test_writePictureMetadata_lat(datafiles):
    latitude = -38.889469

    with open(str(datafiles / "1.jpg"), "rb") as image_file:
        image_file_upd = writer.writePictureMetadata(image_file.read(), writer.PictureMetadata(latitude=latitude))

    pil_img = Image.open(io.BytesIO(image_file_upd))
    tags = reader.readPictureMetadata(pil_img)

    assert math.isclose(tags.lat, latitude)

    pil_exif = pil_img._getexif()
    assert pil_exif[ExifTags.Base.GPSInfo][ExifTags.GPS.GPSLatitude] == (38.0, 53.0, 22.0884)
    assert pil_exif[ExifTags.Base.GPSInfo][ExifTags.GPS.GPSLatitudeRef] == "S"


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "1.jpg"))
def test_writePictureMetadata_picture_type_flat(datafiles):
    pic_type = model.PictureType.flat

    with open(str(datafiles / "1.jpg"), "rb") as image_file:
        image_file_upd = writer.writePictureMetadata(image_file.read(), writer.PictureMetadata(picture_type=pic_type))

    pil_img = Image.open(io.BytesIO(image_file_upd))
    tags = reader.readPictureMetadata(pil_img)

    assert tags.type == "flat"


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "1.jpg"))
def test_writePictureMetadata_picture_type_equi(datafiles):
    pic_type = model.PictureType.equirectangular

    with open(str(datafiles / "1.jpg"), "rb") as image_file:
        image_file_upd = writer.writePictureMetadata(image_file.read(), writer.PictureMetadata(picture_type=pic_type))

    pil_img = Image.open(io.BytesIO(image_file_upd))
    tags = reader.readPictureMetadata(pil_img)

    assert tags.type == "equirectangular"
