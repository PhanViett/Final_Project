import axios from 'axios';
import md5 from 'md5';
import React, { useEffect, useState } from 'react';
import BlockUi from 'react-block-ui';
import { Button } from 'react-bootstrap';
import { TailSpin } from 'react-loader-spinner';
import { useDispatch, useSelector } from 'react-redux';
import Switch from "react-switch";
import { toast } from 'react-toastify';
import validator from 'validator';
import api from '../../../configs/api';
// import { updateUserSuccess } from '../../../saga-modules/auth/actions';
// import { setTitle } from '../../../saga-modules/common/actions';

export function UserInfo() {
    const dispatch = useDispatch()
    const [form, setForm] = useState({});
    const [errors, setErrors] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [CheckedMatKhau, setCheckedMatKhau] = useState(false);


    const userInfo = useSelector(
        (state) => state.auth?.user);

    useEffect(() => {
        getUserInfo()
        // dispatch(setTitle({ title: "Thông tin tài khoản" }));
    }, []);

    const setField = (field, value) => {
        setForm({
            ...form,
            [field]: value,
        });
        // Check and see if errors exist, and remove them from the error object:
        if (!!errors[field])
            setErrors({
                ...errors,
                [field]: null,
            });
    };

    const findFormErrors = () => {
        const { ho, ten, so_dien_thoai, email, password, re_password } = form;
        const newErrors = {};
        // name errors
        if (!ten || ten === "")
            newErrors.ten = "Tên không được bỏ trống!";
        if (!ho || ho === "")
            newErrors.ho = "Họ không được bỏ trống!";
        if (!validator.isEmail(email) || !email || email === "") {
            newErrors.email = "Email không hợp lệ!";
        }
        if (!validator.isMobilePhone(so_dien_thoai, "vi-VN") || !so_dien_thoai || so_dien_thoai === "") newErrors.so_dien_thoai = "Số điện thoại không hợp lệ!";
        // if (!email || email === "")
        //   newErrors.valueDanhMuc =  "Email không được bỏ trống!";
        // if (!mo_ta || mo_ta === "") newErrors.mo_ta = "Mô tả không được bỏ trống!";
        if ((!password || password === "") && CheckedMatKhau)
            newErrors.password = "Vui lòng nhập mật khẩu";
        if (re_password !== password && CheckedMatKhau)
            newErrors.re_password = "Mật khẩu nhập lại không chính xác";
        return newErrors;
    };


    const getUserInfo = async () => {
        await setIsLoading(true);
        axios
            .get(api.LIST_USER + "/" + userInfo?.id)
            .then(async ({ data }) => {
                console.log("log data", data);
                setForm(data?.nguoi_dung)
            })
            .catch((error) => {
                if (error?.response?.data) {
                    toast.error(error.response.data.msg, {
                        position: "top-right",
                        autoClose: 3000,
                        hideProgressBar: false,
                        closeOnClick: true,
                        pauseOnHover: true,
                        draggable: true,
                        progress: undefined,
                        toastId: "error",
                    });
                }
            })
            .finally(() => {
                setIsLoading(false);
            });
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        // get our new errors
        const newErrors = findFormErrors();
        // Conditional logic:
        if (Object.keys(newErrors).length > 0) {
            console.log(newErrors);
            // We got errors!
            setErrors(newErrors);
        } else {
            // No errors! Put any logic here for the form submission!
            updateUser();
        }
    };

    const updateUser = async () => {
        await setIsLoading(true);
        const { ten, so_dien_thoai, email, password, ho } = form;
        let jsonUpdateUser = {
            ho, ten, so_dien_thoai, email, mat_khau: password ? md5(password) : null
        }
        axios.put(api.LIST_USER + "/" + userInfo?.id, jsonUpdateUser)
            .then(async ({ data }) => {
                console.log("log data", data);
                toast.success("Cập nhật thông tin thành công", {
                    position: "top-right",
                    autoClose: 2000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                    toastId: "success",
                });
                // dispatch(updateUserSuccess({ dataUser: data?.nguoi_dung }))
            })
            .catch((error) => {
                if (error.response.data) {
                    toast.error(error.response.data?.msg, {
                        position: "top-right",
                        autoClose: 3000,
                        hideProgressBar: false,
                        closeOnClick: true,
                        pauseOnHover: true,
                        draggable: true,
                        progress: undefined,
                        toastId: "error",
                    });
                }
            })
            .finally(() => {
                setIsLoading(false);
            });
    }


    return (
        <div className="page">
            <BlockUi
                tag="div"
                blocking={isLoading}
                loader={
                    <TailSpin
                        ariaLabel="loading-indicator"
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
                <div className="card">
                    <div className="card-body">
                        <div className="row">
                            <div className="col-md-6">
                                <div className="form-group required">
                                    <div className="row">
                                        <div className="col-6"><label>
                                            Tên<span className="text-danger">*</span>
                                        </label>
                                            <input
                                                type="text"
                                                placeholder="Nhập tên"
                                                className="form-control"
                                                onChange={(e) => setField("ten", e.target.value)}
                                                value={form?.ten === null ? "" : form?.ten}
                                            />
                                            {errors?.ten !== null ? (
                                                <span className="text-danger"> {errors?.ten}</span>
                                            ) : null}</div>
                                        <div className="col-6"><label>
                                            Họ<span className="text-danger">*</span>
                                        </label>
                                            <input
                                                type="text"
                                                placeholder="Nhập họ"
                                                className="form-control"
                                                onChange={(e) => setField("ho", e.target.value)}
                                                value={form?.ho === null ? "" : form?.ho}
                                            />
                                            {errors?.ho !== null ? (
                                                <span className="text-danger"> {errors?.ho}</span>
                                            ) : null}</div>

                                    </div>
                                </div>

                                {/* <div className="form-group required">
                                    <label>
                                        Tên đăng nhập
                                    </label>
                                    <input
                                        type="text"
                                        disabled={true}
                                        className="form-control"
                                        value={form?.tai_khoan === null ? "" : form?.tai_khoan}
                                    />
                                </div> */}

                                <div className="form-group required">
                                    <label>Điện thoại<span className="text-danger">*</span></label>
                                    <input
                                        type="number"
                                        placeholder="Nhập số điện thoại"
                                        className="form-control"
                                        onChange={(e) => setField("so_dien_thoai", e.target.value)}
                                        value={form?.so_dien_thoai === null ? "" : form?.so_dien_thoai}
                                    />
                                    {errors?.so_dien_thoai !== null ? (
                                        <span className="text-danger"> {errors?.so_dien_thoai}</span>
                                    ) : null}
                                </div>
                                <div className="form-group required">
                                    <label>Email<span className="text-danger">*</span></label>
                                    <input
                                        type="text"
                                        placeholder="Nhập email"
                                        className="form-control"
                                        onChange={(e) => setField("email", e.target.value)}
                                        value={form?.email === null ? "" : form?.email}
                                    />
                                    {errors?.email !== null ? (
                                        <span className="text-danger"> {errors?.email}</span>
                                    ) : null}
                                </div>
                                <div className="form-group required">
                                    <label>Vai trò</label>
                                    <input
                                        type="text"
                                        className="form-control"
                                        disabled={true}
                                        value={form?.ten_vai_tro === null ? "" : form?.ten_vai_tro}
                                    />
                                </div>
                            </div>

                            <div className="col-md-6">
                                <div>
                                    <label>Đổi mật khẩu</label>
                                    <br />
                                    <Switch
                                        onChange={() => {
                                            setCheckedMatKhau(!CheckedMatKhau);
                                        }}
                                        checked={CheckedMatKhau}
                                    />
                                </div>
                                {CheckedMatKhau ? <div>
                                    <div className="form-group">
                                        <label>Mật khẩu</label>
                                        <input
                                            className="form-control"
                                            type="password"
                                            placeholder="Nhập mật khẩu"
                                            onChange={(e) => setField("password", e.target.value)}
                                        />
                                        {errors?.password !== null ? (
                                            <span className="text-danger"> {errors?.password}</span>
                                        ) : null}
                                    </div>
                                    <div className="form-group">
                                        <label>Nhập lại mật khẩu</label>
                                        <input
                                            className="form-control"
                                            type="password"
                                            placeholder="Nhập lại mật khẩu"
                                            onChange={(e) => setField("re_password", e.target.value)}
                                        />
                                        {errors?.re_password !== null ? (
                                            <span className="text-danger"> {errors?.re_password}</span>
                                        ) : null}
                                    </div>
                                </div> : null}

                            </div>
                        </div>
                        <Button className='float-right' onClick={(e) => { handleSubmit(e) }} >Cập nhật</Button>
                    </div>
                </div>
            </BlockUi>
        </div >
    );
}
