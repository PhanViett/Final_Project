/* eslint-disable jsx-a11y/anchor-is-valid */
import { FC, useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";
import {
    authActions,
    selectCurrentUser,
    selectRoleUser
} from "../../../../app/redux-module/auth/authSlice";
import { toAbsoluteUrl } from "../../../helpers";

const HeaderUserMenu: FC = () => {
    const dispatch = useDispatch();

    const roleUser = useSelector(selectRoleUser);
    const currentUser = useSelector(selectCurrentUser);
    const [chucVu, setChucVu] = useState("");

    const [roles, setRoles] = useState<any | undefined>();

    useEffect(() => {
        if (roleUser) {
            setRoles(roleUser);
        }
        // if (currentUser) {
        //     getChucVu(currentUser?.chuc_vu);
        // }
    }, [roleUser, currentUser]);

    // const getChucVu = (chuc_vu: any) => {
    //     let chucVu = optionsDoiTuong.find(
    //         (e: any) => e.value === String(chuc_vu)
    //     );
    //     if (chucVu) {
    //         setChucVu(chucVu?.label);
    //     }
    // };

    return (
        <div
            className="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg menu-state-primary fw-bold py-4 fs-6 w-300px"
            data-kt-menu="true"
        >
            <div className="menu-item px-3">
                {roles &&
                (roles[0]?.ten_en === "duocsi" ||
                    roles[0]?.ten_en === "admin" ||
                    roles[0]?.ten_en === "chuyenvien" ||
                    roles[0]?.ten_en === "lanhdao" ||
                    roles[0]?.ten_en === "chuyenvienhoidong" ||
                    roles[0]?.ten_en === "vanthu") ? (
                    <div>
                        <Link
                            to={"/thong-tin-duoc-si"}
                            className="menu-content d-flex align-items-center px-3"
                        >
                            <div className="symbol symbol-50px me-5">
                                <img
                                    alt="Logo"
                                    src={toAbsoluteUrl(
                                        "/media/avatars/blank.png"
                                    )}
                                />
                            </div>

                            <div className="d-flex flex-column">
                                <div className="fw-bolder d-flex align-items-center fs-5">
                                    {currentUser?.ho} {currentUser?.ten}
                                </div>
                                <span className="fw-bold text-muted text-hover-primary fs-7">
                                    {currentUser?.email}
                                </span>
                            </div>
                        </Link>
                        <div className="separator my-2"></div>
                    </div>
                ) : null}
                {roles && roles[0]?.ten_en === "tochuc" ? (
                    <div>
                        <Link
                            to={"/thong-tin-to-chuc"}
                            className="menu-content d-flex align-items-center px-3"
                        >
                            <div className="symbol symbol-50px me-5">
                                <img
                                    alt="Logo"
                                    src={toAbsoluteUrl(
                                        "/media/avatars/blank.png"
                                    )}
                                />
                            </div>

                            <div className="d-flex flex-column">
                                <div className="fw-bolder d-flex align-items-center fs-5">
                                    {currentUser?.ho} {currentUser?.ten}
                                </div>
                                <a
                                    href="#"
                                    className="fw-bold text-muted text-hover-primary fs-7"
                                >
                                    {currentUser?.email}
                                </a>
                            </div>
                        </Link>
                        <div className="separator my-2"></div>
                    </div>
                ) : null}
            </div>
            <div className="menu-item px-5">
                <Link
                    to={""}
                    className="menu-link px-5"
                    onClick={(e) => e.preventDefault()}
                >
                    {/* Vai trò : {currentUser?.assigned_role[0]?.ten} */}
                    Chức vụ : {chucVu ? chucVu : "N/A"}
                </Link>
            </div>

            <div className="separator my-2"></div>

            {/* <Languages /> */}
            {roles &&
            (roles[0]?.ten_en === "lanhdao" || roles[0]?.ten_en === "admin") ? (
                <div className="menu-item px-5 my-1">
                    <Link to="/quan-ly-nguoi-dung" className="menu-link px-5">
                        Quản lý người dùng
                    </Link>
                </div>
            ) : null}

            <div className="menu-item px-5 my-1">
                <Link to="/doi-mat-khau" className="menu-link px-5">
                    Đổi mật khẩu
                </Link>
            </div>

            <div className="menu-item px-5">
                <a
                    onClick={() => {
                        dispatch(authActions.logout());
                        // localStorage.clear();
                    }}
                    className="menu-link px-5"
                >
                    Đăng xuất
                </a>
            </div>
        </div>
    );
};

export { HeaderUserMenu };

