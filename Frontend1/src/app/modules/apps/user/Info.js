import { DesktopDatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { enAU } from "date-fns/locale";

import { TextField } from "@mui/material";
import { useEffect, useState } from "react";
import { Form } from "react-bootstrap";
import ImageUploading from "react-images-uploading";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import Select from "react-select";
import { PageTitle } from "../../../../_metronic/layout/core";
import { locationActions, selectListNoiCap, selectListTinhThanh } from "../../../redux-module/locations/locationSlice";
import { genderOptions } from "../../../data";
import { compareDate } from "../../../../_metronic/helpers";


export function Info () {
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const [form, setForm] = useState({})
    const [errors, setErrors] = useState({})

    const [ngaySinh, setNgaySinh] = useState();
    const [ngayCap, setNgayCap] = useState();
    const [selectedGioiTinh, setSelectedGioiTinh] = useState(null);
    const [selectedNoiCapCMND, setSelectedNoiCapCMND] = useState();

    const listTinhThanh = useSelector(selectListTinhThanh);
    const listNoiCap = useSelector(selectListNoiCap);

    useEffect(() => {
        dispatch(locationActions.getTinhThanh());
        dispatch(locationActions.getNoiCap());
    }, [])



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

    const usersBreadcrumbs = [
        {
            title: "Trang chủ",
            path: "/",
            isSeparator: false,
            isActive: false,
        },
        {
            title: "",
            path: "",
            isSeparator: true,
            isActive: false,
        },
    ];

    const cardBox = {
        backgroundColor: "#fff",
        backgroundClip: "border-box",
        border: "1px solid #e7eaed",
        padding: "1.5rem",
        marginBottom: "24px",
        borderRadius: "0.5rem",
    };

    const groupStyles = {
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
    };

    const formatGroupLabel = (listTemp) => (
        <div style={groupStyles}>
            <span>{listTemp.ten}</span>
        </div>
    );




    const handleNgaySinh = (newValue) => {
        const content = "Ngày sinh không được lớn hơn ngày hiện tại";
        if (compareDate(newValue, content) === true) {
            setNgaySinh(newValue)
            setField("ngay_sinh", new Date(newValue).getTime());
        }
    };
    const handleNgayCap = (newValue) => {
        const content = "Ngày cấp không được lớn hơn ngày hiện tại";
        if (compareDate(newValue, content) === true) {
            setNgayCap(newValue)
            setField("ngay_cap", new Date(newValue).getTime());
        }
    };
    const handleGioiTinh = () => {

    };

    
    const onSubmit = () => {

    }


    return (
        <LocalizationProvider dateAdapter={AdapterDateFns} locale={enAU}>
            <PageTitle breadcrumbs={usersBreadcrumbs}>
                Thông tin tài khoản
            </PageTitle>
            <div className="card">
                <div className="card-body">
                    <div className="row">
                        <div className="row col-12 d-flex justify-content-between mx-0">
                            <div className="col-md-6">
                                <div style={cardBox}>
                                    <ImageUploading maxNumber={1} dataURLKey="data_url">
                                        {({
                                            imageList,
                                            onImageUpload,
                                            onImageRemove,
                                            isDragging,
                                            dragProps,
                                        }) => (
                                            <div className="form-group">
                                                {imageList.length >= 1 ? (
                                                    imageList.map((image, index) => (
                                                        <div key={index} className="form-group">
                                                            <button
                                                                style={{ fontSize: "14px" }}
                                                                className="btn btn-danger"
                                                                onClick={() => onImageRemove(index)}
                                                            >
                                                                Xóa
                                                            </button>
                                                            <div>
                                                                <img
                                                                    className="mr-2 my-2"
                                                                    src={image.data_url}
                                                                    alt=""
                                                                    width="140"
                                                                />
                                                            </div>
                                                        </div>
                                                    ))
                                                ) : (
                                                    <div>
                                                        <div className="avatar-img">
                                                            <i
                                                                className="fas fa-camera btn-change-avatar"
                                                            // onClick={onImageUpload}
                                                            ></i>
                                                            <img
                                                                src="/media/avatars/default-forum-user.png"
                                                                alt=""
                                                                className="rounded-circle border p-1"
                                                                id="avatar-img"
                                                                width="150"
                                                                height="150"
                                                                backgroundcolor="red"
                                                            />
                                                        </div>
                                                    </div>
                                                )}
                                            </div>
                                        )}
                                    </ImageUploading>
                                    <div>
                                        <label className="font-weight-bold"></label>
                                    </div>
                                    <div className="row">
                                        <div className="col-6">
                                            <div className="form-group">
                                                <label className="fw-bold required fs-6 mb-1">
                                                    Họ
                                                </label>
                                                <Form.Control
                                                    type="text"
                                                    placeholder="Nhập họ"
                                                    style={{
                                                        fontSize: 14,
                                                        fontWeight: 400,
                                                        height: "38px",
                                                    }}
                                                    className="text-uppercase"
                                                    onChange={(e) => {
                                                        setField("ho", e.target.value);
                                                    }}
                                                    value={form.ho != null ? form?.ho : ""}
                                                />
                                                {errors?.ho !== null ? (
                                                    <span className="text-danger"> {errors?.ho}</span>
                                                ) : null}
                                            </div>
                                        </div>
                                        <div className="col-6">
                                            <div className="form-group">
                                                <label className="fw-bold required fs-6 mb-1">
                                                    Tên
                                                </label>
                                                <Form.Control
                                                    type="text"
                                                    placeholder="Nhập tên"
                                                    style={{
                                                        fontSize: 14,
                                                        fontWeight: 400,
                                                        height: "38px",
                                                    }}
                                                    className="text-uppercase"
                                                    onChange={(e) => {
                                                        setField("ten", e.target.value);
                                                    }}
                                                    value={form.ten != null ? form?.ten : ""}
                                                />
                                                {errors?.ten !== null ? (
                                                    <span className="text-danger">
                                                        {" "}
                                                        {errors?.ten}
                                                    </span>
                                                ) : null}
                                            </div>
                                        </div>
                                    </div>

                                    <div className="form-group mt-2">
                                        <label className="fw-bold required fs-6 mb-2">
                                            Ngày sinh
                                        </label>
                                        <DesktopDatePicker
                                            label=" "
                                            inputFormat="dd/MM/yyyy"
                                            onChange={handleNgaySinh}
                                            maxDate={new Date()}
                                            renderInput={(params) => <TextField {...params} />}
                                            value={ngaySinh}
                                        />
                                        {errors?.ngay_sinh !== null ? (
                                            <span className="text-danger">
                                                {errors?.ngay_sinh}
                                            </span>
                                        ) : null}
                                    </div>

                                    <div className="form-group mt-2">
                                        <label className="fw-bold required fs-6 mb-2">
                                            Giới tính
                                        </label>
                                        <Select
                                            key={"id"}
                                            options={genderOptions}
                                            value={selectedGioiTinh}
                                            placeholder="Chọn giới tính"
                                            formatGroupLabel={formatGroupLabel}
                                            onChange={(e) => {
                                                setSelectedGioiTinh(e);
                                            }}
                                        />
                                        {errors?.gioi_tinh !== null ? (
                                            <span className="text-danger">
                                                {" "}
                                                {errors?.gioi_tinh}
                                            </span>
                                        ) : null}
                                    </div>

                                    <div className="form-group mt-2">
                                        <label className="fw-bold required fs-6 mb-2">
                                            CMND/CCCD
                                        </label>
                                        <Form.Control
                                            type="text"
                                            placeholder="Nhập CMND/CCCD"
                                            style={{
                                                fontSize: 14,
                                                fontWeight: 400,
                                                height: "38px",
                                            }}
                                            onChange={(e) => {
                                                setField("ma_cong_dan", e.target.value);
                                            }}
                                            value={
                                                form.ma_cong_dan != null ? form.ma_cong_dan : ""
                                            }
                                        />
                                        {errors?.ma_cong_dan !== null ? (
                                            <span className="text-danger">
                                                {" "}
                                                {errors?.ma_cong_dan}
                                            </span>
                                        ) : null}
                                    </div>

                                    <div className="form-group mt-2">
                                        <label className="fw-bold required fs-6 mb-2">
                                            Ngày cấp
                                        </label>
                                        <DesktopDatePicker
                                            label=" "
                                            inputFormat="dd/MM/yyyy"
                                            onChange={handleNgayCap}
                                            maxDate={new Date()}
                                            renderInput={(params) => <TextField {...params} />}
                                            value={ngayCap}
                                        />
                                        {errors?.ngay_cap !== null ? (
                                            <span className="text-danger">
                                                {errors?.ngay_cap}
                                            </span>
                                        ) : null}
                                    </div>

                                    <div className="form-group mt-2">
                                        <label className="required fw-bold required fs-6 mb-2">
                                            Nơi cấp CMND/CCCD
                                        </label>
                                        <Select
                                            key={"id"}
                                            options={listNoiCap}
                                            value={selectedNoiCapCMND}
                                            placeholder="Chọn nơi cấp CMND/CCCD"
                                            formatGroupLabel={formatGroupLabel}
                                            onChange={(e) => {
                                                setField("noi_cap", e.value);
                                                setSelectedNoiCapCMND(e);
                                            }}
                                        />
                                        {errors?.noi_cap !== null ? (
                                            <span className="text-danger">
                                                {" "}
                                                {errors?.noi_cap}
                                            </span>
                                        ) : null}
                                    </div>

                                    <div className="form-group mt-2">
                                        <label className="fw-bold required fs-6 mb-2">
                                            Số điện thoại{" "}
                                        </label>
                                        <Form.Control
                                            type="text"
                                            placeholder="Nhập số điện thoại"
                                            style={{
                                                fontSize: 14,
                                                fontWeight: 400,
                                                height: "38px",
                                            }}
                                            onChange={(e) => {
                                                setField("dien_thoai", e.target.value);
                                            }}
                                            value={form.dien_thoai != null ? form.dien_thoai : ""}
                                        />
                                        {errors?.dien_thoai !== null ? (
                                            <span className="text-danger">
                                                {" "}
                                                {errors?.dien_thoai}
                                            </span>
                                        ) : null}
                                    </div>

                                    <div className="form-group mt-2">
                                        <label className="fw-bold required fs-6 mb-2">
                                            Email
                                        </label>
                                        <Form.Control
                                            type="text"
                                            placeholder="Nhập email"
                                            style={{
                                                fontSize: 14,
                                                fontWeight: 400,
                                                height: "38px",
                                            }}
                                            onChange={(e) => {
                                                setField("email", e.target.value);
                                            }}
                                            value={form.email != null ? form.email : ""}
                                        />
                                        {errors?.email !== null ? (
                                            <span className="text-danger"> {errors?.email}</span>
                                        ) : null}
                                    </div>
                                </div>
                            </div>

                            <div className="col-md-6">
                                <div style={cardBox}>
                                    <div className="mt-5">
                                        <label className="font-weight-bold text-uppercase">
                                            Hộ khẩu thường trú:
                                        </label>
                                    </div>

                                    <div className="form-group mt-4">
                                        <label className="fw-bold required fs-6 mb-2">
                                            {" "}
                                            Tỉnh/Thành phố{" "}
                                        </label>
                                        <Select
                                            key={"id"}
                                            labelField={"ten"}
                                            placeholder="Chọn tỉnh thành"
                                            searchBy={"tenkhongdau"}
                                            options={listTinhThanh}
                                            onChange={(values) => onChangeTinhThanh(values)}
                                            value={selectedTTTT}
                                        />
                                        {errors?.selectedTTTT !== null &&
                                            !form.tinh_thanh_hien_nay_id ? (
                                            <span className="text-danger">
                                                {errors?.selectedTTTT}
                                            </span>
                                        ) : null}
                                    </div>

                                    <div className="form-group mt-4">
                                        <label className="fw-bold required fs-6 mb-2">
                                            Quận/Huyện
                                        </label>
                                        <Select
                                            key={"id"}
                                            labelField={"ten"}
                                            placeholder="Chọn quận huyện"
                                            options={listQuanHuyen}
                                            onChange={(values) =>
                                                values ? onChangeQuanHuyen(values) : null
                                            }
                                            isDisabled={selectedTTTT ? false : true}
                                            value={selectedQHTT}
                                        />
                                        {errors?.selectedQHTT !== null &&
                                            !form.quan_huyen_hien_nay_id ? (
                                            <span className="text-danger">
                                                {" "}
                                                {errors?.selectedQHTT}
                                            </span>
                                        ) : null}
                                    </div>

                                    <div className="form-group mt-4">
                                        <label className="fw-bold required fs-6 mb-2">
                                            Xã/Phường
                                        </label>
                                        <Select
                                            key={"id"}
                                            labelField={"ten"}
                                            placeholder="Chọn xã phường"
                                            options={listXaPhuong}
                                            onChange={(values) =>
                                                values ? onChangeXaPhuong(values) : null
                                            }
                                            isDisabled={selectedQHTT ? false : true}
                                            value={selectedXPTT}
                                        />
                                        {errors?.selectedXPTT !== null && !form.xa_phuong_hien_nay_id ? (
                                            <span className="text-danger">
                                                {" "}
                                                {errors?.selectedXPTT}
                                            </span>
                                        ) : null}
                                    </div>

                                    <div className="form-group mt-4">
                                        <label className="fw-bold fs-6 mb-2">
                                            Số nhà, tên đường
                                        </label>
                                        <Form.Control
                                            type="text"
                                            placeholder="Nhập số nhà tên đường"
                                            style={{
                                                fontSize: 14,
                                                fontWeight: 400,
                                                height: "38px",
                                            }}
                                            value={form.so_nha_thuong_tru != null ? form.so_nha_thuong_tru : ""}
                                            onChange={(e) => {
                                                setField("so_nha_thuong_tru", e.target.value);
                                            }}
                                        />
                                    </div>

                                    <div style={{ marginTop: "3rem" }}>
                                        <label className="font-weight-bold text-uppercase">
                                            Chỗ ở hiện nay:
                                        </label>
                                    </div>

                                    <div className="form-group mt-5">
                                        <label className="fw-bold required fs-6 mb-2">
                                            Tỉnh/Thành phố{" "}
                                        </label>
                                        <Select
                                            key={"id"}
                                            labelField={"ten"}
                                            placeholder="Chọn tỉnh thành"
                                            searchBy={"tenkhongdau"}
                                            options={listTinhThanhCOHN}
                                            onChange={(values) => onChangeTinhThanhCOHN(values)}
                                            value={selectedTTHN}
                                        />
                                        {errors?.selectedTTHN !== null &&
                                            !form.tinh_thanh_id ? (
                                            <span className="text-danger">
                                                {" "}
                                                {errors?.selectedTTHN}
                                            </span>
                                        ) : null}
                                    </div>

                                    <div className="form-group mt-4">
                                        <label className="fw-bold required fs-6 mb-2">
                                            Quận/Huyện
                                        </label>
                                        <Select
                                            key={"id"}
                                            className={"quan_huyen"}
                                            labelField={"ten"}
                                            placeholder="Chọn quận huyện"
                                            options={listQuanHuyenCOHN}
                                            onChange={(values) =>
                                                values ? onChangeQuanHuyenCOHN(values) : null
                                            }
                                            isDisabled={selectedTTHN ? false : true}
                                            value={selectedQHHN}
                                        />
                                        {errors?.selectedQHHN !== null &&
                                            !form.quan_huyen_id ? (
                                            <span className="text-danger">
                                                {" "}
                                                {errors?.selectedQHHN}
                                            </span>
                                        ) : null}
                                    </div>

                                    <div className="form-group mt-4">
                                        <label className="fw-bold required fs-6 mb-2">
                                            Xã/Phường
                                        </label>
                                        <Select
                                            key={"id"}
                                            labelField={"ten"}
                                            placeholder="Chọn xã phường"
                                            options={listXaPhuongCOHN}
                                            onChange={(values) =>
                                                values ? onChangeXaPhuongCOHN(values) : null
                                            }
                                            isDisabled={selectedQHHN ? false : true}
                                            value={selectedXPHN}
                                        />
                                        {errors?.selectedXPHN !== null &&
                                            !form.xa_phuong_id ? (
                                            <span className="text-danger">
                                                {" "}
                                                {errors?.selectedXPHN}
                                            </span>
                                        ) : null}
                                    </div>

                                    <div className="form-group mt-4">
                                        <label className="fw-bold fs-6 mb-2">
                                            Số nhà, tên đường
                                        </label>
                                        <Form.Control
                                            type="text"
                                            placeholder="Nhập số nhà tên đường"
                                            style={{
                                                fontSize: 14,
                                                fontWeight: 400,
                                                height: "38px",
                                            }}
                                            value={
                                                form.so_nha === null
                                                    ? ""
                                                    : form.so_nha
                                            }
                                            onChange={(e) => {
                                                setField("so_nha", e.target.value);
                                            }}
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="col-12 text-center mt-5">
                            <button
                                className="btn btn-secondary btn-trolai text-uppercase"
                                onClick={() => navigate(-1)}
                            >
                                Trở về
                            </button>
                            <button
                                onClick={(e) => {
                                    onSubmit(e);
                                }}
                                className="btn btn-primary text-uppercase"
                                style={{ marginLeft: "10px" }}
                            >
                                Lưu thông tin
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </LocalizationProvider>
    )
}