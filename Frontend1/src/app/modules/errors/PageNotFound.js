import { Link, Outlet } from "react-router-dom";
import { toAbsoluteUrl } from "../../../_metronic/helpers";

export default function PageNotFound() {
  return (
    <div className="d-flex flex-column flex-root">
      <div className="d-flex flex-column flex-column-fluid bgi-position-y-bottom position-x-center bgi-no-repeat bgi-size-contain bgi-attachment-fixed">
        <div className="d-flex flex-column flex-column-fluid text-center p-5 py-lg-20">
          <div className="mb-5 pt-lg-20">
            <img
              alt="Logo"
              src={toAbsoluteUrl("/media/logos/Logo_BoYTe.png")}
              className="h-160px"
            />
          </div>
          <div className="p-3">
            <p
              style={{
                fontSize: "2.5rem",
                fontWeight: "bold",
              }}
            >
              Trang này không hiển thị
            </p>
          </div>
          <div className="pt-3">
            <h3 style={{ fontWeight: "500" }}>
              Có thể liên kết đã hỏng hoặc trang đã bị gỡ.
            </h3>
          </div>
          <div>
            <h3 style={{ fontWeight: "500" }}>
              Hãy kiểm tra xem liên kết mà bạn đang cố mở có chính xác không.
            </h3>
          </div>
          <div className="pt-lg-10 mb-10">
            <Outlet />
            <div className="text-center">
              <Link to="/" className="btn btn-lg btn-primary fw-bolder">
                Đi tới trang chủ
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
