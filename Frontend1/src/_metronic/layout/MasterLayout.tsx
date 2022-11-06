import { useEffect } from "react";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { MenuComponent } from "../assets/ts/components";
import { Content } from "./components/Content";
import { ScrollTop } from "./components/ScrollTop";
import { PageDataProvider } from "./core";

const MasterLayout = () => {
  const navigate = useNavigate();
  const location = useLocation();
  useEffect(() => {
    setTimeout(() => {
      MenuComponent.reinitialization();
    }, 500);
  }, []);

  useEffect(() => {
    setTimeout(() => {
      MenuComponent.reinitialization();
    }, 500);
  }, [location.key]);

  return (
    <PageDataProvider>
      <div id="main" className="main">

        <div className="topnav">

        </div>
        <div>
          <div className="sidenav text-center">
            <div className="menu-item">
              <button className="btn btn-link" onClick={() => navigate("/home")} title="Trang chủ"><i className="fas fa-home ms-1"></i></button><br />
              <button className="btn btn-link" onClick={() => navigate("/admin/quan-ly-nguoi-dung")} title="Quản lý người dùng"><i className="fas fa-users ms-1"></i></button><br />
              <button className="btn btn-link" onClick={() => navigate("/admin/quan-ly-lich-su")} title="Quản lý lịch sử"><i className="fas fa-notes-medical ms-1"></i></button><br />
              <button className="btn btn-link" onClick={() => navigate("/admin/quan-ly-tin-tuc")} title="Quản lý tin tức"><i className="fas fa-newspaper ms-1"></i></button><br />
              {/* <button className="btn btn-link" onClick={() => navigate("/admin/quan-ly-tai-khoan")} title="Quản lý tài khoản"><i className="fas fa-user-circle ms-1"></i></button><br /> */}
            </div>

            <div className="logout">
              <button className="btn btn-link" onClick={() => navigate("/admin/quan-ly-tai-khoan")} title="Đăng xuất"><i className="fas fa-sign-out-alt ms-1"></i></button><br />
            </div>
          </div>  
          <div className="content">
            <Content>
              <Outlet></Outlet>
            </Content>
          </div>
        </div>
      </div>
      <ScrollTop />
    </PageDataProvider>
  );
};

export { MasterLayout };

