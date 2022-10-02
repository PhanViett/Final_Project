/* eslint-disable jsx-a11y/alt-text */
import React, { useState } from "react";
import { Form } from "react-bootstrap";
import { NavLink } from "react-router-dom";

export function LoginPage() {

  const [isLogin, setIsLogin] = useState(true);

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

  const renderLayout = () => {
    if (isLogin === true) {
      return (
        <div className="px-5 mx-auto" style={{ width: "72%", marginTop: "20vh" }}>
          <div className="box-login-wrapper">
            <Form>
              <Form.Group>
                <div className="row mb-3">
                  <span
                    className="mb-2"
                    style={{ fontSize: "1rem", fontWeight: 600 }}
                  >
                    Tên đăng nhập
                  </span>
                  <Form.Control
                    type="text"
                    placeholder="Tên đăng nhập" clear
                    style={{ fontSize: 14, fontWeight: 400 }}
                    onChange={(e) => {
                      setField("username", e.target.value);
                    }}
                  />
                </div>
                <div className="row mb-3">
                  <span
                    className="mb-2"
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
                      <button type="button" className="btn ps-3 pe-3" style={{ backgroundColor: "#fff", border: "1px solid #ced4da", borderTopLeftRadius: 0, borderBottomLeftRadius: 0 }} onClick={showOrHide}>
                        <i className={icon}></i>
                      </button>
                    </div>
                  </div>
                </div>
              </Form.Group>

              <div className="form-group mb-1 text-center">
                <button
                  className="btn btn-primary btn-block btn-login"
                  style={{ width: "100%", height: "46px" }}
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
                        &nbsp;&nbsp; Đăng nhập
                    </span>
                  )}
                </button>
              </div>
            </Form>
            <div className="form-group text-center mt-2 mb-3">
              <NavLink onClick={() => setIsLogin(false)}>Bạn chưa có tài khoản ?</NavLink>
            </div>

            <div className="form-group float-start">
              <div className="form-check">
                <input
                  className="form-check-input"
                  type="checkbox"
                  value=""
                  id="flexCheckDefault"
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
      )
    } else if (isLogin === false) {
      return (
        <div className="px-5 mx-auto" style={{ width: "72%", marginTop: "16vh" }}>
          <div className="box-login-wrapper">
            <Form>
              <Form.Group>
                <div className="row mb-3">
                  <span
                    className="mb-2"
                    style={{ fontSize: "1rem", fontWeight: 600 }}
                  >
                    Họ và tên
                  </span>
                  <Form.Control
                    type="text"
                    placeholder="Nhập họ và tên" clear
                    style={{ fontSize: 14, fontWeight: 400 }}
                    onChange={(e) => {
                      setField("username", e.target.value);
                    }}
                  />
                </div>
                <div className="row mb-3">
                  <span
                    className="mb-2"
                    style={{ fontSize: "1rem", fontWeight: 600 }}
                  >
                    Tên đăng nhập
                  </span>
                  <Form.Control
                    type="text"
                    placeholder="Tên đăng nhập" clear
                    style={{ fontSize: 14, fontWeight: 400 }}
                    onChange={(e) => {
                      setField("username", e.target.value);
                    }}
                  />
                </div>
                <div className="row mb-3">
                  <span
                    className="mb-2"
                    style={{ fontSize: "1rem", fontWeight: 600 }}
                  >
                    Số điện thoại
                  </span>
                  <Form.Control
                    type="text"
                    placeholder="Nhập số điện thoại" clear
                    style={{ fontSize: 14, fontWeight: 400 }}
                    onChange={(e) => {
                      setField("username", e.target.value);
                    }}
                  />
                </div>
                <div className="row mb-3">
                  <span
                    className="mb-2"
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
                      <button type="button" className="btn ps-3 pe-3" style={{ backgroundColor: "#fff", border: "1px solid #ced4da", borderTopLeftRadius: 0, borderBottomLeftRadius: 0 }} onClick={showOrHide}>
                        <i className={icon}></i>
                      </button>
                    </div>
                  </div>
                </div>
                <div className="row mb-3">
                  <span
                    className="mb-2"
                    style={{ fontSize: "1rem", fontWeight: 600 }}
                  >
                    Nhập lại mật khẩu
                  </span>
                  <div className="input-group px-0" id="show_hide_password">
                    <Form.Control
                      className="inputPassword"
                      type={type}
                      placeholder="Xác nhận mật khẩu"
                      style={{ fontSize: 14, fontWeight: 400 }}
                      onChange={(e) => {
                        setField("password", e.target.value);
                      }}
                      autoComplete="off"
                    />
                    <div className="input-group-addon">
                      <button type="button" className="btn ps-3 pe-3" style={{ backgroundColor: "#fff", border: "1px solid #ced4da", borderTopLeftRadius: 0, borderBottomLeftRadius: 0 }} onClick={showOrHide}>
                        <i className={icon}></i>
                      </button>
                    </div>
                  </div>
                </div>
              </Form.Group>

              <div className="form-group mb-1 text-center">
                <button
                  className="btn btn-primary btn-block btn-login"
                  style={{ width: "100%", height: "46px"}}
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
                        &nbsp; &nbsp; Đăng ký
                    </span>
                  )}
                </button>
              </div>
            </Form>
            <div className="form-group text-center mt-2 mb-3">
              <NavLink onClick={() => setIsLogin(true)}>Bạn đã có tài khoản ?</NavLink>
            </div>

            <div className="form-group float-start">
              <div className="form-check">
                <input
                  className="form-check-input"
                  type="checkbox"
                  value=""
                  id="flexCheckDefault"
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
      )
    } else {
      return null;
    }
  }

  useState(() => {
    renderLayout();
  }, [isLogin])
  return (
    <div id="loginPage">
      <div className="row" style={{ height: "100vh" }}>

        {/* LEFT SIDE */}
        <div className="col-5" style={{ backgroundColor: "black" }}> </div>

        {/* RIGHT SIDE */}
        <div className="col-7">
          {renderLayout()}
        </div>
      </div>
    </div>
  );
}