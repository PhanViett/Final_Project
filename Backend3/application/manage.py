import click
from flask.cli import with_appcontext
from application.extensions import pwd_context
from application.models import TaiKhoan


@click.command("init")
@with_appcontext
def init():
    """Create a new admin nhan_vien"""
    from application.extensions import db
    from application.models import NhanVien

    click.echo("create nhan_vien")
    user = TaiKhoan(tai_khoan="test", mat_khau=pwd_context.hash("e10adc3949ba59abbe56e057f20f883e"))
    db.session.add(user)
    db.session.commit()
    click.echo("created nhan_vien admin")
