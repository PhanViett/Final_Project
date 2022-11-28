import axios from "axios";
import { useEffect } from "react";
import { Dropdown } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import api from "../../app/configs/api";
import { authActions, selectCurrentUser, selectRoleUser } from "../../app/redux-module/auth/authSlice";
import { MenuComponent } from "../assets/ts/components";
import { Content } from "./components/Content";
import { ScrollTop } from "./components/ScrollTop";
import { PageDataProvider } from "./core";

const MasterLayout = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const location = useLocation();

    const currentUser = useSelector(selectCurrentUser)

    const currentRole = useSelector(selectRoleUser)

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

    const onLogOut = () => {
        axios
            .post(api.API_LOGOUT)
            .then(({ data }) => { })
            .catch(() => { })
            .finally(() => { })
        dispatch(authActions.loginSuccess({}));
        navigate("/dang-nhap")
    }

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
                                        <label className="ms-4">{currentUser.ho_ten}</label>
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

                                    <Dropdown.Item onClick={() => onLogOut()}>
                                        Đăng xuất
                                    </Dropdown.Item>
                                </Dropdown.Menu>
                            </Dropdown>
                        </div>
                    </div>
                </div>
                <div>
                    <div className="sidenav text-center">
                        {currentRole === "admin" ?
                            <div className="menu-item">
                                <button className="btn btn-link" onClick={() => navigate("/trang-chu")} title="Trang chủ"><i className="fas fa-home ms-1"></i></button><br />
                                <button className="btn btn-link" onClick={() => navigate("/chan-doan")} title="Chẩn đoán"><i className="fas fa-stethoscope ms-1"></i></button><br />
                                <button className="btn btn-link" onClick={() => navigate("/tin-tuc")} title="Tin tức" style={{ paddingLeft: "6px !important" }}><i className="fas fa-blog ms-1"></i></button><br />
                                <button className="btn btn-link" onClick={() => navigate("/admin/quan-ly-nguoi-dung")} title="Quản lý người dùng"><i className="fas fa-users ms-1"></i></button><br />
                                <button className="btn btn-link" onClick={() => navigate("/admin/quan-ly-lich-su")} title="Quản lý lịch sử"><i className="fas fa-notes-medical ms-1"></i></button><br />
                                <button className="btn btn-link" onClick={() => navigate("/admin/quan-ly-tin-tuc")} title="Quản lý tin tức"><i className="fas fa-newspaper ms-1"></i></button><br />
                            </div>
                            : currentRole === "user" ?
                                <div className="menu-item">
                                    <button className="btn btn-link" onClick={() => navigate("/trang-chu")} title="Trang chủ"><i className="fas fa-home ms-1"></i></button><br />
                                    <button className="btn btn-link" onClick={() => navigate("/chan-doan")} title="Chẩn đoán"><i className="fas fa-stethoscope ms-1"></i></button><br />
                                    <button className="btn btn-link" onClick={() => navigate("/admin/quan-ly-lich-su")} title="Quản lý lịch sử"><i className="fas fa-notes-medical ms-1"></i></button><br />
                                    <button className="btn btn-link" onClick={() => navigate("/tin-tuc")} title="Tin tức" style={{ paddingLeft: "6px !important" }}><i className="fas fa-blog ms-1"></i></button><br />
                                </div>
                                : null
                        }


                        <div className="logout">
                            <button className="btn btn-link" onClick={() => onLogOut()} title="Đăng xuất"><i className="fas fa-sign-out-alt ms-1"></i></button><br />
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

