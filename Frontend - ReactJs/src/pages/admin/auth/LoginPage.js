import React, { useState } from "react";

import axios from "axios";
import { useFormik } from "formik";
import BlockUi from "react-block-ui";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { Navigate, NavLink, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import * as Yup from "yup";

import { TailSpin } from "react-loader-spinner";
import api from "../../../configs/api";
import { loginSuccess } from "../../../saga-modules/auth/actions";

export function LoginPage() {
    var md5 = require("md5");
    const loginSchema = Yup.object().shape({
        username: Yup.string()
            .min(3, "Minimum 3 symbols")
            .max(50, "Maximum 50 symbols")
            .required("Email is required"),
        password: Yup.string()
            .min(3, "Minimum 3 symbols")
            .max(50, "Maximum 50 symbols")
            .required("Password is required"),
    });

    const initialValues = {
        username: "",
        password: "",
    };

    const [loading, setLoading] = useState(false);
    const dispatch = useDispatch();
    let navigate = useNavigate();

    const isAuthorized = useSelector(
        (state) => state.auth.isAuthorized,
        shallowEqual
    );

    const formik = useFormik({
        initialValues,
        validationSchema: loginSchema,
        onSubmit: (values, { setStatus, setSubmitting }) => {
            let dataLogin = {
                username: values.username,
                password: md5(values.password),
            };
            setLoading(true);
            axios
                .post(api.API_LOGIN, dataLogin)
                .then(({ data }) => {
                    dispatch(loginSuccess({ dataLogin: data }));
                    navigate("/admin");
                    setLoading(false);
                })
                .catch((error) => {

                    toast.error(error.response?.data?.msg, {
                        position: "top-right",
                        autoClose: 3000,
                        hideProgressBar: false,
                        closeOnClick: true,
                        pauseOnHover: true,
                        draggable: true,
                        progress: undefined,
                        toastId: "error",
                    });
                    setLoading(false);
                });
        },
    });
    const getInputClasses = (fieldname) => {
        if (formik.touched[fieldname] && formik.errors[fieldname]) {
            return "is-invalid";
        }

        if (formik.touched[fieldname] && !formik.errors[fieldname]) {
            return "is-valid";
        }

        return "";
    };

    if (isAuthorized) {
        return <Navigate to="/admin" />;
    }

    return (
        <>
            <div id="loginPage" className="container ">
                <div className="row justify-content-center mt-5">
                    <div className="col-lg-4 col-md-6 col-sm-6">
                        <div className="card shadow">
                            <div className="card-title text-center border-bottom">
                                <NavLink to={"/"}>
                                    <h2 className="p-3">
                                        <img
                                            className="logo border-0"
                                            src="/media/Logo_BoYTe.png"
                                        />
                                    </h2>
                                </NavLink>
                            </div>
                            <div className="card-body">
                                <BlockUi
                                    tag="div"
                                    blocking={loading}
                                    loader={
                                        <TailSpin
                                            arialLabel="loading-indicator"
                                            height={60}
                                            width={60}
                                            strokeWidth={2}
                                            strokeWidthSecondary={1}
                                            color="blue"
                                            secondaryColor="blue"
                                            wrapperClass={"d-inline-flex"}
                                        />
                                    }
                                >
                                    <form
                                        onSubmit={formik.handleSubmit}
                                        noValidate
                                        id="kt_login_signin_form"
                                    >
                                        <div className="mb-2 form-group">
                                            <label className="form-label d-block p-0">
                                                Username/Email
                                            </label>
                                            <input
                                                label="Tên đăng nhập"
                                                placeholder="Tên đăng nhập"
                                                type="username"
                                                className={`${getInputClasses(
                                                    "username"
                                                )} w-100 form-control`}
                                                name="username"
                                                {...formik.getFieldProps("username")}
                                            />
                                        </div>
                                        {formik.touched.username && formik.errors.username ? (
                                            <div className="fv-plugins-message-container">
                                                <div className="text-danger fv-help-block">
                                                    {formik.errors.username}
                                                </div>
                                            </div>
                                        ) : null}
                                        <div className="mb-4 form-group">
                                            <label className="form-label d-block">Password</label>
                                            <input
                                                placeholder="Mật khẩu"
                                                type="password"
                                                className={`${getInputClasses(
                                                    "password"
                                                )} w-100 form-control`}
                                                name="password"
                                                {...formik.getFieldProps("password")}
                                            />
                                            {formik.touched.password && formik.errors.password ? (
                                                <div className="fv-plugins-message-container">
                                                    <div className="text-danger fv-help-block">
                                                        {formik.errors.password}
                                                    </div>
                                                </div>
                                            ) : null}
                                        </div>
                                        <div className="d-grid">
                                            {!loading && (
                                                <button
                                                    type="submit"
                                                    className="btn text-light btn-success"
                                                >
                                                    Đăng nhập
                                                </button>
                                            )}
                                            {loading && (
                                                <span
                                                    className="indicator-progress"
                                                    style={{ display: "block" }}
                                                >
                                                    Please wait...
                                                    <span className="spinner-border spinner-border-sm align-middle ms-2"></span>
                                                </span>
                                            )}
                                        </div>
                                    </form>
                                </BlockUi>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
}