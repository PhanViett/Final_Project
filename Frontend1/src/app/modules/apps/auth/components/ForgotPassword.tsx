import { Link } from "react-router-dom";
import { Form } from "react-bootstrap";

export function ForgotPassword() {
  return (
    <div className="pageForgotPassword">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-8 col-lg-6 col-xl-6">
            <div className="box-login-wrapper card border-0 position-relative">
              <Link to={"/dang-nhap"}>
                <i className="fas fa-times-circle position-absolute icon-close"></i>
              </Link>
              <div className="card-body w-100 w-md-75 pt-4 px-5 pb-5 m-auto ">
                <div className="title-text text-center">Quên mật khẩu</div>

                <div className="form-group mt-10 mb-6 input-icon">
                  <Form.Control
                    type="text"
                    placeholder="Nhập số điện thoại"
                    className="input-register input-login"
                    style={{ fontSize: 14, fontWeight: 400 }}
                  />
                </div>
                <div className="form-group text-center mb-3 w-100">
                  Mã xác nhận sẽ được gửi qua số điện thoại ở trên
                </div>

                <div className="form-group mb-1 text-center w-100">
                  <button
                    className="btn btn-primary btn-block btn-login"
                    type="button"
                    id="button-forgot-password"
                  >
                    <i className="fas fa-chevron-circle-right"></i> Gửi{" "}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="footer footer-alt text-footer">
        SỞ Y TẾ TP HỒ CHÍ MINH
      </div>
    </div>
  );
}
