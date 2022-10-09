import { useState } from "react";
import DataTable from "react-data-table-component";
import { Oval } from "react-loader-spinner";
import { conditionalRowStyles, customStyles, handlePerRowsChange, paginationOptions } from "../../../assets/customStyles/stylesTable";

export function NewMain() {

    const [isLoading, setIsLoading] = useState(false);
    const [totalRows, setTotalRows] = useState(0);


    const handlePageChange = async (page) => {
        // await setPage(page);
        // getList({ page_number: page });
    };




    const columns = [
        {
            name: "STT",
            grow: 3,
            selector: (row) => (<span>{row.ma_chuyen_mon}</span>),
            style: {
                color: "#1251ff",
                fontSize: "14px",
                fontWeight: 500,
                width: 300,
                cursor: "pointer",
            },
        },
        {
            name: "Tên người dùng",
            selector: (row) => <span>{row.ten}</span>,
            grow: 8,
            style: {
                cursor: "pointer",
                color: "#202124",
            },
        },
        {
            name: "Giới tính",
            selector: (row) => <span>{row.trang_thai}</span>,
            grow: 3,
        },
        {
            name: "Số điện thoại",
            selector: (row) => <span>{row.trang_thai}</span>,
            grow: 2,
        },
        {
            name: "Vai trò",
            selector: (row) => <span>{row.trang_thai}</span>,
            grow: 2,
        },
        {
            name: "",
            selector: (row) => <span>{row.trang_thai}</span>,
            grow: 2,
        },
    ];

    return (
        <div className="py-3">
            <div className="card-box">
                <div className="row">
                    <div className="col-12">
                        <h5 className="text-secondary fw-bolder">QUẢN LÝ NGƯỜI DÙNG</h5>
                    </div>

                    <div className="col-12">

                        <DataTable
                            noDataComponent={"Không có dữ liệu ..."}
                            sortServer
                            progressPending={isLoading}
                            columns={columns}
                            data={[]}
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