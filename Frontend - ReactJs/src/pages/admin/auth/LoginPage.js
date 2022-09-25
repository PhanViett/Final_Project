/* eslint-disable jsx-a11y/alt-text */
import React, { useState } from "react";

import { Form } from "react-bootstrap";
import { useDispatch } from "react-redux";
import { NavLink, useNavigate } from "react-router-dom";


export function LoginPage() {
    const navigate = useNavigate();
    const dispatch = useDispatch();

    const [form, setForm] = useState();
    const [errors, setErrors] = useState();
    const [loading, setLoading] = useState(false);

    const [type, setType] = useState("password");
    const [icon, setIcon] = useState("fas fa-eye text-primary mx-auto");

    const setField = (field, value) => {
        setForm({
            ...form,
            [field]: value,
        });
        if (!!errors[field])
            setErrors({
                ...errors,
                [field]: null,
            });
    };

    function showOrHide(e) {
        e.preventDefault()
        type === "password" ? setType("text") : setType("password");


        if (type === "password") {
            setType("text");
            setIcon("fas fa-eye-slash text-primary mx-auto")
        } else if (type === "text") {
            setType("password");
            setIcon("fas fa-eye text-primary mx-auto");
        }
    }

    return (
        <div id="loginPage">
            <div className="row justify-content-center">
                <div className="col-sm-8 col-lg-5 col-xl-4">
                    <div className="text-center w-100 m-auto">
                        <div className="auth-logo">
                            <NavLink to="/" className="logo logo-dark text-center">
                                <span className="logo">
                                    <img
                                        className="img-logo"
                                        src="media/logos/Logo_BoYTe.png"
                                        alt=""
                                        height="90"
                                        width="90"
                                    />
                                </span>
                            </NavLink>
                        </div>
                    </div>
                    <div className="box-login-wrapper card border-0">
                        <div className="card-body w-100 w-md-75 py-3 px-5 m-auto">
                            <Form>
                                <Form.Group>
                                    <div className="row mb-8">
                                        <span
                                            className="mb-3"
                                            style={{ fontSize: "1rem", fontWeight: 600 }}
                                        >
                                            Tên đăng nhập
                                        </span>
                                        <Form.Control
                                            type="text"
                                            placeholder="Tên đăng nhập"
                                            style={{ fontSize: 14, fontWeight: 400 }}
                                            onChange={(e) => {
                                                setField("username", e.target.value);
                                            }}
                                        />
                                    </div>
                                    <div className="row mb-9">
                                        <span
                                            className="mb-3"
                                            style={{ fontSize: "1rem", fontWeight: 600 }}
                                        >
                                            Mật khẩu
                                        </span>
                                        <div className="input-group px-0" id="show_hide_password">
                                            <Form.Control
                                                className="inputPassword"
                                                type={type}
                                                placeholder="Mật khẩu"
                                                style={{ fontSize: 14, fontWeight: 400 }}
                                                onChange={(e) => {
                                                    setField("password", e.target.value);
                                                }}
                                                autoComplete="off"
                                            />
                                            <div className="input-group-addon">
                                                <button type="button" className="btn btn-light showHidePassword ps-4 pe-3" onClick={showOrHide}>
                                                    <i className={icon}></i>
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </Form.Group>

                                <div className="form-group mb-1 text-center">
                                    <button
                                        className="btn btn-primary btn-block btn-login"
                                        style={{ width: "100%" }}
                                        type="submit"
                                        onClick={(e) => {
                                        }}
                                    >
                                        {loading ? (
                                            <span
                                                className="indicator-progress"
                                                style={{ display: "block" }}
                                            >
                                                Vui lòng chờ...
                                                <span className="spinner-border spinner-border-sm align-middle ms-2"></span>
                                            </span>
                                        ) : (
                                            <span>
                                                <i className="fas fa-chevron-circle-right"></i>
                                                Đăng nhập
                                            </span>
                                        )}
                                    </button>
                                </div>
                            </Form>
                            <div className="form-group text-center mb-3">
                                <NavLink to="/dang-ky">Bạn chưa có tài khoản?</NavLink>
                            </div>

                            <div className="form-group float-start">
                                <div className="form-check">
                                    <input
                                        className="form-check-input"
                                        type="checkbox"
                                        value=""
                                        id="flexCheckDefault"
                                        defaultChecked
                                    />
                                    <label
                                        className="form-check-label"
                                        htmlFor="flexCheckDefault"
                                    >
                                        Lưu mật khẩu
                                    </label>
                                </div>
                            </div>

                            <div className="form-group float-end">
                                <NavLink to="/forgot-password" className="forgot-password">
                                    Quên mật khẩu
                                </NavLink>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}