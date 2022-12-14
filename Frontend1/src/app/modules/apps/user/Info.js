import { DesktopDatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { enAU } from "date-fns/locale";

import { TextField } from "@mui/material";
import axios from "axios";
import { useEffect, useState } from "react";
import { Form } from "react-bootstrap";
import ImageUploading from "react-images-uploading";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import Select from "react-select";
import { toast } from "react-toastify";
import { compareDate } from "../../../../_metronic/helpers";
import { PageTitle } from "../../../../_metronic/layout/core";
import api from "../../../configs/api";
import { genderOptions } from "../../../data";
import { authActions, authSlice, selectCurrentUser } from "../../../redux-module/auth/authSlice";


export function Info() {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const thongTinCaNhan = useSelector(selectCurrentUser);

    const [form, setForm] = useState({})
    const [errors, setErrors] = useState({})
    const [isLoading, setIsLoading] = useState(false)

    const [ngaySinh, setNgaySinh] = useState();
    const [ngayCap, setNgayCap] = useState();
    const [selectedGioiTinh, setSelectedGioiTinh] = useState(null);
    const [selectedNoiCapCMND, setSelectedNoiCapCMND] = useState();

    const [ListNoiCap, setListNoiCap] = useState([]);
    const [ListTinhThanh, setListTinhThanh] = useState([]);
    const [ListQuanHuyenTT, setListQuanHuyenTT] = useState([]);
    const [ListXaPhuongTT, setListXaPhuongTT] = useState([]);
    const [ListQuanHuyenHN, setListQuanHuyenHN] = useState([]);
    const [ListXaPhuongHN, setListXaPhuongHN] = useState([]);

    const [TinhThanhTTSelected, setTinhThanhTTSelected] = useState(null);
    const [QuanHuyenTTSelected, setQuanHuyenTTSelected] = useState(null);
    const [XaPhuongTTSelected, setXaPhuongTTSelected] = useState(null);

    const [TinhThanhHNSelected, setTinhThanhHNSelected] = useState(null);
    const [QuanHuyenHNSelected, setQuanHuyenHNSelected] = useState(null);
    const [XaPhuongHNSelected, setXaPhuongHNSelected] = useState(null);


    useEffect(() => {
        getCATinhThanh();
        handleGioiTinh(3);
        getListTinhThanh();
        setForm(thongTinCaNhan)
        setSelectedNoiCapCMND({
            label: thongTinCaNhan?.noi_cap,
            value: "tempNoicap",
        });
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

    useEffect(() => {
        if (ListTinhThanh && ListTinhThanh.length > 0) {
            if (form?.tinh_thanh_thuong_tru_id) {
                onChangeTinhThanh("thuongtru", ListTinhThanh.find((e) => e.value === form?.tinh_thanh_thuong_tru_id));
            }
            if (form?.tinh_thanh_hien_nay_id) {
                onChangeTinhThanh("hiennay", ListTinhThanh.find((e) => e.value === form?.tinh_thanh_hien_nay_id));
            }
        }
    }, [ListTinhThanh, form?.tinh_thanh_thuong_tru_id, form?.tinh_thanh_hien_nay_id]);

    useEffect(() => {
        if (ListQuanHuyenTT && ListQuanHuyenTT.length > 0) {
            if (form?.quan_huyen_thuong_tru_id) {
                onChangeQuanHuyen("thuongtru", ListQuanHuyenTT.find((e) => e.value === form?.quan_huyen_thuong_tru_id));
            }
        }
        if (ListQuanHuyenHN && ListQuanHuyenHN.length > 0) {
            if (form?.quan_huyen_hien_nay_id) {
                onChangeQuanHuyen("hiennay", ListQuanHuyenHN.find((e) => e.value === form?.quan_huyen_hien_nay_id));
            }
        }
    }, [ListQuanHuyenTT, ListQuanHuyenHN, form?.quan_huyen_thuong_tru_id, form?.quan_huyen_hien_nay_id]);

    useEffect(() => {
        if (ListXaPhuongTT && ListXaPhuongTT.length > 0) {
            if (form?.xa_phuong_thuong_tru_id) {
                onChangeXaPhuong("thuongtru", ListXaPhuongTT.find((e) => e.value === form?.xa_phuong_thuong_tru_id));
            }
        }
        if (ListXaPhuongHN && ListXaPhuongHN.length > 0) {
            if (form?.xa_phuong_hien_nay_id) {
                onChangeXaPhuong("hiennay", ListXaPhuongHN.find((e) => e.value === form?.xa_phuong_hien_nay_id));
            }
        }
    }, [ListXaPhuongTT, ListXaPhuongHN, form?.xa_phuong_thuong_tru_id, form?.xa_phuong_hien_nay_id]);


    const onChangeTinhThanh = async (type, value) => {
        if (value) {
            if (type === "thuongtru") {
                setField("tinh_thanh_thuong_tru_id", value?.id);
                getListQuanHuyen(type, value)
                setTinhThanhTTSelected(value);
                setQuanHuyenTTSelected(null);
                setXaPhuongTTSelected(null);
            }
            if (type === "hiennay") {
                setField("tinh_thanh_hien_nay_id", value?.id);
                getListQuanHuyen(type, value)
                setTinhThanhHNSelected(value);
                setQuanHuyenHNSelected(null);
                setXaPhuongHNSelected(null);
            }
        }
    }

    const onChangeQuanHuyen = async (type, value) => {
        if (value) {
            if (type === "thuongtru") {
                setField("quan_huyen_thuong_tru_id", value?.id);
                getListXaPhuong(type, value);
                setQuanHuyenTTSelected(value);
                setXaPhuongTTSelected(null);
            }
            if (type === "hiennay") {
                setField("quan_huyen_hien_nay_id", value?.id);
                getListXaPhuong(type, value);
                setQuanHuyenHNSelected(value);
                setXaPhuongHNSelected(null);
            }
        }
    }

    const onChangeXaPhuong = (type, value) => {
        if (value) {
            if (type === "thuongtru") {
                setField("xa_phuong_thuong_tru_id", value.id);
                setXaPhuongTTSelected(value);
            }
            if (type === "hiennay") {
                setField("xa_phuong_hien_nay_id", value.id);
                setXaPhuongHNSelected(value);
            }
        }
    }

    const getListTinhThanh = () => {
        axios
            .get(api.API_TINH_THANH_PUBLIC)
            .then(({ data }) => {
                const resultsTinhThanh = data?.results;
                resultsTinhThanh.forEach((e) => {
                    e.label = e.ten;
                    e.value = e.id;
                })
                setListTinhThanh(resultsTinhThanh)
            })
            .catch((error) => {
            })
            .finally(() => { });
    }

    const getListQuanHuyen = (type, value) => {
        axios
            .get(api.API_QUAN_HUYEN_PUBLIC + value?.id + "?per_page=100")
            .then(({ data }) => {
                const resultsQuanHuyen = data?.results;
                resultsQuanHuyen.forEach((e) => {
                    e.label = e.ten;
                    e.value = e.id;
                });
                if (type === "thuongtru") setListQuanHuyenTT(resultsQuanHuyen)
                if (type === "hiennay") setListQuanHuyenHN(resultsQuanHuyen)
            })
            .catch((error) => {
            });
    }

    const getListXaPhuong = (type, value) => {
        axios
            .get(api.API_XA_PHUONG_PUBLIC + value?.id + "?per_page=100")
            .then(({ data }) => {
                const resultsXaPhuong = data?.results;
                resultsXaPhuong.forEach((e) => {
                    e.label = e.ten;
                    e.value = e.id;
                });
                if (type === "thuongtru") setListXaPhuongTT(resultsXaPhuong)
                if (type === "hiennay") setListXaPhuongHN(resultsXaPhuong)
            })
            .catch((error) => {
            });
    }

    const getCATinhThanh = () => {
        return new Promise((resolve, reject) => {
            axios
                .get(api.API_NOI_CAP_PUBLIC)
                .then(async ({ data }) => {
                    setListNoiCap(data?.results)
                })
                .catch((error) => {
                })
        })
    }

    const handleGioiTinh = (id) => {
        let tempGioiTinh = genderOptions.find((e) => e.value == id);
        setSelectedGioiTinh(tempGioiTinh);
    };


    const usersBreadcrumbs = [
        {
            title: "Trang ch???",
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


    const handleNgaySinh = (newValue) => {
        const content = "Ng??y sinh kh??ng ???????c l???n h??n ng??y hi???n t???i";
        if (compareDate(newValue, content) === true) {
            setNgaySinh(newValue)
            setField("ngay_sinh", new Date(newValue).getTime());
        }
    };
    const handleNgayCap = (newValue) => {
        const content = "Ng??y c???p kh??ng ???????c l???n h??n ng??y hi???n t???i";
        if (compareDate(newValue, content) === true) {
            setNgayCap(newValue)
            setField("ngay_cap", new Date(newValue).getTime());
        }
    };

    const findFormErrors = () => {
        const numCheck = /^\d+$/;
        const { ho, ten, ngay_sinh, ma_cong_dan, ngay_cap, dien_thoai, email } =
            form;
        const newErrors = {};

        if (!ho || ho === "") newErrors.ho = "H??? kh??ng ???????c b??? tr???ng!";
        if (!ten || ten === "") newErrors.ten = "T??n kh??ng ???????c b??? tr???ng!";
        if (!ma_cong_dan || ma_cong_dan === "")
            newErrors.ma_cong_dan = "CMND/CCCD kh??ng ???????c b??? tr???ng!";

        if (dien_thoai) {
            if (numCheck.test(dien_thoai) === false || dien_thoai.length !== 10) {
                newErrors.dien_thoai = "Sai ?????nh d???ng s??? ??i???n tho???i!";
            }
        }

        if (ma_cong_dan) {
            if (
                numCheck.test(ma_cong_dan) === false ||
                (ma_cong_dan.length !== 9 && ma_cong_dan.length !== 12)
            ) {
                newErrors.ma_cong_dan = "Sai ?????nh d???ng CMND/CCCD!";
            }
        }

        if (!dien_thoai || dien_thoai === "")
            newErrors.dien_thoai = "S??? ??i???n tho???i kh??ng ???????c b??? tr???ng!";

        if (!email || email === "") newErrors.email = "Email kh??ng ???????c b??? tr???ng!";

        if (!ngay_sinh) newErrors.ngay_sinh = "Ng??y sinh kh??ng ???????c b??? tr???ng!";
        else if (ngay_sinh > new Date().getTime())
            newErrors.ngay_sinh = "Ng??y sinh kh??ng h???p l???!";
        if (!ngay_cap)
            newErrors.ngay_cap = "Ng??y c???p CMND/CCCD kh??ng ???????c b??? tr???ng!";
        else if (ngay_cap > new Date().getTime())
            newErrors.ngay_cap = "Ng??y c???p CMND/CCCD kh??ng h???p l???!";

        if (!selectedGioiTinh) {
            newErrors.gioi_tinh = "Gi???i t??nh kh??ng ???????c b??? tr???ng!";
        }
        if (!selectedNoiCapCMND) {
            newErrors.noi_cap = "N??i c???p CMND/CCCD kh??ng ???????c b??? tr???ng!";
        }

        if (!TinhThanhTTSelected) {
            newErrors.selectedTTTT = "T???nh th??nh th?????ng tr?? kh??ng ???????c b??? tr???ng!";
        }
        if (!QuanHuyenTTSelected) {
            newErrors.selectedQHTT = "Qu???n huy???n th?????ng tr?? kh??ng ???????c b??? tr???ng!";
        }
        if (!XaPhuongTTSelected) {
            newErrors.selectedXPTT = "X?? ph?????ng th?????ng tr?? kh??ng ???????c b??? tr???ng!";
        }
        if (!TinhThanhHNSelected) {
            newErrors.selectedTTHN = "T???nh th??nh hi???n nay kh??ng ???????c b??? tr???ng!";
        }
        if (!QuanHuyenHNSelected) {
            newErrors.selectedQHHN = "Qu???n huy???n hi???n nay kh??ng ???????c b??? tr???ng!";
        }
        if (!XaPhuongHNSelected) {
            newErrors.selectedXPHN = "X?? ph?????ng hi???n nay kh??ng ???????c b??? tr???ng!";
        }

        return newErrors;
    };


    const onSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true)

        const newErrors = findFormErrors();
        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
            setIsLoading(false);
            toast.error("Vui l??ng nh???p ?????y ????? th??ng tin tr?????c khi c???p nh???t", {
                position: "top-right",
                autoClose: 2000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
                toastId: "error",
            });
        } else {
            const {
                ho,
                ten,
                ngay_sinh,
                ma_cong_dan,
                ngay_cap,
                dien_thoai,
                email,
                so_nha_hien_nay,
                so_nha_thuong_tru,
            } = form;

            const json = new FormData();

            await json.append("ho", ho.toUpperCase());
            await json.append("ten", ten.toUpperCase());
            await json.append("ngay_sinh", ngay_sinh);
            await json.append("gioi_tinh", selectedGioiTinh ? selectedGioiTinh.value : null);
            await json.append("ma_cong_dan", ma_cong_dan);
            await json.append("ngay_cap", ngay_cap);
            await json.append("noi_cap", selectedNoiCapCMND ? selectedNoiCapCMND.label : null);
            await json.append("dien_thoai", dien_thoai);
            await json.append("email", email);
            await json.append("tinh_thanh_thuong_tru_id", TinhThanhTTSelected ? TinhThanhTTSelected.value : null);
            await json.append("quan_huyen_thuong_tru_id", QuanHuyenTTSelected ? QuanHuyenTTSelected.value : null);
            await json.append("xa_phuong_thuong_tru_id", XaPhuongTTSelected ? XaPhuongTTSelected.value : null);
            await json.append("so_nha_thuong_tru", so_nha_thuong_tru ? so_nha_thuong_tru : "");
            await json.append("tinh_thanh_hien_nay_id", TinhThanhHNSelected ? TinhThanhHNSelected.value : null);
            await json.append("quan_huyen_hien_nay_id", QuanHuyenHNSelected ? QuanHuyenHNSelected.value : null);
            await json.append("xa_phuong_hien_nay_id", XaPhuongHNSelected ? XaPhuongHNSelected.value : null);
            await json.append("so_nha_hien_nay", so_nha_hien_nay ? so_nha_hien_nay : "");


            axios
                .put(api.API_QUAN_LY_NGUOI_DUNG_UPDATE + "/" + thongTinCaNhan.id, json)
                .then(({ data }) => {
                    toast.success("C???p nh???t th??ng tin th??nh c??ng", {
                        position: "top-right",
                        autoClose: 2000,
                        hideProgressBar: false,
                        closeOnClick: true,
                        pauseOnHover: true,
                        draggable: true,
                        progress: undefined,
                        toastId: "success",
                    });
                dispatch(authActions.setCurrentUser(data?.results))
                })
                .catch((error) => {
                    toast.error(error?.data?.errors, {
                        position: "top-right",
                        autoClose: 2000,
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
    }
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


    return (
        <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={enAU}>
            <PageTitle breadcrumbs={usersBreadcrumbs}>
                Th??ng tin t??i kho???n
            </PageTitle>
            <div className="card">
                <div className="card-body">
                    <div className="row">
                        <div className="row col-12 d-flex justify-content-between mx-0">
                            <div className="col-md-6">
                                <div style={cardBox}>
                                    <ImageUploading maxNumber={1} dataURLKey="data_url">
                                        {({ imageList, onImageUpload, onImageRemove, isDragging, dragProps }) => (
                                            <div className="form-group">
                                                {imageList.length >= 1 ? (
                                                    imageList.map((image, index) => (
                                                        <div key={index} className="form-group">
                                                            <button className="btn btn-danger" style={{ fontSize: "14px" }} onClick={() => onImageRemove(index)}> X??a </button>
                                                            <div>
                                                                <img className="mr-2 my-2" alt="" src={image.data_url} width="140" />
                                                            </div>
                                                        </div>
                                                    ))
                                                ) : (
                                                    <div>
                                                        <div className="avatar-img">
                                                            <i className="fas fa-camera btn-change-avatar"></i>
                                                            <img
                                                                className="rounded-circle border p-1"
                                                                alt=""
                                                                src="/media/avatars/default-forum-user.png"
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
                                                <label className="fw-bold required fs-6 mb-1"> H??? </label>
                                                <Form.Control
                                                    type="text"
                                                    placeholder="Nh???p h???"
                                                    style={{ fontSize: 14, fontWeight: 400, height: "38px" }}
                                                    className="text-uppercase"
                                                    onChange={(e) => setField("ho", e.target.value)}
                                                    value={form.ho != null ? form?.ho : ""}
                                                />
                                                {errors?.ho !== null ? <span className="text-danger">{errors?.ho}</span> : null}
                                            </div>
                                        </div>
                                        <div className="col-6">
                                            <div className="form-group">
                                                <label className="fw-bold required fs-6 mb-1"> T??n </label>
                                                <Form.Control
                                                    type="text"
                                                    placeholder="Nh???p t??n"
                                                    style={{ fontSize: 14, fontWeight: 400, height: "38px" }}
                                                    className="text-uppercase"
                                                    onChange={(e) => setField("ten", e.target.value)}
                                                    value={form.ten != null ? form?.ten : ""}
                                                />
                                                {errors?.ten !== null ? <span className="text-danger">{errors?.ten}</span> : null}
                                            </div>
                                        </div>
                                    </div>

                                    <div className="form-group mt-2">
                                        <label className="fw-bold required fs-6 mb-2"> Ng??y sinh </label>
                                        <DesktopDatePicker
                                            label=" "
                                            inputFormat="dd/MM/yyyy"
                                            onChange={handleNgaySinh}
                                            maxDate={new Date()}
                                            renderInput={(params) => <TextField {...params} />}
                                            value={ngaySinh}
                                        />
                                        {errors?.ngay_sinh !== null ? <span className="text-danger">{errors?.ngay_sinh}</span> : null}
                                    </div>

                                    <div className="form-group mt-2">
                                        <label className="fw-bold required fs-6 mb-2"> Gi???i t??nh </label>
                                        <Select
                                            key={"id"}
                                            options={genderOptions}
                                            value={selectedGioiTinh}
                                            placeholder="Ch???n gi???i t??nh"
                                            formatGroupLabel={formatGroupLabel}
                                            onChange={(e) => {
                                                setField("gioi_tinh", e.value)
                                                setSelectedGioiTinh(e);
                                            }}
                                        />
                                        {errors?.gioi_tinh !== null ? <span className="text-danger">{errors?.gioi_tinh}</span> : null}
                                    </div>

                                    <div className="form-group mt-2">
                                        <label className="fw-bold required fs-6 mb-2"> CMND/CCCD </label>
                                        <Form.Control
                                            type="text"
                                            placeholder="Nh???p CMND/CCCD"
                                            style={{ fontSize: 14, fontWeight: 400, height: "38px" }}
                                            onChange={(e) => setField("ma_cong_dan", e.target.value)}
                                            value={form.ma_cong_dan != null ? form.ma_cong_dan : ""}
                                        />
                                        {errors?.ma_cong_dan !== null ? <span className="text-danger">{errors?.ma_cong_dan}</span> : null}
                                    </div>

                                    <div className="form-group mt-2">
                                        <label className="fw-bold required fs-6 mb-2"> Ng??y c???p </label>
                                        <DesktopDatePicker
                                            label=" "
                                            inputFormat="dd/MM/yyyy"
                                            onChange={handleNgayCap}
                                            maxDate={new Date()}
                                            renderInput={(params) => <TextField {...params} />}
                                            value={ngayCap}
                                        />
                                        {errors?.ngay_cap !== null ? <span className="text-danger">{errors?.ngay_cap}</span> : null}
                                    </div>

                                    <div className="form-group mt-2">
                                        <label className="required fw-bold required fs-6 mb-2"> N??i c???p CMND/CCCD </label>
                                        <Select
                                            key={"id"}
                                            options={ListNoiCap}
                                            value={selectedNoiCapCMND}
                                            placeholder="Ch???n n??i c???p CMND/CCCD"
                                            formatGroupLabel={formatGroupLabel}
                                            onChange={(e) => {
                                                setField("noi_cap", e.value);
                                                setSelectedNoiCapCMND(e);
                                            }}
                                        />
                                        {errors?.noi_cap !== null ? <span className="text-danger">{errors?.noi_cap}</span> : null}
                                    </div>

                                    <div className="form-group mt-2">
                                        <label className="fw-bold required fs-6 mb-2"> S??? ??i???n tho???i </label>
                                        <Form.Control
                                            type="text"
                                            placeholder="Nh???p s??? ??i???n tho???i"
                                            style={{ fontSize: 14, fontWeight: 400, height: "38px" }}
                                            onChange={(e) => setField("dien_thoai", e.target.value)}
                                            value={form.dien_thoai != null ? form.dien_thoai : ""}
                                        />
                                        {errors?.dien_thoai !== null ? <span className="text-danger">{errors?.dien_thoai}</span> : null}
                                    </div>

                                    <div className="form-group mt-2">
                                        <label className="fw-bold required fs-6 mb-2"> Email </label>
                                        <Form.Control
                                            type="text"
                                            placeholder="Nh???p email"
                                            style={{ fontSize: 14, fontWeight: 400, height: "38px" }}
                                            onChange={(e) => setField("email", e.target.value)}
                                            value={form.email != null ? form.email : ""}
                                        />
                                        {errors?.email !== null ? <span className="text-danger">{errors?.email}</span> : null}
                                    </div>
                                </div>
                            </div>

                            <div className="col-md-6">
                                <div style={cardBox}>
                                    <div className="mt-5">
                                        <label className="font-weight-bold text-uppercase">
                                            H??? kh???u th?????ng tr??:
                                        </label>
                                    </div>

                                    <div className="form-group mt-4">
                                        <label className="fw-bold required fs-6 mb-2"> T???nh/Th??nh ph??? </label>
                                        <Select
                                            key={"id"}
                                            labelField={"ten"}
                                            placeholder="Ch???n t???nh th??nh"
                                            searchBy={"tenkhongdau"}
                                            options={ListTinhThanh}
                                            onChange={(values) => onChangeTinhThanh("thuongtru", values)}
                                            value={TinhThanhTTSelected}
                                        />
                                        {errors?.selectedTTTT !== null && !form.tinh_thanh_thuong_tru_id ? <span className="text-danger">{errors?.selectedTTTT}</span> : null}
                                    </div>

                                    <div className="form-group mt-4">
                                        <label className="fw-bold required fs-6 mb-2"> Qu???n/Huy???n </label>
                                        <Select
                                            key={"id"}
                                            labelField={"ten"}
                                            placeholder="Ch???n qu???n huy???n"
                                            options={ListQuanHuyenTT}
                                            onChange={(values) => onChangeQuanHuyen("thuongtru", values)}
                                            isDisabled={TinhThanhTTSelected ? false : true}
                                            value={QuanHuyenTTSelected}
                                        />
                                        {errors?.selectedQHTT !== null && !form.quan_huyen_thuong_tru_id ? <span className="text-danger">{errors?.selectedQHTT}</span> : null}
                                    </div>

                                    <div className="form-group mt-4">
                                        <label className="fw-bold required fs-6 mb-2"> X??/Ph?????ng </label>
                                        <Select
                                            key={"id"}
                                            labelField={"ten"}
                                            placeholder="Ch???n x?? ph?????ng"
                                            options={ListXaPhuongTT}
                                            onChange={(values) => onChangeXaPhuong("thuongtru", values)}
                                            isDisabled={QuanHuyenTTSelected ? false : true}
                                            value={XaPhuongTTSelected}
                                        />
                                        {errors?.selectedXPTT !== null && !form.xa_phuong_thuong_tru_id ? <span className="text-danger">{errors?.selectedXPTT}</span> : null}
                                    </div>

                                    <div className="form-group mt-4">
                                        <label className="fw-bold fs-6 mb-2"> S??? nh??, t??n ???????ng </label>
                                        <Form.Control
                                            type="text"
                                            placeholder="Nh???p s??? nh?? t??n ???????ng"
                                            style={{ fontSize: 14, fontWeight: 400, height: "38px" }}
                                            value={form.so_nha_thuong_tru != null ? form.so_nha_thuong_tru : ""}
                                            onChange={(e) => setField("so_nha_thuong_tru", e.target.value)}
                                        />
                                    </div>

                                    <div style={{ marginTop: "3rem" }}>
                                        <label className="font-weight-bold text-uppercase">
                                            Ch??? ??? hi???n nay:
                                        </label>
                                    </div>

                                    <div className="form-group mt-5">
                                        <label className="fw-bold required fs-6 mb-2"> T???nh/Th??nh ph??? </label>
                                        <Select
                                            key={"id"}
                                            labelField={"ten"}
                                            placeholder="Ch???n t???nh th??nh"
                                            searchBy={"tenkhongdau"}
                                            options={ListTinhThanh}
                                            onChange={(values) => onChangeTinhThanh("hiennay", values)}
                                            value={TinhThanhHNSelected}
                                        />
                                        {errors?.selectedTTHN !== null && !form.tinh_thanh_id ? <span className="text-danger">{errors?.selectedTTHN}</span> : null}
                                    </div>

                                    <div className="form-group mt-4">
                                        <label className="fw-bold required fs-6 mb-2"> Qu???n/Huy???n </label>
                                        <Select
                                            key={"id"}
                                            className={"quan_huyen"}
                                            labelField={"ten"}
                                            placeholder="Ch???n qu???n huy???n"
                                            options={ListQuanHuyenHN}
                                            onChange={(values) => onChangeQuanHuyen("hiennay", values)}
                                            isDisabled={TinhThanhHNSelected ? false : true}
                                            value={QuanHuyenHNSelected}
                                        />
                                        {errors?.selectedQHHN !== null && !form.quan_huyen_id ? <span className="text-danger">{errors?.selectedQHHN}</span> : null}
                                    </div>

                                    <div className="form-group mt-4">
                                        <label className="fw-bold required fs-6 mb-2"> X??/Ph?????ng </label>
                                        <Select
                                            key={"id"}
                                            labelField={"ten"}
                                            placeholder="Ch???n x?? ph?????ng"
                                            options={ListXaPhuongHN}
                                            onChange={(values) => onChangeXaPhuong("hiennay", values)}
                                            isDisabled={QuanHuyenHNSelected ? false : true}
                                            value={XaPhuongHNSelected}
                                        />
                                        {errors?.selectedXPHN !== null && !form.xa_phuong_id ? <span className="text-danger">{errors?.selectedXPHN}</span> : null}
                                    </div>

                                    <div className="form-group mt-4">
                                        <label className="fw-bold fs-6 mb-2">
                                            S??? nh??, t??n ???????ng
                                        </label>
                                        <Form.Control
                                            type="text"
                                            placeholder="Nh???p s??? nh?? t??n ???????ng"
                                            style={{ fontSize: 14, fontWeight: 400, height: "38px" }}
                                            value={form.so_nha_hien_nay === null ? "" : form.so_nha_hien_nay}
                                            onChange={(e) => setField("so_nha_hien_nay", e.target.value)}
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>

                        {isLoading ? (
                            <div className="col-12 text-center mt-5">

                                <button className="btn btn-link">
                                    <span
                                        className="indicator-progress"
                                        style={{ display: "block" }}
                                    >
                                        Vui l??ng ch???...
                                        <span className="spinner-border spinner-border-sm align-middle ms-2"></span>
                                    </span>
                                </button>
                            </div>
                        ) : (
                            <div className="col-12 text-center mt-5">
                                <button
                                    className="btn btn-secondary btn-trolai text-uppercase"
                                    onClick={() => navigate(-1)}
                                >
                                    Tr??? v???
                                </button>
                                <button
                                    onClick={(e) => {
                                        onSubmit(e);
                                    }}
                                    className="btn btn-primary text-uppercase"
                                    style={{ marginLeft: "10px" }}
                                >
                                    L??u th??ng tin
                                </button>
                            </div>
                        )}

                    </div>
                </div>
            </div >
        </LocalizationProvider >
    )
}