import axios from "axios";
import React, { useState } from "react";
import { Form } from "react-bootstrap";
import { NavLink, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import api from "../../../configs/api";

export function LoginPage() {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);

  const [form, setForm] = useState({});
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const [type, setType] = useState("password");
  const [icon, setIcon] = useState("fas fa-eye text-primary mx-auto");

  const spanStyle = { fontSize: "15px", fontWeight: 600 }

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

  const resetStates = () => {
    setForm({});
    setErrors({});
  }

  const handleSubmit = (e, type) => {
    e.preventDefault();
    const newErrors = formValidation(type);
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
    } else {
      onSubmit(type)
    }
  }

  const formValidation = (type) => {
    const newErrors = {};

    if (type === "login") {
      console.log(form);
      const { username, password } = form
      
      if (!username || username === "") {
        newErrors.username = "Tên đăng nhập không được bỏ trống!"
      }
      if (!password || password === "") {
        newErrors.password = "Mật khẩu không được bỏ trống!"
      }
    } 
    else if (type === "register") {
      const { ho, ten, email, tai_khoan, mat_khau, retype_mat_khau, dien_thoai } = form

      if (!ho || ho === "") {
        newErrors.ho = "Họ không được bỏ trống!"
      }
      if (!ten || ten === "") {
        newErrors.ten = "Tên không được bỏ trống!"
      }
      if (!email || email === "") {
        newErrors.email = "Email không được bỏ trống!"
      } else if (/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(email) === false) {
        newErrors.email = "Email không hợp lệ!"
      }
      if (!tai_khoan || tai_khoan === "") {
        newErrors.tai_khoan = "Tài khoản không được bỏ trống!"
      }
      if (!dien_thoai || dien_thoai === "") {
        newErrors.dien_thoai = "Điện thoại không được bỏ trống!"
      } else if (dien_thoai.split("").length !== 10) {
        newErrors.dien_thoai = "Điện thoại không hợp lệ!"
      }
      if (!mat_khau || mat_khau === "") {
        newErrors.mat_khau = "Mật khẩu không được bỏ trống!"
      }
      if (!retype_mat_khau || retype_mat_khau === "") {
        newErrors.retype_mat_khau = "Mật khẩu xác nhận không được bỏ trống!"
      }
      if (mat_khau !== retype_mat_khau) {
        newErrors.retype_mat_khau = "Xác nhận mật khẩu không trùng khớp!"
      }
    }

    return newErrors;
  }

  const onSubmit = (type) => {
    if (type === "login") {
      axios
        .post(api.API_LOGIN, form)
        .then((data) => {
          if (data) {
            navigate("/admin/quan-ly-nguoi-dung")
          }
        })
        .catch((error) => {
          toast.error("Có lỗi xảy ra khi đăng nhập vào hệ thống", {
            position: "top-right",
            autoClose: 1000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            toastId: "error",
          });
        })
        .finally(() => {
          resetStates();
        });
    } else if (type === "register") {
      delete form.retype_mat_khau
      
      axios
        .post(api.API_REGISTER, form)
        .then((data) => {
          if (data.status === "SUCCESS") {
            setTimeout(() => {
              navigate("/login")
            }, 2000);
          }
        })
        .catch((error) => {
          toast.error("Có lỗi xảy ra khi đăng ký tài khoản", {
            position: "top-right",
            autoClose: 1000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            toastId: "error",
          });
        })
        .finally(() => {
          resetStates();
        });
    } else {
      return;
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
                  <span className="mb-2" style={spanStyle}>
                    Tên đăng nhập <span className="text-danger">*</span>
                  </span>
                  <Form.Control
                    type="text"
                    placeholder="Tên đăng nhập"
                    style={{ fontSize: 14, fontWeight: 400 }}
                    value={form?.username ? form?.username : ""}
                    onChange={(e) => setField("username", e.target.value)}
                  />
                  {errors?.username ? (<span className="text-danger">{errors?.username}</span>) : ("")}

                </div>
                <div className="row mb-3">
                  <span className="required mb-2" style={spanStyle}>
                    Mật khẩu <span className="text-danger">*</span>
                  </span>
                  <div className="input-group px-0" id="show_hide_password">
                    <Form.Control
                      type={type}
                      placeholder="Mật khẩu"
                      style={{ fontSize: 14, fontWeight: 400 }}
                      value={form?.password ? form?.password : ""}
                      onChange={(e) => setField("password", e.target.value)}
                    />
                    <div className="input-group-addon">
                      <button type="button" className="btn ps-3 pe-3" style={{ backgroundColor: "#fff", border: "1px solid #ced4da", borderTopLeftRadius: 0, borderBottomLeftRadius: 0 }} onClick={showOrHide}>
                        <i className={icon}></i>
                      </button>
                    </div>
                  </div>
                  {errors?.password ? (<span className="text-danger">{errors?.password}</span>) : ("")}

                </div>
              </Form.Group>

              <div className="form-group mb-1 text-center">
                <button
                  className="btn btn-primary btn-block btn-login"
                  style={{ width: "100%", height: "46px" }}
                  onClick={(e) => handleSubmit(e, "login")}
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
              <NavLink onClick={() => { setIsLogin(false); resetStates() }}>Bạn chưa có tài khoản ?</NavLink>
            </div>

            <div className="form-group float-start">
              <div className="form-check">
                <input
                  type="checkbox"
                  id="flexCheckDefault"
                  className="form-check-input"
                />
                <label
                  htmlFor="flexCheckDefault"
                  className="form-check-label"
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
                  <div className="col-7 px-0">
                    <span className="mx-2 mb-2" style={spanStyle}>
                      Họ <span className="text-danger">*</span>
                    </span>
                    <Form.Control
                      type="text"
                      placeholder="Nhập họ và tên"
                      value={form?.ho ? form?.ho : ""}
                      style={{ fontSize: 14, fontWeight: 400 }}
                      onChange={(e) => setField("ho", e.target.value)}
                    />
                    {errors?.ho ? (<span className="text-danger">{errors?.ho}</span>) : ("")}
                  </div>

                  <div className="col-5 pl-1 pr-0">
                    <span className="mx-2 mb-2" style={spanStyle}>
                      Tên <span className="text-danger">*</span>
                    </span>
                    <Form.Control
                      type="text"
                      placeholder="Nhập tên"
                      value={form?.ten ? form?.ten : ""}
                      style={{ fontSize: 14, fontWeight: 400 }}
                      onChange={(e) => setField("ten", e.target.value)}
                    />
                    {errors?.ten ? (<span className="text-danger">{errors?.ten}</span>) : ("")}
                  </div>
                </div>

                <div className="row mb-3">
                  <span className="mb-2" style={spanStyle}>
                    Tên đăng nhập <span className="text-danger">*</span>
                  </span>
                  <Form.Control
                    type="text"
                    placeholder="Tên đăng nhập"
                    style={{ fontSize: 14, fontWeight: 400 }}
                    value={form?.tai_khoan ? form?.tai_khoan : ""}
                    onChange={(e) => setField("tai_khoan", e.target.value)}
                  />
                  {errors?.tai_khoan ? (<span className="text-danger">{errors?.tai_khoan}</span>) : ("")}
                </div>

                <div className="row mb-3">
                  <span className="mb-2" style={spanStyle}>
                    Số điện thoại <span className="text-danger">*</span>
                  </span>
                  <Form.Control
                    type="text"
                    placeholder="Nhập số điện thoại"
                    style={{ fontSize: 14, fontWeight: 400 }}
                    value={form?.dien_thoai ? form?.dien_thoai : ""}
                    onChange={(e) => setField("dien_thoai", e.target.value)}
                  />
                  {errors?.dien_thoai ? (<span className="text-danger">{errors?.dien_thoai}</span>) : ("")}
                </div>

                <div className="row mb-3">
                  <span className="mb-2" style={spanStyle}>
                    Email <span className="text-danger">*</span>
                  </span>
                  <Form.Control
                    type="text"
                    placeholder="Nhập email"
                    value={form?.email ? form?.email : ""}
                    style={{ fontSize: 14, fontWeight: 400 }}
                    onChange={(e) => setField("email", e.target.value)}
                  />
                  {errors?.email ? (<span className="text-danger">{errors?.email}</span>) : ("")}
                </div>

                <div className="row mb-3">
                  <span className="mb-2" style={spanStyle}>
                    Mật khẩu <span className="text-danger">*</span>
                  </span>
                  <div className="input-group px-0" id="show_hide_password">
                    <Form.Control
                      type={type}
                      placeholder="Mật khẩu"
                      className="inputPassword"
                      value={form?.mat_khau ? form?.mat_khau : ""}
                      style={{ fontSize: 14, fontWeight: 400 }}
                      onChange={(e) => setField("mat_khau", e.target.value)}
                      autoComplete="off"
                    />
                    <div className="input-group-addon">
                      <button type="button" className="btn ps-3 pe-3" style={{ backgroundColor: "#fff", border: "1px solid #ced4da", borderTopLeftRadius: 0, borderBottomLeftRadius: 0 }} onClick={showOrHide}>
                        <i className={icon}></i>
                      </button>
                    </div>
                  </div>
                  {errors?.mat_khau ? (<span className="text-danger">{errors?.mat_khau}</span>) : ("")}
                </div>

                <div className="row mb-3">
                  <span className="mb-2" style={spanStyle}>
                    Nhập lại mật khẩu <span className="text-danger">*</span>
                  </span>
                  <div className="input-group px-0" id="show_hide_password">
                    <Form.Control
                      type={type}
                      className="inputPassword"
                      placeholder="Xác nhận mật khẩu"
                      style={{ fontSize: 14, fontWeight: 400 }}
                      value={form?.retype_mat_khau ? form?.retype_mat_khau : ""}
                      onChange={(e) => setField("retype_mat_khau", e.target.value)}
                      autoComplete="off"
                    />
                    <div className="input-group-addon">
                      <button type="button" className="btn ps-3 pe-3" style={{ backgroundColor: "#fff", border: "1px solid #ced4da", borderTopLeftRadius: 0, borderBottomLeftRadius: 0 }} onClick={showOrHide}>
                        <i className={icon}></i>
                      </button>
                    </div>
                  </div>
                  {errors?.retype_mat_khau ? (<span className="text-danger">{errors?.retype_mat_khau}</span>) : ("")}
                </div>

              </Form.Group>

              <div className="form-group mb-1 text-center">
                <button
                  className="btn btn-primary btn-block btn-login"
                  style={{ width: "100%", height: "46px" }}
                  onClick={(e) => {
                    handleSubmit(e, "register")
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
              <NavLink onClick={() => {setIsLogin(true); resetStates()}}>Bạn đã có tài khoản ?</NavLink>
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