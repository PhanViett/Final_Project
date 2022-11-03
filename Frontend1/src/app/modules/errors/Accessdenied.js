import { Link, Outlet } from "react-router-dom";
import { toAbsoluteUrl } from "../../../_metronic/helpers";

export default function Accessdenied() {
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
                color: "red",
              }}
            >
              <i
                className="fas fa-hand-paper"
                style={{
                  color: "red",
                  fontSize: "2rem",
                  marginRight: "1.5rem",
                }}
              ></i>
              Không được quyền truy cập
              <i
                className="fas fa-hand-paper"
                style={{
                  color: "red",
                  fontSize: "2rem",
                  marginLeft: "1.5rem",
                }}
              ></i>
            </p>
          </div>
          <div>
            <h3 style={{ fontWeight: "500" }}>
              Bạn không thể truy cập vào trang này
            </h3>
          </div>
          <div className="pt-lg-10 mb-10">
            <Outlet />
            <div className="text-center">
              <Link to="/" className="btn btn-lg btn-primary fw-bolder">
                QUAY LẠI TRANG CHỦ
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
