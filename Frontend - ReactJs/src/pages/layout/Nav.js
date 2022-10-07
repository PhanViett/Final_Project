import { FaUserCircle } from "react-icons/fa";
import { MdLogout } from "react-icons/md";
import { useSelector } from "react-redux";
import { useDispatch } from "react-redux";
import { logout } from "../../saga-modules/auth/actions";
import "react-pro-sidebar/dist/css/styles.css";
import React from "react";
import { NavLink } from "react-router-dom";

export default function Nav(props) {    
    const { handleCollapsedChange, collapsed } = props;
    const dispatch = useDispatch();
    const userInfo = useSelector(
        (state) => state.auth?.user);

    return (
        <nav
            id="nav-admin"
            className="navbar navbar-expand-lg navbar-light p-0"
        >
            <div className="container-fluid position-relative">
                <button style={{ backgroundColor: 'red' }}
                    className="border-0"
                    onClick={handleCollapsedChange}>
                    {!collapsed ? <i className="fas fa-solid fa-outdent text-white"></i> : <i className="fas fa-solid fa-indent text-white"></i>}
                </button>

                <div className="btn-group">
                    <button
                        type="button"
                        className="btn btn-primary dropdown-toggle"
                        data-toggle="dropdown"
                        aria-haspopup="true"
                        aria-expanded="false"
                    >
                        <span className="text-white ">
                            <FaUserCircle size={30} color="white" /> {userInfo?.ten}
                        </span>
                    </button>
                    <div className="dropdown-menu dropdown-menu-right">
                        <NavLink style={{ textDecoration: "none" }} to="thong-tin-tai-khoan">
                            <button className="dropdown-item"
                                type="button"
                            >
                                <FaUserCircle /> Thông tin tài khoản
                            </button>
                        </NavLink>  
                        <button className="dropdown-item"
                            onClick={() => {
                                dispatch(logout());
                            }}
                            type="button"
                        >
                            <MdLogout /> Đăng xuất
                        </button>

                    </div>
                </div>
            </div>
        </nav>
    );
}
