import axios from "axios";
import { useEffect, useState } from "react";
import { Form } from "react-bootstrap";
import { useDispatch } from "react-redux";
import { NavLink, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import api from "../../../configs/api";
import { authActions } from "../../../redux-module/auth/authSlice";

export function Login() {
    const navigate = useNavigate();
    const dispatch = useDispatch();

    const [form, setForm] = useState({});
    const [errors, setErrors] = useState({});
    const [isLoading, setIsLoading] = useState(false);

    const [type, setType] = useState("password");
    const [icon, setIcon] = useState("fas fa-eye text-primary mx-auto");

    const spanStyle = { fontSize: "15px", fontWeight: 600 }

    useEffect(() => {
        console.log(isLoading);
    }, [isLoading])

    function showOrHide(e) {
        e.preventDefault();
        type === "password" ? setType("text") : setType("password");

        if (type === "password") {
            setType("text");
            setIcon("fas fa-eye-slash text-primary mx-auto");
        } else if (type === "text") {
            setType("password");
            setIcon("fas fa-eye text-primary mx-auto");
        }
    }

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

    const formValidation = () => {
        const newErrors = {};

        const { username, password } = form

        if (!username || username === "") {
            newErrors.username = "Tên đăng nhập không được bỏ trống!"
        }
        if (!password || password === "") {
            newErrors.password = "Mật khẩu không được bỏ trống!"
        }

        return newErrors;
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        setIsLoading(true)
        const newErrors = formValidation();

        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
            setIsLoading(false);
        } else {
            onSubmit()
        }
    }

    const onSubmit = () => {
        axios
            .post(api.API_LOGIN, form)
            .then(({ data }) => {
                if (data) {
                    dispatch(authActions.loginSuccess(data));
                    const role = data?.data?.assigned_role[0].ten_en;
                    if (role && role === "user") {
                        navigate("/trang-chu")
                    } else {
                        navigate("/admin/quan-ly-nguoi-dung")
                    }
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
                setIsLoading(false);
            });

    }


    return (
        <div id="loginPage">
            <div className="row" style={{ height: "100vh" }}>
                <div className="col-5" style={{ backgroundColor: "black" }}> </div>

                <div className="col-7">
                    <div className="px-5 mx-auto" style={{ width: "72%", marginTop: "24vh" }}>
                        <div className="">

                            <div className="row mb-3">
                                <span className="required mb-2" style={spanStyle}>
                                    Tên đăng nhập
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
                                    Mật khẩu
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
                            <div className="form-group mb-1 text-center">
                                {isLoading   ? (
                                    <button className="btn btn-primary btn-block btn-login"
                                        style={{ width: "100%", height: "46px" }}>
                                        <span
                                            className="indicator-progress"
                                            style={{ display: "block" }}
                                        >
                                            Vui lòng chờ...
                                            <span className="spinner-border spinner-border-sm align-middle ms-2"></span>
                                        </span>
                                    </button>
                                ) : (
                                    <button className="btn btn-primary btn-block btn-login"
                                        style={{ width: "100%", height: "46px" }} onClick={(e) => handleSubmit(e)}>
                                        <span>
                                            <i className="fas fa-chevron-circle-right"></i>
                                            &nbsp;&nbsp; Đăng nhập
                                        </span>
                                    </button>
                                )}
                            </div>
                            <div className="form-group text-center mt-2 mb-3">
                                <NavLink to="/dang-ky">Bạn chưa có tài khoản ?</NavLink>
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
                </div>
            </div >
        </div >
    );
}
