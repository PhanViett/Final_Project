import axios from "axios";
import { useEffect, useState } from "react";
import { Form, Modal } from "react-bootstrap";
import DataTable from "react-data-table-component";
import { Dna, InfinitySpin } from "react-loader-spinner";
import { toast } from "react-toastify";
import { conditionalRowStyles, customStyles, paginationOptions } from "../../../../../_metronic/assets/custom/table";
import { useDebounce } from "../../../../../_metronic/helpers";
import api from "../../../../configs/api";
import { genderOptions } from "../../../../data";


export function QuanLyNguoiDung() {

    const [page, setPage] = useState(1);
    const [perPage, setPerPage] = useState(10);
    const [totalRows, setTotalRows] = useState(0);
    const [isLoading, setIsLoading] = useState(true);

    const [show, setShow] = useState(false);
    const [form, setForm] = useState({});
    const [errors, setErrors] = useState({});
    const [searchKey, setSearchKey] = useState("");

    const [status, setStatus] = useState("Tạo mới");
    const [selectedId, setSelectedId] = useState("");
    const [nguoiDungList, setNguoiDungList] = useState({});

    const debouncedSearchKey = useDebounce(searchKey, 1000);

    const openModal = () => setShow(true)
    const closeModal = () => setShow(false)


    useEffect(() => {
        if (debouncedSearchKey !== undefined && searchKey !== undefined) {
            getList(1, perPage, debouncedSearchKey);
        }
    }, [debouncedSearchKey]);



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

    const getList = ({ page_number = page, size = perPage, search_key = searchKey }) => {
        setIsLoading(true);
        axios
            .post(api.API_QUAN_LY_NGUOI_DUNG + `?page=${page_number}&per_page=${size}`, { search_key: search_key })
            .then((data) => {
                if (data && data?.status === 404) {
                    setIsLoading(true);
                    getList(page, perPage, debouncedSearchKey);
                } else {
                    data = data?.data;
                    if (data) {
                        let temp_data = data?.results
                        for (let i = 0; i < data?.results.length; i++) {
                            temp_data[i].stt = i + 1
                            const gt = genderOptions.find((e) => e.value == temp_data[i].gioi_tinh)
                            temp_data[i].gioi_tinh = gt ? gt.label : "N/A"
                        }
                        setNguoiDungList(temp_data);
                        setTotalRows(data?.total);
                    }
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

    const handlePageChange = (page) => {
        setPage(page);
        getList({ page_number: page });
    };

    const handlePerRowsChange = async (newPerPage, page) => {
        setIsLoading(true)
        axios
            .post(api.API_QUAN_LY_NGUOI_DUNG + `?page=${page}&per_page=${newPerPage}`, { search_key: searchKey })
            .then((data) => {
                if (data && data?.status === 404) {
                    setIsLoading(true);
                    getList(page, perPage, debouncedSearchKey);
                } else {
                    data = data?.data;
                    if (data) {
                        let temp_data = data?.results
                        for (let i = 0; i < data?.results.length; i++) {
                            temp_data[i].stt = i + 1
                            const gt = genderOptions.find((e) => e.value == temp_data[i].gioi_tinh)
                            temp_data[i].gioi_tinh = gt ? gt.label : "N/A"
                        }
                        setNguoiDungList(temp_data);
                        setTotalRows(data?.total);
                    }
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
                setIsLoading(false)
            });
    };

    const handleReset = async () => {
        await setForm({});
        await setErrors({});
    }



    const formValidation = () => {
        const newErrors = {};
        const { ho, ten, tai_khoan, dien_thoai, email, mat_khau } = form;

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
        if (!dien_thoai || dien_thoai === "") {
            newErrors.dien_thoai = "Điện thoại không được bỏ trống!"
        } else if (dien_thoai.split("").length !== 10) {
            newErrors.dien_thoai = "Điện thoại không hợp lệ!"
        }
        if (status !== "Cập nhật") {
            if (!tai_khoan || tai_khoan === "") {
                newErrors.tai_khoan = "Tài khoản không được bỏ trống!"
            }
            if (!mat_khau || mat_khau === "") {
                newErrors.mat_khau = "Mật khẩu không được bỏ trống!"
            }
        }

        return newErrors;
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        const newErrors = formValidation();

        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
        } else {
            onSubmit();
        }
    }

    const onSubmit = () => {
        if (status === "Thêm mới") {
            const data = new FormData()

            data.append("ho", form?.ho)
            data.append("ten", form?.ten)
            data.append("tai_khoan", form?.tai_khoan)
            data.append("mat_khau", form?.mat_khau)
            data.append("dien_thoai", form?.dien_thoai)
            data.append("email", form?.email)

            axios
                .post(api.API_QUAN_LY_NGUOI_DUNG_CREATE, data)
                .then(({ data }) => {
                    if (data) {
                        toast.success("Thêm mới thành công", {
                            position: "top-right",
                            autoClose: 1000,
                            hideProgressBar: false,
                            closeOnClick: true,
                            pauseOnHover: true,
                            draggable: true,
                            progress: undefined,
                            toastId: "error",
                        });
                        getList({ page, perPage, searchKey });
                        handleReset();
                        closeModal();
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
                });
        } else if (status === "Cập nhật") {
            const data = new FormData()

            data.append("ho", form?.ho)
            data.append("ten", form?.ten)
            data.append("dien_thoai", form?.dien_thoai)
            data.append("email", form?.email)

            axios
                .put(api.API_QUAN_LY_NGUOI_DUNG_UPDATE + "/" + selectedId, data)
                .then(({ data }) => {
                    if (data) {
                        toast.success("Cập nhật thành công", {
                            position: "top-right",
                            autoClose: 1000,
                            hideProgressBar: false,
                            closeOnClick: true,
                            pauseOnHover: true,
                            draggable: true,
                            progress: undefined,
                            toastId: "error",
                        });
                        getList({ page, perPage, searchKey });
                        handleReset();
                        closeModal();
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
                });
        }
    }

    const handleDelete = (id) => {
        axios
            .delete(api.API_QUAN_LY_NGUOI_DUNG_DELETE + "/" + id)
            .then(({ data }) => {
                if (data) {
                    toast.success("Xóa người dùng thành công", {
                        position: "top-right",
                        autoClose: 1000,
                        hideProgressBar: false,
                        closeOnClick: true,
                        pauseOnHover: true,
                        draggable: true,
                        progress: undefined,
                        toastId: "error",
                    });
                    getList({ page, perPage, searchKey });
                    handleReset();
                    closeModal();
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
            });
    }



    const columns = [
        {
            name: "STT",
            selector: (row) => row.stt ? <span>{row?.stt}</span> : <span className="text-danger"> N/A</span>,
            grow: 1,
            style: {
                cursor: "pointer",
                color: "#202124",
            },
            center: true
        },
        {
            name: "Tên người dùng",
            selector: (row) => row.ho_ten ? <span>{row?.ho_ten}</span> : <span className="text-danger"> N/A</span>,
            grow: 5,
            style: {
                cursor: "pointer",
                color: "#202124",
            },
        },
        {
            name: "Tài khoản",
            selector: (row) => row.tai_khoan ? <span>{row?.tai_khoan}</span> : <span className="text-danger"> N/A</span>,
            grow: 4,
            style: {
                cursor: "pointer",
                color: "#202124",
            },
        },
        {
            name: "Giới tính",
            selector: (row) => row?.gioi_tinh === "N/A" ? <span style={{ color: "#9fa2ae" }}>{row?.gioi_tinh}</span> : <>{row?.gioi_tinh}</>,
            grow: 2,
            center: true
        },
        {
            name: "Số điện thoại",
            selector: (row) => row.dien_thoai ? <span>{row?.dien_thoai}</span> : <span className="text-danger"> N/A</span>,
            grow: 3,
            center: true
        },
        {
            name: "Email",
            selector: (row) => row.email ? <span>{row?.email}</span> : <span className="text-danger"> N/A</span>,
            grow: 3,
            center: true
        },
        {
            name: "",
            selector: (row) =>
                <div>
                    <button className="btn btn-link me-2"
                        onClick={() => {
                            setForm({
                                ho: row?.ho ? row?.ho : "",
                                ten: row?.ten ? row?.ten : "",
                                tai_khoan: row?.tai_khoan ? row?.tai_khoan : "",
                                dien_thoai: row?.dien_thoai ? row?.dien_thoai : "",
                                email: row?.email ? row?.email : "",
                            })
                            setStatus("Cập nhật");
                            setSelectedId(row?.id)
                            openModal();
                        }}>
                        <i className="fas fa-edit text-primary"></i>
                    </button>
                    {/* <button className="btn btn-link ms-2" onClick={() => {setSelectedId(row?.id); handleDelete(row?.id)}}>
                        <i className="fas fa-trash-alt text-danger"></i>
                    </button> */}
                </div>
            ,
            grow: 1,
        },
    ];


    return (
        <div className="py-3">
            <div className="card-box" style={{ padding: "32px" }}>
                <div className="row">
                    <div className="col-12 mb-4">
                        <h4 className="fw-bold">QUẢN LÝ NGƯỜI DÙNG</h4>
                    </div>

                    <div className="col-8 mt-4 mb-6 ">
                        <Form.Control
                            type="text"
                            placeholder="Nhập từ khóa tìm kiếm..."
                            style={{ fontSize: 14, fontWeight: 400, height: "38px", width: "320px" }}
                            onChange={(e) => setSearchKey(e.target.value)}
                        />
                    </div>
                    <div className="col-4 mt-4 mb-6 text-end">
                        <button className="btn btn-primary py-0" style={{ fontSize: "13px", height: "38px" }} onClick={() => { setStatus("Thêm mới"); handleReset(); openModal(); }}>
                            <i className="fas fa-plus me-1" style={{ fontSize: "12px" }}></i>Tạo mới
                        </button>
                    </div>

                    <div className="col-12 mt-6 pe-10">
                        <DataTable
                            noDataComponent={"Không có dữ liệu ..."}
                            sortServer
                            progressPending={isLoading}
                            columns={columns}
                            data={nguoiDungList}
                            customStyles={customStyles}
                            pagination
                            highlightOnHover
                            pointerOnHover
                            paginationServer
                            paginationTotalRows={totalRows}
                            onChangeRowsPerPage={handlePerRowsChange}
                            onChangePage={handlePageChange}
                            paginationComponentOptions={paginationOptions}
                            conditionalRowStyles={conditionalRowStyles}
                            progressComponent={
                                <div style={{ padding: "24px" }}>
                                    <InfinitySpin
                                        width='200'
                                        color="#4fa94d"
                                    />
                                </div>
                            }
                        />
                    </div>

                    <Modal className="modal-md-80" show={show} size="lg">
                        <Modal.Header className="py-5">
                            <label style={{ fontSize: "18px", fontWeight: 600 }}> {status} người dùng</label>
                        </Modal.Header>
                        <Modal.Body>
                            <div className="row mb-4">
                                <div className="col-2">
                                    <label className="mt-1 mb-2 required" style={{ fontWeight: 600 }}>Họ</label>
                                </div>
                                <div className="col-4">
                                    <Form.Control
                                        type="text"
                                        placeholder="Nhập họ"
                                        value={form?.ho ? form?.ho : ""}
                                        style={{ fontSize: 13, fontWeight: 400, height: "34px" }}
                                        onChange={(e) => setField("ho", e.target.value)}
                                    />
                                    <span className="text-danger">
                                        {errors?.ho ? (<span style={{ fontSize: 13 }}>{errors?.ho}</span>) : ("")}
                                    </span>
                                </div>

                                <div className="col-2">
                                    <label className="mt-1 mb-2 required" style={{ fontWeight: 600 }}>Tên</label>
                                </div>
                                <div className="col-4">
                                    <Form.Control
                                        type="text"
                                        placeholder="Nhập tên"
                                        value={form?.ten ? form?.ten : ""}
                                        style={{ fontSize: 13, fontWeight: 400, height: "34px" }}
                                        onChange={(e) => setField("ten", e.target.value)}
                                    />
                                    <span className="text-danger">
                                        {errors?.ten ? (<span style={{ fontSize: 13 }}>{errors?.ten}</span>) : ("")}
                                    </span>
                                </div>

                            </div>

                            <div className="row mb-4">
                                <div className="col-2">
                                    {status === "Thêm mới" ?
                                        <label className="mt-1 mb-2 required" style={{ fontWeight: 600 }}>Tên đăng nhập</label>
                                        :
                                        <label className="mt-1 mb-2" style={{ fontWeight: 600 }}>Tên đăng nhập</label>
                                    }
                                </div>
                                <div className="col-10">
                                    <Form.Control
                                        type="text"
                                        placeholder="Nhập tên đăng nhập"
                                        value={form?.tai_khoan ? form?.tai_khoan : ""}
                                        style={{ fontSize: 13, fontWeight: 400, height: "34px" }}
                                        onChange={(e) => setField("tai_khoan", e.target.value)}
                                        disabled={status === "Cập nhật" ? true : false}
                                    />
                                    <span className="text-danger">
                                        {errors?.tai_khoan ? (<span style={{ fontSize: 13 }}>{errors?.tai_khoan}</span>) : ("")}
                                    </span>
                                </div>
                            </div>

                            <div className="row mb-4">
                                <div className="col-2">
                                    <label className="mt-1 mb-2 required" style={{ fontWeight: 600 }}>Số điện thoại</label>
                                </div>
                                <div className="col-10">
                                    <Form.Control
                                        type="text"
                                        placeholder="Nhập số điện thoại"
                                        value={form?.dien_thoai ? form?.dien_thoai : ""}
                                        style={{ fontSize: 13, fontWeight: 400, height: "34px" }}
                                        onChange={(e) => setField("dien_thoai", e.target.value)}
                                    />
                                    <span className="text-danger">
                                        {errors?.dien_thoai ? (<span style={{ fontSize: 13 }}>{errors?.dien_thoai}</span>) : ("")}
                                    </span>
                                </div>
                            </div>

                            <div className="row mb-4">
                                <div className="col-2">
                                    <label className="mt-1 mb-2 required" style={{ fontWeight: 600 }}>Email</label>
                                </div>
                                <div className="col-10">
                                    <Form.Control
                                        type="text"
                                        placeholder="Nhập email"
                                        value={form?.email ? form?.email : ""}
                                        style={{ fontSize: 13, fontWeight: 400, height: "34px" }}
                                        onChange={(e) => setField("email", e.target.value)}
                                    />
                                    <span className="text-danger">
                                        {errors?.email ? (<span style={{ fontSize: 13 }}>{errors?.email}</span>) : ("")}
                                    </span>
                                </div>
                            </div>

                            <div className="row mb-4">
                                <div className="col-2">
                                    {status === "Thêm mới" ?
                                        <label className="mt-1 mb-2 required" style={{ fontWeight: 600 }}>Mật khẩu</label>
                                        :
                                        <label className="mt-1 mb-2" style={{ fontWeight: 600 }}>Mật khẩu</label>
                                    }
                                </div>
                                <div className="col-10">
                                    <Form.Control
                                        type="password"
                                        placeholder="Nhập mật khẩu"
                                        value={form?.mat_khau ? form?.mat_khau : ""}
                                        style={{ fontSize: 13, fontWeight: 400, height: "34px" }}
                                        onChange={(e) => setField("mat_khau", e.target.value)}
                                        disabled={status === "Cập nhật" ? true : false}
                                    />
                                    <span className="text-danger">
                                        {errors?.mat_khau ? (<span style={{ fontSize: 13 }}>{errors?.mat_khau}</span>) : ("")}
                                    </span>
                                </div>
                            </div>


                            <div className="row pt-6">
                                <div className="col-12 text-center">
                                    <button className="btn btn-secondary btn-bottom-sm mx-3" onClick={() => closeModal()}><i className="fas fa-arrow-circle-left"></i> Quay lại</button>
                                    <button className="btn btn-primary btn-bottom-sm mx-3" onClick={() => handleReset()}><i className="fas fa-undo-alt"></i> Reset</button>
                                    <button className="btn btn-success btn-bottom-sm mx-3" onClick={(e) => handleSubmit(e)}><i className="fas fa-save"></i> Lưu</button>
                                </div>
                            </div>
                        </Modal.Body>
                    </Modal>

                </div>
            </div>
        </div>
    )
}