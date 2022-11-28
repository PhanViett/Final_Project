import { Select } from "@mui/material";
import axios from "axios";
import moment from "moment";
import { useEffect, useState } from "react";
import { Form, Modal } from "react-bootstrap";
import DataTable from "react-data-table-component";
import { InfinitySpin } from "react-loader-spinner";
import { toast } from "react-toastify";
import { conditionalRowStyles, customStyles, paginationOptions } from "../../../../../_metronic/assets/custom/table";
import { useDebounce } from "../../../../../_metronic/helpers";
import Level from "../../../../components/Level";
import Status from "../../../../components/Status";
import YesNo from "../../../../components/YesNo";
import api from "../../../../configs/api";
import { genderOptions } from "../../../../data";


export function QuanLyLichSu() {

    const [form, setForm] = useState({});

    const [page, setPage] = useState(1);
    const [perPage, setPerPage] = useState(10);
    const [isLoading, setIsLoading] = useState(false);
    const [totalRows, setTotalRows] = useState(0);

    const [show, setShow] = useState(false);
    const [recordList, setRecordList] = useState({});

    const [searchKey, setSearchKey] = useState("");
    const debouncedSearchKey = useDebounce(searchKey, 1000);

    const options = [
        {
            label: "Tất cả",
            value: 3
        },
        {
            label: "Bình thường",
            value: 0
        },
        {
            label: "Không bình thường",
            value: 1
        },
    ]
    const [selected, setSelected] = useState(options[0]);


    useEffect(() => {
        if (debouncedSearchKey !== undefined && searchKey !== undefined) {
            getList(1, perPage, debouncedSearchKey);
        }
    },
        [debouncedSearchKey]
    );

    const getList = (page_number = page, size = perPage, search_key = searchKey) => {
        setIsLoading(true)
        const json = {
            "search_key": search_key,
            "status": selected.value,
        }
        axios
            .post(api.API_QUAN_LY_LICH_SU + `?page=${page_number}&per_page=${size}`, { search_key: search_key })
            .then(({ data }) => {
                let temp_data = data?.results
                for (let i = 0; i < data?.results.length; i++) {
                    temp_data[i].stt = i + 1
                    const gt = genderOptions.find((e) => e.value == temp_data[i].gioi_tinh)
                    temp_data[i].gioi_tinh = gt ? gt.label : "N/A"
                }
                setRecordList(temp_data);
                setTotalRows(data?.total);
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
    }

    const handlePageChange = (page) => {
        setPage(page);
        getList({ page_number: page });
    };

    const handlePerRowsChange = async (newPerPage, page) => {
        setIsLoading(true)
        axios
            .post(api.API_QUAN_LY_LICH_SU + `?page=${page}&per_page=${newPerPage}`, {})
            .then(({ data }) => {
                if (data) {
                    let temp_data = data?.results
                    for (let i = 0; i < data?.results.length; i++) {
                        temp_data[i].stt = i + 1
                        const gt = genderOptions.find((e) => e.value == temp_data[i].gioi_tinh)
                        temp_data[i].gioi_tinh = gt ? gt.label : "N/A"
                    }
                    setRecordList(temp_data);
                    setTotalRows(data?.total);
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

    const handleSelect = (value) => {
        setSelected(value);
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
            name: "Ngày chẩn đoán",
            selector: (row) => row.created_at ? <span>{moment(new Date(row.created_at)).format("hh:mm DD/MM/YYYY")}</span> : <span className="text-danger"> N/A</span>,
            grow: 4,
            center: true
        },
        {
            name: "Giới tính",
            selector: (row) => row.gioi_tinh ? <span>{row?.gioi_tinh}</span> : <span className="text-danger"> N/A</span>,
            grow: 3,
            center: true
        },
        {
            name: "Chiều cao",
            selector: (row) => row.height ? <span>{row?.height}</span> : <span className="text-danger"> N/A</span>,
            grow: 2,
            center: true
        },
        {
            name: "Cân nặng",
            selector: (row) => row.weight ? <span>{row?.weight}</span> : <span className="text-danger"> N/A</span>,
            grow: 2,
            center: true
        },
        {
            name: "Huyết áp",
            selector: (row) => <span>{row?.ap_hi ? row?.ap_hi : ""}/{row?.ap_lo ? row?.ap_lo : ""}</span>,
            grow: 3,
            center: true
        },
        {
            name: "Kết quả",
            selector: (row) => <Status status={row.result} />,
            grow: 3,
            center: true
        },
        {
            name: " ",
            selector: (row) => 
                <button className="btn btn-link me-2"
                    onClick={() => {setForm(row); setShow(true)}}>
                    <i className="fas fa-eye text-primary"></i>
                </button>,
            grow: 1,
        },
    ];

    return (
        <div className="py-3">
            <div className="card-box" style={{ padding: "32px" }}>
                <div className="row">
                    <div className="col-12 mb-4">
                        <h4 className="fw-bold">QUẢN LÝ LỊCH SỬ CHẨN ĐOÁN</h4>
                    </div>

                    <div className="col-3 mt-4 mb-10">
                        <Form.Control
                            type="text"
                            placeholder="Nhập từ khóa tìm kiếm..."
                            style={{ fontSize: 14, fontWeight: 400 }}
                            onChange={(e) => setSearchKey(e.target.value)}
                        />
                    </div>


                    <div className="col-12 mt-6">
                        <DataTable
                            noDataComponent={"Không có dữ liệu ..."}
                            sortServer
                            progressPending={isLoading}
                            columns={columns}
                            data={recordList}
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
                </div>
            </div>

            <Modal show={show} size="lg" onHide={() => {setShow(false)}} style={{paddingTop: "10vh"}}>
                <Modal.Header className="py-4">
                    <label style={{ fontSize: "18px", fontWeight: 600 }}>  Thông tin chi tiết </label>
                </Modal.Header>
                <Modal.Body className="px-10" style={{fontSize: 15}}>
                    <div className="row mb-9">
                        <div className="col-12">
                            <span style={{fontWeight: 500}}>Ngày chẩn đoán:  </span> {moment(new Date(form.created_at)).format("hh:mm:ss  DD/MM/YYYY")}
                        </div>
                    </div>
                    <div className="row mb-6">
                        <div className="col-4">
                            <span style={{ fontWeight: 500 }}>Tuổi:  </span> {form?.tuoi ? Math.round(form?.tuoi/365) : ""} tuổi
                        </div>
                        <div className="col-4">
                            <span style={{ fontWeight: 500 }}>Giới tính:  </span> {form?.gioi_tinh ? form?.gioi_tinh : ""}
                        </div>
                        <div className="col-4">
                            <span style={{ fontWeight: 500 }}>Chiều cao:  </span> {form?.height ? form?.height : ""} cm
                        </div>
                    </div>
                    <div className="row mb-6">
                        <div className="col-4">
                            <span style={{ fontWeight: 500 }}>Cân nặng:  </span> {form?.weight ? form?.height : ""} kg
                        </div>
                        <div className="col-4">
                            <span style={{ fontWeight: 500 }}>Huyết áp tâm trương:  </span> {form?.ap_hi ? form?.ap_hi : ""} mmHg
                        </div>
                        <div className="col-4">
                            <span style={{ fontWeight: 500 }}>Huyết áp tâm thu:  </span> {form?.ap_lo ? form?.ap_lo : ""} mmHg
                        </div>
                    </div>
                    <div className="row mb-6">
                        <div className="col-4">
                            <span style={{ fontWeight: 500 }}>Cholesterol:  </span> <Level value={form?.chol} />
                        </div>
                        <div className="col-4">
                            <span style={{ fontWeight: 500 }}>Glucose:  </span> <Level value={form?.gluc} />
                        </div>
                        <div className="col-4">
                            <span style={{ fontWeight: 500 }}>Chất kích thích:  </span> <YesNo value={form?.smoke} />
                        </div>
                    </div>
                    <div className="row mb-6">
                        <div className="col-4">
                            <span style={{ fontWeight: 500 }}>Chất có cồn:  </span> <YesNo value={form?.alco} />
                        </div>
                        <div className="col-3">
                            <span style={{ fontWeight: 500 }}>Hoạt động:  </span> <YesNo value={form?.active} />
                        </div>
                        <div className="col-5">
                            <span style={{ fontWeight: 500, display: "inline-block", marginRight: 28 }}>Kết quả  </span> <Status status={form?.result} />
                        </div>
                    </div>
                </Modal.Body>
            </Modal>

        </div>
    )
}