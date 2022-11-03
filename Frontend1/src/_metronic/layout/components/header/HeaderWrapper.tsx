/* eslint-disable react-hooks/exhaustive-deps */
import clsx from "clsx";
import { useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { KTSVG } from "../../../helpers";
import { useLayout } from "../../core";
import { Header } from "./Header";
import { DefaultTitle } from "./page-title/DefaultTitle";
import { Topbar } from "./Topbar";
import { selectRoleUser } from "../../../../app/redux-module/auth/authSlice";

export function HeaderWrapper() {
    const currentRole = useSelector(selectRoleUser);
    const currRole = currentRole[0]?.ten_en;
    const { config, classes, attributes } = useLayout();
    const { header, aside } = config;

    return (
        <div
            id="kt_header"
            className={clsx(
                "header",
                classes.header.join(" "),
                "align-items-stretch"
            )}
            {...attributes.headerMenu}
        >
            <div
                className={clsx(
                    classes.headerContainer.join(" "),
                    "d-flex flex-row-reverse justify-content-between"
                )}
            >
                {/* begin::Aside mobile toggle */}
                {aside.display && (
                    <div
                        className="d-flex align-items-center d-lg-none ms-n3 me-1"
                        title="Show aside menu"
                    >
                        <div
                            className="btn btn-icon btn-active-light-primary w-30px h-30px w-md-40px h-md-40px"
                            id="kt_aside_mobile_toggle"
                        >
                            <KTSVG
                                path="/media/icons/duotune/abstract/abs015.svg"
                                className="svg-icon-2x mt-1"
                            />
                        </div>
                    </div>
                )}
                {/* end::Aside mobile toggle */}

                {/* begin::Wrapper */}
                <div className="d-flex align-items-stretch justify-content-end flex-lg-grow-1">
                    {/* begin::Navbar */}
                    {header.left === "menu" && (
                        <div
                            className="d-flex align-items-stretch"
                            id="kt_header_nav"
                        >
                            <Header />
                        </div>
                    )}

                    {header.left === "page-title" && (
                        <div
                            className="d-flex align-items-center"
                            id="kt_header_nav"
                        >
                            <DefaultTitle />
                        </div>
                    )}

                    <div className="d-flex align-items-stretch flex-shrink-0">
                        <Topbar />
                    </div>
                </div>
                {/* end::Wrapper */}

                {/* begin::Logo */}
                {!aside.display && (
                    <div className="d-flex align-items-center flex-grow-1 flex-lg-grow-0">
                        {currRole === "duocsi" ? (
                            <>
                                <Link
                                    to="/admin/chung-chi-hanh-nghe"
                                    className=""
                                >
                                    <img
                                        alt="Logo"
                                        src="/media/logos/Logo_BoYTe.png"
                                        className="h-60px"
                                    />
                                </Link>
                                <Link
                                    to="/admin/chung-chi-hanh-nghe"
                                    style={{ marginLeft: "10px" }}
                                >
                                    <span
                                        className="text-white"
                                        style={{ fontWeight: 600 }}
                                    >
                                        SỞ Y TẾ TP HỒ CHÍ MINH
                                    </span>
                                    <br />
                                    <span className="text-white">
                                        HỆ THỐNG QUẢN LÝ HÀNH NGHỀ DƯỢC
                                    </span>
                                </Link>
                            </>
                        ) : currRole === "tochuc" ? (
                            <>
                                {" "}
                                <Link to="/giay-phep-kinh-doanh" className="">
                                    <img
                                        alt="Logo"
                                        src="/media/logos/Logo_BoYTe.png"
                                        className="h-60px"
                                    />
                                </Link>
                                <Link
                                    to="/giay-phep-kinh-doanh"
                                    style={{ marginLeft: "10px" }}
                                >
                                    <span
                                        className="text-white"
                                        style={{ fontWeight: 600 }}
                                    >
                                        SỞ Y TẾ TP HỒ CHÍ MINH
                                    </span>
                                    <br />
                                    <span className="text-white">
                                        HỆ THỐNG QUẢN LÝ HÀNH NGHỀ DƯỢC
                                    </span>
                                </Link>
                            </>
                        ) : (
                            <>
                                <Link to="/dashboard" className="">
                                    <img
                                        alt="Logo"
                                        src="/media/logos/Logo_BoYTe.png"
                                        className="h-60px"
                                    />
                                </Link>
                                <Link
                                    to="/dashboard"
                                    style={{ marginLeft: "10px" }}
                                >
                                    <span
                                        className="text-white"
                                        style={{ fontWeight: 600 }}
                                    >
                                        SỞ Y TẾ TP HỒ CHÍ MINH
                                    </span>
                                    <br />
                                    <span className="text-white">
                                        HỆ THỐNG QUẢN LÝ HÀNH NGHỀ DƯỢC
                                    </span>
                                </Link>
                            </>
                        )}
                    </div>
                )}
                {/* end::Logo */}
            </div>
        </div>
    );
}
