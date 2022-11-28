import { DesktopDatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import { enAU } from "date-fns/locale";

import { TextField } from "@mui/material";
import axios from "axios";
import moment from "moment";
import { useEffect, useState } from "react";
import { Form } from "react-bootstrap";
import { ThreeDots } from "react-loader-spinner";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import Select from "react-select";
import { toast } from "react-toastify";
import api from "../../../configs/api";
import { genderOptions, levelOptions, ynOptions } from "../../../data";
import { selectCurrentUser } from "../../../redux-module/auth/authSlice";


export function Diagnostic() {
    const navigate = useNavigate();
    const currentUser = useSelector(selectCurrentUser);

    const [form, setForm] = useState({});
    const [datas, setDatas] = useState({});
    const [errors, setErrors] = useState({});
    const [isLoading, setIsLoading] = useState(false);
    const [predictForm, setPredictForm] = useState({});

    const [tuoi, setTuoi] = useState(new Date());
    const [gioiTinh, setGioiTinh] = useState();
    const [chol, setChol] = useState();
    const [gluc, setGluc] = useState();
    const [alco, setAlco] = useState();
    const [smoke, setSmoke] = useState();
    const [activ, setActiv] = useState();
    const [isUpdate, setIsUpdate] = useState(false);
    const [isProgressing, setIsProgressing] = useState(true);
    const [isManually, setIsManually] = useState(false);

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


    const setPredictField = (field, value) => {
        setPredictForm({
            ...predictForm,
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
                    setDatas(data)
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

    const handleTuoi = (value) => {
        setField("ngay_sinh", value);
        const now = new Date().getTime();
        const diff = Math.round((now - value) / (1000 * 60 * 60 * 24) - 1);
        setTuoi(diff)
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
        const { ho_ten, ngay_sinh, weight, height } = form;

        if (!ho_ten || ho_ten === "") newErrors.ho_ten = "Họ tên không được bỏ trống!";
        if (!ngay_sinh || ngay_sinh <= 0) newErrors.ngay_sinh = "Ngày sinh không được bỏ trống!";
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


    const handleSubmit = async () => {
        setIsLoading(true);
        const newError = formValidation();

        if (Object.keys(newError).length > 0) {
            setErrors(newError);
            setIsLoading(false);
        } else {
            setErrors({});
            const json = new FormData();

            await json.append("ho_ten", form?.ho_ten.toUpperCase());
            await json.append("ngay_sinh", form?.ngay_sinh);
            await json.append("tuoi", tuoi);
            await json.append("gioi_tinh", form?.gioi_tinh);
            await json.append("height", form?.height);
            await json.append("weight", form?.weight);
            await json.append("chol", Number(form?.chol));
            await json.append("gluc", Number(form?.gluc));
            await json.append("smoke", Number(form?.smoke));
            await json.append("alco", Number(form?.alco));
            await json.append("active", Number(form?.active));


            axios
                .put(api.API_QUAN_LY_NGUOI_DUNG_STATIC + "/" + form?.id, json)
                .then(({ data }) => {
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
                    getUserInfo();
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

    const formPredictValidation = () => {
        const newErrors = {}

        if (!predictForm?.ap_hi || predictForm?.ap_hi === "") {
            newErrors.ap_hi = "Huyết áp tâm trương không được bỏ trống!"
        }
        if (!predictForm?.ap_lo || predictForm?.ap_lo === "") {
            newErrors.ap_lo = "Huyết áp tâm thu không được bỏ trống!"
        }

        return newErrors;
    }

    const handlePredict = (e) => {
        e.preventDefault();

        const newError = formPredictValidation();

        if (Object.keys(newError).length > 0) {
            setErrors(newError);
            setIsLoading(false);
        } else {
            const data = new FormData();

            data.append("age", tuoi)
            data.append("height", form?.height)
            data.append("weight", form?.weight)
            data.append("gender", form?.gioi_tinh)
            data.append("chol", form?.chol)
            data.append("ap_hi", predictForm?.ap_hi)
            data.append("ap_lo", predictForm?.ap_lo)
            data.append("gluc", form?.gluc)
            data.append("smoke", form?.smoke)
            data.append("alco", form?.alco)
            data.append("active", form?.active)

            axios
                .post(api.API_QUAN_LY_LICH_SU_PREDICT, data)
                .then(({ data }) => {
                    setIsManually(false)
                    setIsProgressing(true)
                    setIsUpdate(false)

                    toast.success(data?.result, {
                        position: "top-right",
                        autoClose: 1000,
                        hideProgressBar: false,
                        closeOnClick: true,
                        pauseOnHover: true,
                        draggable: true,
                        progress: undefined,
                        toastId: "error",
                    });

                    setTimeout(() => {
                        navigate("/admin/quan-ly-lich-su")
                    }, 2000);
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

    const onReset = () => {
        setErrors({})
        setForm(datas)
        handleStatics(datas)
        setTuoi(datas?.ngay_sinh)
        handleGioiTinh(datas?.gioi_tinh)
    }

    return (
        <LocalizationProvider dateAdapter={AdapterDateFns} locale={enAU}>
            <div>
                <div className="card-box" style={{ padding: "32px" }}>
                    {isProgressing === true ?
                        <div style={{ height: "47vh" }}>
                            <div className="row">
                                <div className="col-12 mb-8">
                                    <h4 className="fw-bold">CHẨN ĐOÁN TÌNH TRẠNG</h4>
                                </div>

                                <div className="col-6 mt-8">
                                    <h5 className="fw-bold">Thông tin hiện tại</h5>
                                </div>

                                <div className="col-6 mb-10 text-end">
                                    {isUpdate == true ?
                                        <div>
                                            <button className="btn btn-success py-0 me-2" style={{ fontSize: "13px", height: "38px", width: "130px" }} onClick={() => { setIsUpdate(false); handleSubmit(); }}>
                                                <i className="fas fa-save me-1" style={{ fontSize: "12px" }}></i>Lưu
                                            </button>
                                            <button className="btn btn-secondary py-0 ms-2" style={{ fontSize: "13px", height: "38px", width: "130px" }} onClick={() => { setIsUpdate(false); onReset() }}>
                                                <i className="fas fa-arrow-right me-1" style={{ fontSize: "12px" }}></i>Quay lại
                                            </button>
                                        </div>
                                        :
                                        isLoading == false ?
                                            <button className="btn btn-primary py-0" style={{ fontSize: "13px", height: "38px", width: "130px" }} onClick={() => setIsUpdate(true)}>
                                                <i className="fas fa-edit me-1" style={{ fontSize: "12px" }}></i>Cập nhật
                                            </button>
                                            :
                                            <button className="btn btn-link" style={{ fontSize: "13px", height: "38px", width: "130px" }}>
                                                <span className="indicator-progress" style={{ display: "block", fontSize: 12 }} >
                                                    Vui lòng chờ...
                                                    <span className="spinner-border spinner-border-sm align-middle ms-2"></span>
                                                </span>
                                            </button>
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
                                        } {errors?.password ? (<span className="text-danger">{errors?.password}</span>) : ("")}
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
                                                value={form?.ngay_sinh}
                                                onChange={(e) => {handleTuoi(new Date(e).getTime())}}
                                                renderInput={(params) => <TextField {...params} />}
                                            />
                                        } {errors?.tuoi ? (<span className="text-danger">{errors?.tuoi}</span>) : ("")}
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
                                        } {errors?.gioiTinh ? (<span className="text-danger">{errors?.gioiTinh}</span>) : ("")}
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
                                        } {errors?.weight ? (<span className="text-danger">{errors?.weight}</span>) : ("")}
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
                                        } {errors?.height ? (<span className="text-danger">{errors?.height}</span>) : ("")}
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
                                        } {errors?.chol ? (<span className="text-danger">{errors?.chol}</span>) : ("")}
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
                                        } {errors?.gluc ? (<span className="text-danger">{errors?.gluc}</span>) : ("")}
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
                                        } {errors?.smoke ? (<span className="text-danger">{errors?.smoke}</span>) : ("")}
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
                                        } {errors?.alco ? (<span className="text-danger">{errors?.alco}</span>) : ("")}
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
                                        } {errors?.activ ? (<span className="text-danger">{errors?.activ}</span>) : ("")}
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
                        isManually ?
                            <div style={{ height: "78vh" }} >
                                <div className="row" style={{ paddingTop: "20vh" }}>
                                    <div className="col-4"> </div>
                                    <div className="col-4 mb-6">
                                        <label className="font-weight-bold">Huyết áp tâm trương:</label>
                                        <Form.Control
                                            type="text"
                                            placeholder="Nhập chỉ số"
                                            style={{ fontSize: 14, fontWeight: 400 }}
                                            value={predictForm?.ap_hi ? predictForm?.ap_hi : ""}
                                            onChange={(e) => setPredictField("ap_hi", e.target.value)}
                                        />
                                    </div>
                                    <div className="col-4"> </div>
                                    <div className="col-4"> </div>
                                    <div className="col-4 mb-6">
                                        <label className="font-weight-bold">Huyết áp tâm thu:</label>
                                        <Form.Control
                                            type="text"
                                            placeholder="Nhập chỉ số"
                                            style={{ fontSize: 14, fontWeight: 400 }}
                                            value={predictForm?.ap_lo ? predictForm?.ap_lo : ""}
                                            onChange={(e) => setPredictField("ap_lo", e.target.value)}
                                        />
                                    </div>
                                    <div className="col-4"> </div>
                                    <div className="col-4"> </div>
                                    <div className="col-4">
                                        {isLoading ? (
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
                                                style={{ width: "100%", height: "46px" }} onClick={(e) => handlePredict(e)}>
                                                <span>
                                                    <i className="fas fa-chevron-circle-right"></i>
                                                    &nbsp;&nbsp; Chẩn đoán
                                                </span>
                                            </button>
                                        )}
                                    </div>
                                    <div className="col-4"> </div>
                                </div>
                            </div>
                            :
                            <div className="d-flex justify-content-center align-items-center" style={{ height: "78vh", flexDirection: "column" }}>
                                <div className="mb-8">
                                    <ThreeDots
                                        height="80"
                                        width="80"
                                        radius="9"
                                        color="#4fa94d"
                                        ariaLabel="three-dots-loading"
                                        wrapperStyle={{}}
                                        wrapperClassName=""
                                        visible={true}
                                    />
                                </div>
                                <span style={{ fontSize: 18 }}>
                                    Đang nhận data từ thiết bị...
                                </span>
                                <span>
                                    hoặc
                                </span>
                                <span className="text-primary" style={{ fontSize: 18, textDecoration: "underline", cursor: "pointer" }}
                                    onClick={() => setIsManually(true)}>
                                    Nhập thông tin thủ công
                                </span>
                            </div>
                    }
                </div>

                <div className="card-box" style={{ padding: "32px" }}>
                    <div className="row">
                        <div className="col-12 mb-8">
                            <h4 className="fw-bold">LỊCH SỬ GẦN ĐÂY</h4>
                        </div>
                    </div>
                </div>
            </div>
        </LocalizationProvider>
    )
}
