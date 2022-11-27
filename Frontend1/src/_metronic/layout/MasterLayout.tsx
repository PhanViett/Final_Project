import { useEffect } from "react";
import { Dropdown } from "react-bootstrap";
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
                    <div className="row">
                        <div className="col-6">

                        </div>
                        <div className="col-6 text-end" style={{ paddingTop: "11px", paddingRight: "30px" }}>


                            <Dropdown>
                                <Dropdown.Toggle variant="link" className="py-0">
                                    <img alt="" height={46} width={46} style={{ borderRadius: "50%" }}
                                        src="/media/avatars/default-avatar.jpg" />
                                </Dropdown.Toggle>

                                <Dropdown.Menu>
                                    <Dropdown.Item>
                                        <img alt="" height={46} width={46} style={{ borderRadius: "50%" }}
                                            src="/media/avatars/default-avatar.jpg" />
                                        <label className="ms-4">Nguyễn Đức Đoàn Quân</label>
                                    </Dropdown.Item>
                                    
                                    <Dropdown.Item className="py-0" style={{ height: "4px" }}>
                                        <hr style={{ margin: "2px 0", opacity: "0.08" }} />
                                    </Dropdown.Item>
                                    <Dropdown.Item onClick={() => navigate("/thong-tin-ca-nhan")}>
                                        Cập nhật thông tin
                                    </Dropdown.Item>
                                    <Dropdown.Item className="py-0" style={{ height: "4px" }}>
                                        <hr style={{ margin: "2px 0", opacity: "0.08" }} />
                                    </Dropdown.Item>

                                    <Dropdown.Item onClick={() => navigate("/tin-tuc/viet-bai")}>
                                        Tạo bài viết
                                    </Dropdown.Item>
                                    
                                    <Dropdown.Item onClick={() => navigate("/tin-tuc/danh-sach")}>
                                        Bài viết của tôi
                                    </Dropdown.Item>
                                    
                                    <Dropdown.Item className="py-0" style={{ height: "4px" }}>
                                        <hr style={{ margin: "2px 0", opacity: "0.08" }} />
                                    </Dropdown.Item>
                                    
                                    <Dropdown.Item>
                                        Đăng xuất
                                    </Dropdown.Item>
                                </Dropdown.Menu>
                            </Dropdown>




                        </div>
                    </div>
                </div>
                <div>
                    <div className="sidenav text-center">
                        <div className="menu-item">
                            <button className="btn btn-link" onClick={() => navigate("/trang-chu")} title="Trang chủ"><i className="fas fa-home ms-1"></i></button><br />
                            <button className="btn btn-link" onClick={() => navigate("/chan-doan")} title="Chẩn đoán"><i className="fas fa-stethoscope ms-1"></i></button><br />
                            <button className="btn btn-link" onClick={() => navigate("/tin-tuc")} title="Tin tức"><i className="fas fa-blog ms-1"></i></button><br />
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

