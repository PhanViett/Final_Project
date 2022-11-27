import { DesktopDatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { enAU } from "date-fns/locale";

import { TextField } from "@mui/material";
import axios from "axios";
import moment from "moment";
import { useEffect, useState } from "react";
import { Form } from "react-bootstrap";
import { useSelector } from "react-redux";
import Select from "react-select";
import api from "../../../configs/api";
import { genderOptions, levelOptions, ynOptions } from "../../../data";
import { selectCurrentUser } from "../../../redux-module/auth/authSlice";
import { toast } from "react-toastify";


export function Diagnostic() {
    const currentUser = useSelector(selectCurrentUser)

    const [form, setForm] = useState({});
    const [errors, setErrors] = useState({});
    const [isLoading, setIsLoading] = useState(false);

    const [tuoi, setTuoi] = useState(new Date());
    const [gioiTinh, setGioiTinh] = useState();
    const [chol, setChol] = useState();
    const [gluc, setGluc] = useState();
    const [alco, setAlco] = useState();
    const [smoke, setSmoke] = useState();
    const [activ, setActiv] = useState();
    const [isProgressing, setIsProgressing] = useState(true);
    const [isUpdate, setIsUpdate] = useState(false);

    const inputStyle = { fontSize: 14, fontWeight: 400, height: 40 }

    useEffect(() => {
        getUserInfo();
    }, [])
    useEffect(() => {
        console.log(form);
    }, [form])
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


    const getUserInfo = () => {
        setIsLoading(true)
        axios
            .get(api.API_QUAN_LY_NGUOI_DUNG_INFO + "/" + currentUser.id)
            .then(({ data }) => {
                if (data) {
                    setTuoi(data?.ngay_sinh)
                    handleGioiTinh(data?.gioi_tinh)
                    handleStatics(data)
                    setForm(data)
                }
            })
            .catch((error) => {
                toast.error(error?.response?.data?.msg, {
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
            })
    }

    const handleGioiTinh = (value) => {
        let gioi_tinh = genderOptions.find((e) => e.value === value);
        setField("gioi_tinh", value);
        setGioiTinh(gioi_tinh);
    }

    const handleStatics = (value) => {
        if (value?.chol) {
            let chol = levelOptions.find((e) => e.value === value?.chol);
            if (chol) {
                setChol(chol)
            }
        }
        if (value?.gluc) {
            let gluc = levelOptions.find((e) => e.value === value?.gluc);
            if (gluc) {
                setGluc(gluc)
            }
        }
        if (value?.smoke) {
            let smoke = ynOptions.find((e) => e.value === value?.smoke);
            if (smoke) {
                setSmoke(smoke)
            }
        }
        if (value?.alco) {
            let alco = ynOptions.find((e) => e.value === value?.alco);
            if (alco) {
                setAlco(alco)
            }
        }
        if (value?.active) {
            let active = ynOptions.find((e) => e.value === value?.active);
            if (active) {
                setActiv(active)
            }
        }
    }

    const handleSelectes = (type, data) => {
        if (type === "chol") {
            setChol(data)
            setField("chol", data.value)
        } else if (type === "gluc") {
            setGluc(data)
            setField("gluc", data.value)
        } else if (type === "smoke") {
            setSmoke(data)
            setField("smoke", data.value)
        } else if (type === "alco") {
            setAlco(data)
            setField("alco", data.value)
        } else if (type === "activ") {
            setActiv(data)
            setField("active", data.value)
        }
    }

    const formValidation = () => {
        const newErrors = {};
        const { ho_ten, weight, height } = form;

        if (!ho_ten || ho_ten === "") newErrors.tuoi = "Họ tên không được bỏ trống!";
        if (!tuoi || tuoi <= 0) newErrors.tuoi = "Ngày sinh không được bỏ trống!";
        if (!gioiTinh) newErrors.gioiTinh = "Giới tính không được bỏ trống!"
        if (!weight || weight === "") newErrors.weight = "Cân nặng không được bỏ trống!"
        if (!height || height === "") newErrors.height = "Chiều cao không được bỏ trống!"
        if (!chol) newErrors.chol = "Mức độ cholesterol không được bỏ trống!"
        if (!gluc) newErrors.gluc = "Mức độ glucose không được bỏ trống!"
        if (!smoke) newErrors.smoke = "Vui lòng chọn câu trả lời!"
        if (!alco) newErrors.alco = "Vui lòng chọn câu trả lời!"
        if (!activ) newErrors.activ = "Vui lòng chọn câu trả lời!"

        return newErrors;
    }


    const handleSubmit = () => {
        const newError = formValidation();

        if (Object.keys(newError).length > 0) {
            setErrors(newError);
            console.log(newError);
        } else {
            setIsLoading(true);

            const diff = new Date().getTime() - new Date(tuoi).getTime();
            const day_count = Math.round(diff / (1000 * 3600 * 24))

            const json = {
                "ho_ten": form?.ho_ten,
                "ngay_sinh": form?.ngay_sinh,
                "tuoi": day_count,
                "gioi_tinh": form?.gioi_tinh,
                "height": form?.height,
                "weight": form?.weight,
                "chol": form?.chol,
                "gluc": form?.gluc,
                "smoke": form?.smoke,
                "alco": form?.alco,
                "active": form?.active
            }
            axios
                .put(api.API_QUAN_LY_NGUOI_DUNG_STATIC + "/" + currentUser.id, json)
                .then((data) => {

                })
                .catch((error) => {
                    toast.error(error?.response?.data?.msg, {
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
                })
        }
    }
    const handleTuoi = (value) => {
        if (typeof value === "number") {
            setTuoi(value);
        } else if (typeof value === "object") {
            const diff = new Date().getTime() - new Date(value).getTime();
            setField("tuoi", )
            setTuoi(value)
        }
    }
    return (
        <LocalizationProvider dateAdapter={AdapterDateFns} locale={enAU}>
            <div>
                <div className="card-box" style={{ padding: "32px" }}>
                    {isProgressing === true ?
                        <div style={{ height: "78vh" }}>
                            <div className="row">
                                <div className="col-12 mb-8">
                                    <h4 className="fw-bold">CHẨN ĐOÁN TÌNH TRẠNG</h4>
                                </div>

                                <div className="col-9 mt-8">
                                    <h5 className="fw-bold">Thông tin hiện tại</h5>
                                </div>

                                <div className="col-3 mb-10 text-end">
                                    {isUpdate === false ?
                                        <button className="btn btn-primary py-0" style={{ fontSize: "13px", height: "38px", width: "130px" }} onClick={() => setIsUpdate(true)}>
                                            <i className="fas fa-edit me-1" style={{ fontSize: "12px" }}></i>Cập nhật
                                        </button>
                                        :
                                        <div>
                                            <button className="btn btn-success py-0 me-2" style={{ fontSize: "13px", height: "38px", width: "130px" }} onClick={() => {handleSubmit();} }>
                                                <i className="fas fa-save me-1" style={{ fontSize: "12px" }}></i>Lưu
                                            </button>
                                            <button className="btn btn-secondary py-0 ms-2" style={{ fontSize: "13px", height: "38px", width: "130px" }} onClick={() => setIsUpdate(false)}>
                                                <i className="fas fa-arrow-right me-1" style={{ fontSize: "12px" }}></i>Quay lại
                                            </button>
                                        </div>
                                    }

                                </div>


                                <div className="row mx-1 mb-4">
                                    <div className="col-3">
                                        <span className="d-block mb-1" style={{ fontWeight: 500 }}>Họ tên: </span>
                                        {isUpdate === false ?
                                            <div className="d-flex align-items-center px-4" style={{ height: 40 }}>{form?.ho_ten !== null ? form?.ho_ten : ""}</div>
                                            :
                                            <Form.Control
                                                type="text"
                                                value={form?.ho_ten !== null ? form?.ho_ten : ""}
                                                style={{ fontSize: 14, fontWeight: 400, height: 40, backgroundColor: "#fff" }}
                                                disabled={true}
                                            />
                                        }
                                    </div>
                                    <div className="col-3">
                                        <span className="d-block mb-1" style={{ fontWeight: 500 }}>Ngày sinh: </span>
                                        {isUpdate === false ?
                                            <div className="d-flex align-items-center px-4" style={{ height: 40 }}>{form?.ngay_sinh !== null ? moment(Number(form?.ngay_sinh)).format("DD/MM/YYYY") : ""}</div>
                                            :
                                            <DesktopDatePicker
                                                label=" "
                                                maxDate={new Date()}
                                                inputFormat="dd/MM/yyyy"
                                                value={tuoi}
                                                onChange={(e) => setTuoi(e)}
                                                renderInput={(params) => <TextField {...params} />}
                                            />
                                        }
                                    </div>
                                    <div className="col-3">
                                        <span className="d-block mb-1" style={{ fontWeight: 500 }}>Giới tính: </span>

                                        {isUpdate === false ?
                                            <div className="d-flex align-items-center px-4" style={{ height: 40 }}>{gioiTinh ? gioiTinh.label : "N/A"}</div>
                                            :
                                            <Select
                                                value={gioiTinh}
                                                style={inputStyle}
                                                closeonselect={true}
                                                options={genderOptions}
                                                placeholder="Chọn giới tính"
                                                onChange={(e) => handleGioiTinh(e.value)}
                                            />
                                        }
                                    </div>
                                    <div className="col-3">
                                        <span className="d-block mb-1" style={{ fontWeight: 500 }}>Cân nặng: </span>
                                        {isUpdate === false ?
                                            <div className="d-flex align-items-center px-4" style={{ height: 40 }}>{form?.weight !== null ? form?.weight : "N/A"}</div>
                                            :
                                            <Form.Control
                                                type="text"
                                                style={inputStyle}
                                                placeholder="Nhập cân nặng (kg)"
                                                value={form?.weight != null ? form?.weight : ""}
                                                onChange={(e) => setField("weight", e.target.value)}
                                            />
                                        }
                                    </div>
                                </div>
                                <div className="row mx-1 mb-4">
                                    <div className="col-3">
                                        <span className="d-block mb-1" style={{ fontWeight: 500 }}>Chiều cao: </span>
                                        {isUpdate === false ?
                                            <div className="d-flex align-items-center px-4" style={{ height: 40 }}>{form?.height !== null ? form?.height : "N/A"}</div>
                                            :
                                            <Form.Control
                                                type="text"
                                                style={inputStyle}
                                                placeholder="Nhập chiều cao (cm)"
                                                value={form?.height != null ? form?.height : ""}
                                                onChange={(e) => setField("height", e.target.value)}
                                            />
                                        }
                                    </div>
                                    <div className="col-3">
                                        <span className="d-block mb-1" style={{ fontWeight: 500 }}>Cholesterol: </span>
                                        {isUpdate === false ?
                                            <div className="d-flex align-items-center px-4" style={{ height: 40 }}>{chol ? chol.label : "N/A"}</div>
                                            :
                                            <Select
                                                value={chol}
                                                style={inputStyle}
                                                closeonselect={true}
                                                options={levelOptions}
                                                placeholder="Chọn mức độ"
                                                onChange={(e) => handleSelectes("chol", e)}
                                            />
                                        }
                                    </div>
                                    <div className="col-3">
                                        <span className="d-block mb-1" style={{ fontWeight: 500 }}>Glucose: </span>
                                        {isUpdate === false ?
                                            <div className="d-flex align-items-center px-4" style={{ height: 40 }}>{gluc ? gluc.label : "N/A"}</div>
                                            :
                                            <Select
                                                value={gluc}
                                                style={inputStyle}
                                                closeonselect={true}
                                                options={levelOptions}
                                                placeholder="Chọn mức độ"
                                                onChange={(e) => handleSelectes("gluc", e)}
                                            />
                                        }
                                    </div>
                                    <div className="col-3">
                                        <span className="d-block mb-1" style={{ fontWeight: 500 }}>Smoke: </span>
                                        {isUpdate === false ?
                                            <div className="d-flex align-items-center px-4" style={{ height: 40 }}>{smoke ? smoke.label : "N/A"}</div>
                                            :
                                            <Select
                                                value={smoke}
                                                style={inputStyle}
                                                closeonselect={true}
                                                options={ynOptions}
                                                placeholder="Chọn mức độ"
                                                onChange={(e) => handleSelectes("smoke", e)}
                                            />
                                        }
                                    </div>
                                </div>
                                <div className="row mx-1 mb-4">
                                    <div className="col-3">
                                        <span className="d-block mb-1" style={{ fontWeight: 500 }}>Alcohol: </span>
                                        {isUpdate === false ?
                                            <div className="d-flex align-items-center px-4" style={{ height: 40 }}>{alco ? alco.label : "N/A"}</div>
                                            :
                                            <Select
                                                value={alco}
                                                style={inputStyle}
                                                closeonselect={true}
                                                options={ynOptions}
                                                placeholder="Chọn mức độ"
                                                onChange={(e) => handleSelectes("alco", e)}
                                            />
                                        }
                                    </div>
                                    <div className="col-3">
                                        <span className="d-block mb-1" style={{ fontWeight: 500 }}>Activity: </span>
                                        {isUpdate === false ?
                                            <div className="d-flex align-items-center px-4" style={{ height: 40 }}>{activ ? activ.label : "N/A"}</div>
                                            :
                                            <Select
                                                value={activ}
                                                style={inputStyle}
                                                closeonselect={true}
                                                options={ynOptions}
                                                placeholder="Chọn mức độ"
                                                onChange={(e) => handleSelectes("activ", e)}
                                            />
                                        }
                                    </div>
                                </div>


                                <div className="row px-0">
                                    <div className="col-12 px-0 text-end">
                                        <button className="btn btn-success py-2" style={{ fontSize: 14, height: 44 }} onClick={(e) => setIsProgressing(!isProgressing)}><i className="fas fa-arrow-right"></i> Tiến hành chẩn đoán</button>
                                    </div>
                                </div>

                            </div>
                        </div>
                        :
                        <div className="d-flex justify-content-center align-items-center" style={{ height: "78vh" }}>
                            Đang nhận data từ thiết bị
                        </div>
                    }
                </div>
            </div>
        </LocalizationProvider>
    )
}