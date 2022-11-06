import axios from "axios";
import { useEffect, useState } from "react";
import { Form } from "react-bootstrap";
import DataTable from "react-data-table-component";
import { Oval } from "react-loader-spinner";
import { conditionalRowStyles, customStyles, paginationOptions } from "../../../../../_metronic/assets/custom/table";
import { useDebounce } from "../../../../../_metronic/helpers";
import api from "../../../../configs/api";

// http://localhost:5000/api/v1/record-get-list
export function QuanLyLichSu() {

    const [page, setPage] = useState(1);
    const [perPage, setPerPage] = useState(1);
    const [isLoading, setIsLoading] = useState(false);
    const [totalRows, setTotalRows] = useState(0);

    const [recordList, setRecordList] = useState({});

    const [searchKey, setSearchKey] = useState("");

    const [render, setRender] = useState({});

    const debouncedSearchKey = useDebounce(searchKey, 1000);

    useEffect(() => {
        aaaa()
    }, [])

    useEffect(() => {
        if (debouncedSearchKey !== undefined && searchKey !== undefined) {
            getList(1, perPage, debouncedSearchKey);
        }
    },
        [debouncedSearchKey]
    );

    const getList = (page_number = page, size = perPage, search_key = searchKey) => {
        axios
            .post(api.API_QUAN_LY_LICH_SU + `?page=${page_number}&per_page=${size}`, { search_key: search_key })
            .then(({ data }) => {
                if (data) {
                    setRecordList(data?.results)
                }
            })
    }

    const handlePageChange = (page) => {
        setPage(page);
        getList({ page_number: page });
    };

    const handlePerRowsChange = async (newPerPage, page) => {
        axios
            .post(api.API_QUAN_LY_LICH_SU, {})
            .then(({ data }) => {
                if (data) {
                    setRecordList(data?.results);
                    setPerPage(newPerPage);
                }
            })
            .catch(() => { })
            .finally(() => {
            });
    };


    const aaaa = () => {
        axios
            .post("http://localhost:5000/menu", {})
            .then(({data}) => {
                if (data) {
                    setRender(data)
                }
            })
    }

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
                            placeholder="Nhập tên người dùng"
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
                            // onRowClicked={(data) => {
                            //   detail(data);
                            //   handleRowClicked(data);
                            // }}
                            progressComponent={
                                <div
                                    style={{
                                        padding: "24px",
                                    }}
                                >
                                    <Oval
                                        arialLabel="loading-indicator"
                                        color="#007bff"
                                        height={40}
                                    />
                                </div>
                            }
                        />
                    </div>
                </div>
            </div>
        </div>
    )
}