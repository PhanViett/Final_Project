from flask_seeder import Seeder, Faker, generator

from application.models import NhanVien, TinTuc, DonVi

from application.extensions import pwd_context


class DemoSeeder(Seeder):

    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 10

    def run(self):
        # Create a new Faker and tell it how to create NhanVien objects
        faker = Faker(
            cls=NhanVien,
            init={
                "tai_khoan": generator.String("\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c"),
                "email": generator.String("\\c\\c\\c\\c\\c\\c\\c@gmail.com"),
                "mat_khau": "123456",
                "ho": generator.Name(),
                "ten": generator.Name(),
                "dia_chi": generator.String("\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c"),
                "so_dien_thoai": generator.String("\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d")
            }
        )
        # Create 1000 users
        # for nhan_vien in faker.create(1000):
        #     # print("Adding nhan_vien: %s" % nhan_vien)
        #     self.db.session.add(nhan_vien)

        adminfaker = Faker(
            cls=NhanVien,
            init={
                "tai_khoan": "test",
                "email": generator.String("test@gmail.com"),
                "mat_khau": "e10adc3949ba59abbe56e057f20f883e",
                "ho": "admin",
                "ten": "admin",
                "dia_chi": generator.String("\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c"),
                "so_dien_thoai": generator.String("\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d"),
                "is_super_admin": True
            }
        )

        for nhan_vien in adminfaker.create(1):
            # print("Adding nhan_vien: %s" % nhan_vien)
            self.db.session.add(nhan_vien)

        # donviFake = Faker(
        #     cls=DonVi,
        #     init={
        #         "ma_don_vi": generator.String("\\c\\c\\c\\c\\c\\c\\c"),
        #         "tuyen_don_vi": generator.String("\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c"),
        #         "don_vi_cap_tren": generator.String("\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c"),
        #         "so_dien_thoai": generator.String("\\d\\d\\d\\d\\d\\d\\d"),
        #         "email": generator.Email,
        #         "nguoi_dai_dien": generator.String("\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c"),
        #         "hotline_1": generator.String("\\d\\d\\d\\d\\d\\d\\d"),
        #         "hotline_2": generator.String("\\d\\d\\d\\d\\d\\d\\d"),
        #         "tinh_thanh_id": "1601ab0f-afdd-4cc3-9ebd-bf72d057e955",
        #         "quan_huyen_id": "b3e3e6d8-cab8-4f9b-9048-4d25c79de0bb",
        #         "phuong_xa_id": "30512edb-4cc9-4eee-ae1a-9f242b9c85ae",
        #         "dia_chi": generator.String("\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c\\c")
        #     }
        # )

        # for don_vi in donviFake.create(1):
        #     self.db.session.add(don_vi)
