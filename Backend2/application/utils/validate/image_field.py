from marshmallow import fields, ValidationError

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


class ImageField(fields.Field):
    def _validate(self, value):
        if allowed_file(value.filename) == False:
            raise ValidationError('allow file type are .png , .jpg , .jpeg')
