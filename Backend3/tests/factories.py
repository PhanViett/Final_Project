import factory
from myapi.models import User


class UserFactory(factory.Factory):

    username = factory.Sequence(lambda n: "nhan_vien%d" % n)
    email = factory.Sequence(lambda n: "nhan_vien%d@mail.com" % n)
    password = "mypwd"

    class Meta:
        model = User
