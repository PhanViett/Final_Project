import axios from "axios";
import { useEffect, useState } from "react";
import { Dropdown } from "react-bootstrap";
import DataTable from "react-data-table-component";
import { Oval } from "react-loader-spinner";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { conditionalRowStyles, customStyles, paginationOptions } from "../../../../_metronic/assets/custom/table";
import api from "../../../configs/api";
import { commonActions, selectBlogDetail } from "../../../redux-module/common/commonSlice";


export function BlogList() {
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const blogDetail = useSelector(selectBlogDetail)

    const [page, setPage] = useState(1);
    const [perPage, setPerPage] = useState(10);
    const [totalRows, setTotalRows] = useState(0);
    const [isLoading, setIsLoading] = useState(false);

    const [active, setActive] = useState(1);
    const [blogList, setBlogList] = useState([]);



    useEffect(() => {
        getList(1, perPage);
        dispatch(commonActions.setBlogDetail({}));
    }, [])


    const getList = ({ page_number = page, size = perPage }) => {
        axios
            .post(api.API_QUAN_LY_TIN_TUC + `?page=${page_number}&per_page=${size}`, { "status": active })
            .then(({ data }) => {
                if (data) {
                    let list = data?.results;
                    for (let x = 0; x < list.length; x++) {
                        list[x].stt = x + 1;
                    }
                    setBlogList(list);
                    setTotalRows(data?.totalRows)
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
    }


    const handlePageChange = (page) => {
        setPage(page);
        getList({ page_number: page });
    };

    const handlePerRowsChange = async (newPerPage, page) => {
        axios
            .post(api.API_QUAN_LY_TIN_TUC + `?page=${page}&per_page=${newPerPage}`, { "status": active })
            .then(({ data }) => {
                if (data) {
                    let list = data?.results;
                    for (let x = 0; x < list.length; x++) {
                        list[x].stt = x + 1;
                    }
                    setBlogList(list)
                    setTotalRows(data?.totalRows)``
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
            .finally(() => { });
    };

    const getBlogDetail = (id) => {
        axios
            .post(api.API_QUAN_LY_TIN_TUC_DETAIL, {"id": id})
            .then(({data}) => {
                if (data) {
                    dispatch(commonActions.setBlogDetail(data?.results))
                    navigate("/tin-tuc/viet-bai")
                }
            })
    }

    const blogDelete = (id) => {
        axios
            .delete(api.API_QUAN_LY_TIN_TUC_DELETE + "/" + id)
            .then(({data}) =>{
                if (data) {
                    toast.success("Xóa bài viết thành công", {
                        position: "top-right",
                        autoClose: 1000,
                        hideProgressBar: false,
                        closeOnClick: true,
                        pauseOnHover: true,
                        draggable: true,
                        progress: undefined,
                        toastId: "error",
                    });
                    if (page === 1) {
                        getList({ page_number: 1 });
                    } else if (blogList?.length === 1) {
                        getList({ page_number: page - 1 });
                    } else {
                        getList({ page_number: page });
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
    }

    const columns = [
        {
            name: "STT",
            selector: (row) => <span>{row.stt}</span>,
            grow: 1,
            center: true,
            style: {
                cursor: "pointer",
                color: "#202124",
            },
        },
        {
            name: "Tiêu đề",
            selector: (row) => row.title ? <span>{row?.title}</span> : <span className="text-danger"> N/A</span>,
            grow: 8,
        },
        {
            name: "Nguồn tham khảo",
            center: true,
            selector: (row) => row.ref_name ? <span>{row?.ref_name}</span> : <span className="text-danger"> N/A</span>,
            grow: 3,
        },
        {
            name: "Trạng thái",
            center: true,
            selector: (row) => row.status ? <span>{row?.status}</span> : <span className="text-danger"> N/A</span>,
            grow: 2,
        },
        {
            name: "",
            grow: 2,
            center: true,
            selector: (row) =>
                blogList.length === 1 ? (
                    <div className="d-flex px-0">
                        <button
                            className="btn btn-link"
                            title="Chỉnh sửa"
                            onClick={() => {
                                getBlogDetail(row?.id)
                            }}
                        >
                            <i className="fas fa-eye text-primary me-3"></i>
                        </button>
                        <button
                            className="btn btn-link"
                            title="Xóa"
                            onClick={() => {
                            }}
                        >
                            <i className="fas fa-trash text-danger me-3"></i>
                        </button>
                    </div>
                ) : (
                    <div className="container my-3">
                        <Dropdown>
                            <Dropdown.Toggle variant="link" style={{ float: "right" }}>
                                <i
                                    className="fas fa-bars"
                                    style={{ marginLeft: "3px", marginRight: "-3px" }}
                                ></i>
                            </Dropdown.Toggle>

                            <Dropdown.Menu flip={true} bsPrefix="dropdown-menu dropdown-box">
                                <Dropdown.Item
                                    onClick={() => {
                                    }}
                                >
                                    <i className="fas fa-eye text-primary me-3"></i>Cập nhật
                                </Dropdown.Item>
                                <Dropdown.Item
                                    onClick={() => {
                                    }}
                                >
                                    <i className="fas fa-trash text-danger me-3"></i>Xóa
                                </Dropdown.Item>
                            </Dropdown.Menu>
                        </Dropdown>
                    </div>
                ),
        },
    ];

    const tabStyle = {
        width: 140,
        fontSize: 18,
        fontWeight: 500,
        cursor: "pointer",
        paddingBottom: 10,
        color: '#0000008a',
        textAlign: 'center',

    }

    const tabStyleActive = {
        width: 140,
        fontSize: 18,
        fontWeight: 700,
        cursor: "pointer",
        paddingBottom: 10,
        textAlign: 'center',
        borderBottom: "2px solid black"
    }

    return (
        <div className="px-4 py-4">
            <div className="row px-10">
                <h1>Bài viết của tôi</h1>

                <div className="col-8 d-flex border-bottom" style={{ marginTop: 120 }}>
                    <div style={active === 1 ? tabStyleActive : tabStyle} onClick={() => setActive(1)}>Bản nháp</div>
                    <div style={active === 2 ? tabStyleActive : tabStyle} onClick={() => setActive(2)}>Chờ xuất bản</div>
                    <div style={active === 3 ? tabStyleActive : tabStyle} onClick={() => setActive(3)}>Đã xuất bản</div>
                </div>
                <div className="col-8">
                    <DataTable
                        noDataComponent={"Không có dữ liệu ..."}
                        sortServer
                        progressPending={isLoading}
                        columns={columns}
                        data={blogList}
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
                        onRowClicked={(data) => {
                            getBlogDetail(data?.id)
                        }}
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
            </div>
        </div>
    )
}