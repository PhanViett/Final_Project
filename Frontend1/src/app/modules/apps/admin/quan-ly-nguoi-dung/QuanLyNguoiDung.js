import axios from "axios";
import { useEffect, useState } from "react";
import { Form } from "react-bootstrap";
import DataTable from "react-data-table-component";
import { Oval } from "react-loader-spinner";
import { conditionalRowStyles, customStyles, paginationOptions } from "../../../../../_metronic/assets/custom/table";
import { useDebounce } from "../../../../../_metronic/helpers";
import api from "../../../../configs/api";


export function QuanLyNguoiDung() {

    const [page, setPage] = useState(1);
    const [perPage, setPerPage] = useState(1);
    const [totalRows, setTotalRows] = useState(0);
    const [isLoading, setIsLoading] = useState(false);

    const [form, setForm] = useState({});
    const [errors, setErrors] = useState({});
    const [searchKey, setSearchKey] = useState("");

    const [status, setStatus] = useState("Tạo mới");
    const [nguoiDungList, setNguoiDungList] = useState({});

    const debouncedSearchKey = useDebounce(searchKey, 1000);


    useEffect(() => {
        if (debouncedSearchKey !== undefined && searchKey !== undefined) {
            getList(1, perPage, debouncedSearchKey);
        }
    }, [debouncedSearchKey]);

    const getList = (page_number = page, size = perPage, search_key = searchKey) => {
        axios
            .post(api.API_QUAN_LY_NGUOI_DUNG + `?page=${page_number}&per_page=${size}`, { search_key: search_key })
            .then(({ data }) => {
                if (data) {
                    setNguoiDungList(data?.results)
                }
            })
    }

    const handlePageChange = (page) => {
        setPage(page);
        getList({ page_number: page });
    };

    const handlePerRowsChange = async (newPerPage, page) => {
        axios
            .post(api.API_QUAN_LY_NGUOI_DUNG, {})
            .then(({ data }) => {
                if (data) {
                    setNguoiDungList(data?.results);
                    setPerPage(newPerPage);
                }
            })
            .catch(() => { })
            .finally(() => { });
    };

    const columns = [
        {
            name: "Tên người dùng",
            selector: (row) => row.ho_ten ? <span>{row?.ho_ten}</span> : <span className="text-danger"> N/A</span>,
            grow: 8,
            style: {
                cursor: "pointer",
                color: "#202124",
            },
        },
        {
            name: "Giới tính",
            selector: (row) => row.gioi_tinh ? <span>{row?.gioi_tinh}</span> : <span className="text-danger"> N/A</span>,
            grow: 3,
        },
        {
            name: "Số điện thoại",
            selector: (row) => row.dien_thoai ? <span>{row?.dien_thoai}</span> : <span className="text-danger"> N/A</span>,
            grow: 2,
        },
        {
            name: "Email",
            selector: (row) => row.email ? <span>{row?.email}</span> : <span className="text-danger"> N/A</span>,
            grow: 2,
        },
        {
            name: "Trạng thái",
            selector: (row) => row.active ? <span>{row?.active}</span> : <span className="text-danger"> N/A</span>,
            grow: 2,
        },
        {
            name: "",
            selector: (row) =>
                <div style={{ justifyContent: "end" }}>
                    <button className="btn btn-link me-2" onClick={() => handleSubmit(row?.id, "Cập nhật")}>
                        <i className="fas fa-edit text-primary"></i>
                    </button>
                    <button className="btn btn-link ms-2" onClick={() => handleDelete(row?.id)}>
                        <i class="fas fa-trash-alt text-danger"></i>
                    </button>
                </div>
            ,
            grow: 2,
        },
    ];

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

        return newErrors;

    }

    const handleSubmit = (id, type) => {
        const newErrors = formValidation();

        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
        } else {
            onSubmit(id, type);
        }
    }

    const onSubmit = (id, type) => {
        if (type === "Tạo mới") {

        } else if (type === "Cập nhật") {

        }
    }

    const handleDelete = (id) => {

    }


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
                            placeholder="Nhập tên người dùng"
                            style={{ fontSize: 14, fontWeight: 400, height: "38px", width: "320px" }}
                            onChange={(e) => setSearchKey(e.target.value)}
                        />
                    </div>
                    <div className="col-4 ps-10">
                        <h5 className="mt-4">{status} thông tin người dùng</h5>
                    </div>

                    <div className="col-8 mt-6 pe-10">
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
                            // onRowClicked={(data) => {
                            //   detail(data);
                            //   handleRowClicked(data);
                            // }}
                            progressComponent={
                                <div style={{ padding: "24px" }}>
                                    <Oval
                                        arialLabel="loading-indicator"
                                        color="#007bff"
                                        height={40}
                                    />
                                </div>
                            }
                        />
                    </div>

                    <div className="col-4 mt-6 ps-10">
                        <Form>
                            <div className="row mb-4">
                                <div className="col-3">
                                    <span className="required">Họ</span>
                                </div>
                                <div className="col-4">
                                    <Form.Control
                                        type="text"
                                        placeholder="Nhập họ"
                                        style={{ fontSize: 13, fontWeight: 400, height: "34px" }}
                                        onChange={(e) => setSearchKey(e.target.value)}
                                    />
                                </div>

                                <div className="col-1">
                                    <span className="required">Tên</span>
                                </div>
                                <div className="col-4">
                                    <Form.Control
                                        type="text"
                                        placeholder="Nhập tên"
                                        style={{ fontSize: 13, fontWeight: 400, height: "34px" }}
                                        onChange={(e) => setSearchKey(e.target.value)}
                                    />
                                </div>

                            </div>

                            <div className="row mb-4">
                                <div className="col-3">
                                    <span className="required">Tên đăng nhập</span>
                                </div>
                                <div className="col-9">
                                    <Form.Control
                                        type="text"
                                        placeholder="Nhập tên người dùng"
                                        style={{ fontSize: 13, fontWeight: 400, height: "34px" }}
                                        onChange={(e) => setSearchKey(e.target.value)}
                                    />
                                </div>
                            </div>

                            <div className="row mb-4">
                                <div className="col-3">
                                    <span className="required">Số điện thoại</span>
                                </div>
                                <div className="col-9">
                                    <Form.Control
                                        type="text"
                                        placeholder="Nhập tên người dùng"
                                        style={{ fontSize: 13, fontWeight: 400, height: "34px" }}
                                        onChange={(e) => setSearchKey(e.target.value)}
                                    />
                                </div>
                            </div>

                            <div className="row mb-4">
                                <div className="col-3">
                                    <span className="required">Email</span>
                                </div>
                                <div className="col-9">
                                    <Form.Control
                                        type="text"
                                        placeholder="Nhập tên người dùng"
                                        style={{ fontSize: 13, fontWeight: 400, height: "34px" }}
                                        onChange={(e) => setSearchKey(e.target.value)}
                                    />
                                </div>
                            </div>

                            <div className="row mb-4">
                                <div className="col-3">
                                    <span className="required">Mật khẩu</span>
                                </div>
                                <div className="col-9">
                                    <Form.Control
                                        type="text"
                                        placeholder="Nhập tên người dùng"
                                        style={{ fontSize: 13, fontWeight: 400, height: "34px" }}
                                        onChange={(e) => setSearchKey(e.target.value)}
                                    />
                                </div>
                            </div>

                            <div className="row mb-4 pt-4">
                                <div className="col-12 text-center">
                                    <button className="btn btn-primary py-3 me-3" style={{ fontSize: "12px", width: "120px" }}><i class="fas fa-save"></i>{status}</button>
                                    <button className="btn btn-secondary py-3 ms-3" style={{ fontSize: "12px", width: "120px" }}><i class="fas fa-undo-alt"></i>Reset</button>
                                </div>
                            </div>

                        </Form>
                    </div>
                </div>
            </div>
        </div>
    )
}