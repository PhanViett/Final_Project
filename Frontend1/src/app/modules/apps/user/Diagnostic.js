import { enAU } from "date-fns/locale";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { DesktopDatePicker, LocalizationProvider } from "@mui/x-date-pickers";


import { useEffect, useState } from "react";
import Select from "react-select";
import { Form } from "react-bootstrap";
import { TextField } from "@mui/material";
import { genderOptions, levelOptions, ynOptions } from "../../../data";
import axios from "axios";
import { useSelector } from "react-redux";
import { selectCurrentUser } from "../../../redux-module/auth/authSlice";
import api from "../../../configs/api";
import moment from "moment";


export function Diagnostic() {
    const currentUser = useSelector(selectCurrentUser)

    const [form, setForm] = useState({});
    const [errors, setErrors] = useState({});

    const [tuoi, setTuoi] = useState(new Date());
    const [gioiTinh, setGioiTinh] = useState();
    const [chol, setChol] = useState();
    const [gluc, setGluc] = useState();
    const [alco, setAlco] = useState();
    const [smoke, setSmoke] = useState();
    const [activ, setActiv] = useState();
    const [isUpdate, setIsUpdate] = useState(false);

    const inputStyle = { fontSize: 14, fontWeight: 400, height: 40 }

    useEffect(() => {
        getUserInfo();
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


    const getUserInfo = () => {
        axios
            .get(api.API_QUAN_LY_NGUOI_DUNG_INFO + "/" + currentUser.id)
            .then(({data}) => {
                if (data) {
                    handleTuoi(data?.ngay_sinh)
                    handleGioiTinh(data?.gioi_tinh)
                    handleStatics(data)
                    setForm(data)
                }
            })
    }


    const handleTuoi = (value) => {
        if (typeof value === "number") {
            setTuoi(value);
        } else if (typeof value === "object") {
            const diff = new Date().getTime() - new Date(value).getTime();
            setField("tuoi", Math.round(diff / (1000 * 3600 * 24)))
            setTuoi(value)
        }
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
            setField("chalcool", data.value)
        } else if (type === "activ") {
            setActiv(data)
            setField("active", data.value)
        }
    }


    const formValidation = () => {
        const {ho_ten} = form;
        
    }

    return (
        <LocalizationProvider dateAdapter={AdapterDateFns} locale={enAU}>

            <div className="py-3">
                <div className="card-box" style={{ padding: "32px" }}>
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
                                    <button className="btn btn-success py-0 me-2" style={{ fontSize: "13px", height: "38px", width: "130px" }} onClick={() => setIsUpdate(false)}>
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
                                    <span>{form?.ho_ten !== null ? form?.ho_ten : ""}</span>
                                    :
                                    <Form.Control
                                        type="text"
                                        value="Phan Văn Việt"
                                        style={{ fontSize: 14, fontWeight: 400, height: 40, backgroundColor: "#fff" }}
                                        disabled={true}
                                    />
                                }
                            </div>
                            <div className="col-3">
                                <span className="d-block mb-1" style={{ fontWeight: 500 }}>Ngày sinh: </span>
                                {isUpdate === false ?
                                    <span>{form?.ngay_sinh !== null ? moment(Number(form?.ngay_sinh)).format("DD/MM/YYYY") : ""}</span>
                                    :
                                    <DesktopDatePicker
                                        label=" "
                                        maxDate={new Date()}
                                        inputFormat="dd/MM/yyyy"
                                        value={tuoi}
                                        onChange={handleTuoi}
                                        renderInput={(params) => <TextField {...params} />}
                                    />
                                }
                            </div>
                            <div className="col-3">
                                <span className="d-block mb-1" style={{ fontWeight: 500 }}>Giới tính: </span>
                                {isUpdate === false ?
                                    <span>{gioiTinh ? gioiTinh.label : "N/A"}</span>
                                    :
                                    <Select
                                        value={gioiTinh}
                                        style={inputStyle}
                                        closeOnSelect={true}
                                        options={genderOptions}
                                        placeholder="Chọn giới tính"
                                        onChange={(e) => handleGioiTinh(e.value)}
                                    />
                                }
                            </div>
                            <div className="col-3">
                                <span className="d-block mb-1" style={{ fontWeight: 500 }}>Cân nặng: </span>
                                {isUpdate === false ?
                                    <span>{form?.weight !== null ? form?.weight : "N/A"}</span>
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
                                    <span>{form?.height !== null ? form?.height : "N/A"}</span>
                                    :
                                    <Form.Control
                                        type="text"
                                        style={inputStyle}
                                        placeholder="Nhập chiều cao (cm)"
                                        value={form?.weight != null ? form?.weight : ""}
                                        onChange={(e) => setField("weight", e.target.value)}
                                    />
                                }
                            </div>
                            <div className="col-3">
                                <span className="d-block mb-1" style={{ fontWeight: 500 }}>Cholesterol: </span>
                                {isUpdate === false ?
                                    <span>{chol ? chol.label : "N/A"}</span>
                                    :
                                    <Select
                                        value={chol}
                                        style={inputStyle}
                                        closeOnSelect={true}
                                        options={levelOptions}
                                        placeholder="Chọn mức độ"
                                        onChange={(e) => handleSelectes("chol", e)}
                                    />
                                }
                            </div>
                            <div className="col-3">
                                <span className="d-block mb-1" style={{ fontWeight: 500 }}>Glucose: </span>
                                {isUpdate === false ?
                                    <span>{gluc ? gluc.label : "N/A"}</span>
                                    :
                                    <Select
                                        value={gluc}
                                        style={inputStyle}
                                        closeOnSelect={true}
                                        options={levelOptions}
                                        placeholder="Chọn mức độ"
                                        onChange={(e) => handleSelectes("gluc", e)}
                                    />
                                }
                            </div>
                            <div className="col-3">
                                <span className="d-block mb-1" style={{ fontWeight: 500 }}>Smoke: </span>
                                {isUpdate === false ?
                                    <span>{smoke ? smoke.label : "N/A"}</span>
                                    :
                                    <Select
                                        value={smoke}
                                        style={inputStyle}
                                        closeOnSelect={true}
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
                                    <span>{alco ? alco.label : "N/A"}</span>
                                    :
                                    <Select
                                        value={alco}
                                        style={inputStyle}
                                        closeOnSelect={true}
                                        options={ynOptions}
                                        placeholder="Chọn mức độ"
                                        onChange={(e) => handleSelectes("alco", e)}
                                    />
                                }
                            </div>
                            <div className="col-3">
                                <span className="d-block mb-1" style={{ fontWeight: 500 }}>Activity: </span>
                                {isUpdate === false ?
                                    <span>{activ ? activ.label : "N/A"}</span>
                                    :
                                    <Select
                                        value={activ}
                                        style={inputStyle}
                                        closeOnSelect={true}
                                        options={ynOptions}
                                        placeholder="Chọn mức độ"
                                        onChange={(e) => handleSelectes("activ", e)}
                                    />
                                }
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </LocalizationProvider>
    )
}