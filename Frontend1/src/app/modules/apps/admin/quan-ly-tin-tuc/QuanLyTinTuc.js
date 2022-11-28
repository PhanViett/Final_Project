import axios from "axios";
import { useEffect, useState } from "react";
import { Form, Modal } from "react-bootstrap";
import DataTable from "react-data-table-component";
import { InfinitySpin, Oval } from "react-loader-spinner";
import { conditionalRowStyles, customStyles, paginationOptions } from "../../../../../_metronic/assets/custom/table";
import { useDebounce } from "../../../../../_metronic/helpers";
import api from "../../../../configs/api";

import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import { CKEditor } from "@ckeditor/ckeditor5-react";
import UploadAdapter from "./uploadAdapter";
import { toast } from "react-toastify";
import { BlogStatus } from "../../../../components/BlogStatus";

export function QuanLyTinTuc() {


    const [page, setPage] = useState(1);
    const [perPage, setPerPage] = useState(10);
    const [totalRows, setTotalRows] = useState(0);
    const [isLoading, setIsLoading] = useState(false);

    const [show, setShow] = useState(false);
    const [type, setType] = useState("Thêm mới");
    const [errors, setErrors] = useState({});
    const [searchKey, setSearchKey] = useState("");
    const [tinTucList, setTinTucList] = useState([]);

    const [titleValue, setTitleValue] = useState("");
    const [editorValue, setEditorValue] = useState("");
    const [selectedId, setSelectedId] = useState("");
    const debouncedSearchKey = useDebounce(searchKey, 1000);

    useEffect(() => {
        if (debouncedSearchKey !== undefined && searchKey !== undefined) {
            getList(1, perPage, debouncedSearchKey);
        }
    }, [debouncedSearchKey]);

    const URLUpload = api.API_FILE_UPLOAD

    const config = {
        language: "en",
        placeholder: "Nhập nội dung...",
        extraPlugins: [CustomUploadAdapterPlugin],
    };

    function CustomUploadAdapterPlugin(editor) {
        editor.plugins.get("FileRepository").createUploadAdapter = (loader) => {
            return new UploadAdapter(loader, URLUpload);
        };
    }

    useEffect(() => {
        console.log(editorValue);
    }, [editorValue])

    const handleReset = () => {
        setTitleValue("")
        setEditorValue("")
    }

    const formValidation = () => {
        const newErrors = {};

        if (!titleValue || titleValue === "") {
            newErrors.title = "Tiêu đề không được bỏ trống!"
        }
        if (!editorValue || editorValue === "") {
            newErrors.content = "Nội dung không được bỏ trống!"
        }

        return newErrors
    }

    const getList = ({ page_number = page, size = perPage, search_key = searchKey }) => {
        setIsLoading(true);
        axios
            .post(api.API_QUAN_LY_TIN_TUC + `?page=${page_number}&per_page=${size}`, { search_key: search_key })
            .then(({ data }) => {
                if (data) {
                    let temp_data = data?.results
                    for (let i = 0; i < data?.results.length; i++) {
                        temp_data[i].stt = i + 1
                    }
                    setTinTucList(data?.results)
                    setTotalRows(data?.total)
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
        setIsLoading(true);
        axios
            .post(api.API_QUAN_LY_TIN_TUC + `?page=${page}&per_page=${newPerPage}`, { search_key: searchKey })
            .then(({ data }) => {
                if (data) {
                    let temp_data = data?.results
                    for (let i = 0; i < data?.results.length; i++) {
                        temp_data[i].stt = i + 1
                    }
                    setTinTucList(data?.results)
                    setTotalRows(data?.total)
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
    };

    const handleSubmit = (e, id) => {
        e.preventDefault();

        const newErrors = formValidation();

        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
        } else {
            onSubmit(id);
        }
    }

    const onSubmit = () => {
        setIsLoading(true);
        if (type === "Thêm mới") {
            axios
                .post(api.API_QUAN_LY_TIN_TUC_CREATE, { title: titleValue, content: editorValue, status: 1 })
                .then(({ data }) => {
                    if (data) {
                        toast.success("Lưu bài viết thành công", {
                            position: "top-right",
                            autoClose: 1000,
                            hideProgressBar: false,
                            closeOnClick: true,
                            pauseOnHover: true,
                            draggable: true,
                            progress: undefined,
                            toastId: "error",
                        });
                        setShow(false);
                        getList(1)
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
                });
        } else if (type === "Cập nhật") {
            axios
                .put(api.API_QUAN_LY_TIN_TUC_UPDATE + "/" + selectedId,
                    { title: titleValue, content: editorValue, status: 1 })
                .then(({ data }) => {
                    if (data) {
                        toast.success("Cập nhật thông tin bài viết thành công", {
                            position: "top-right",
                            autoClose: 1000,
                            hideProgressBar: false,
                            closeOnClick: true,
                            pauseOnHover: true,
                            draggable: true,
                            progress: undefined,
                            toastId: "error",
                        });
                        setShow(false);
                        getList(1)
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
                });
        }
    }

    const onDelete = (id) => {
        axios
            .delete(api.API_QUAN_LY_TIN_TUC_DELETE + "/" + id )
            .then(({data}) => {
                toast.success("Xóa tin tức thành công", {
                    position: "top-right",
                    autoClose: 1000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                    toastId: "error",
                });
                getList(1);
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
            });
    }

    const approveOrReject = (data, type) => {
        axios
            .put(api.API_QUAN_LY_TIN_TUC_UPDATE + "/" + data?.id,
                { title: data?.title, content: data?.content, status: type })
            .then(({ data }) => {
                if (data) {
                    toast.success("Cập nhật thông tin bài viết thành công", {
                        position: "top-right",
                        autoClose: 1000,
                        hideProgressBar: false,
                        closeOnClick: true,
                        pauseOnHover: true,
                        draggable: true,
                        progress: undefined,
                        toastId: "error",
                    });
                    setShow(false);
                    getList(1)
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
            });
    }


    const handleDetail = (id) => {
        setIsLoading(true);
        axios
            .post(api.API_QUAN_LY_TIN_TUC_DETAIL, { "id": id })
            .then(({ data }) => {
                if (data) {
                    setSelectedId(data?.results?.id);
                    setTitleValue(data?.results?.title);
                    setEditorValue(data?.results?.content);
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

    const onReset = () => {
        setTitleValue("");
        setEditorValue("");
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
            grow: 2,
            style: {
                cursor: "pointer",
                color: "#202124",
            },
        },
        {
            name: "Tiêu đề",
            selector: (row) => row.title ? <span>{row?.title}</span> : <span className="text-danger"> N/A</span>,
            grow: 8,
            style: {
                cursor: "pointer",
                color: "#202124",
            },
        },
        {
            name: "Trạng thái",
            selector: (row) => row.status ? <BlogStatus status={row?.status} /> : <span className="text-danger"> N/A</span>,
            grow: 2,
            style: {
                cursor: "pointer",
                color: "#202124",
            },
            center: true
        },
        {
            name: "Thao tác",
            selector: (row) =>
                <div className="text-center">
                    <button className="btn btn-link" onClick={() => approveOrReject(row, 2)}><i className="fas fa-check mx-2 text-success"></i></button>
                    <button className="btn btn-link" onClick={() => approveOrReject(row, 3)}><i className="fas fa-times mx-2 text-danger"></i></button>
                    <button className="btn btn-link" onClick={() => { handleDetail(row?.id); setShow(true); setType("Cập nhật") }}><i className="fas fa-edit mx-2 text-primary"></i></button>
                    <button className="btn btn-link" onClick={() => onDelete(row?.id)}><i className="fas fa-trash mx-2 text-danger"></i></button>
                </div>
            ,
            grow: 2,
            style: {
                cursor: "pointer",
                color: "#202124",
            },
            center: true
        },
    ]


    return (
        <div className="py-3">
            <div className="card-box" style={{ padding: "32px" }}>
                <div className="row">
                    <div className="col-12 mb-4">
                        <h4 className="fw-bold">QUẢN LÝ TIN TỨC</h4>
                    </div>

                    <div className="col-8 mt-4 mb-6">
                        <Form.Control
                            type="text"
                            placeholder="Nhập từ khóa tìm kiếm..."
                            style={{ fontSize: 14, fontWeight: 400, height: "38px", width: "320px" }}
                        />
                    </div>
                    <div className="col-4 mt-4 mb-6 text-end">
                        <button className="btn btn-primary py-0" style={{ fontSize: "13px", height: "38px" }} onClick={() => { setShow(true); onReset(); setType("Thêm mới") }}>
                            <i className="fas fa-plus me-1" style={{ fontSize: "12px" }}></i>Tạo mới
                        </button>
                    </div>

                    <div className="col-12">
                        <DataTable
                            noDataComponent={"Không có dữ liệu ..."}
                            sortServer
                            progressPending={isLoading}
                            columns={columns}
                            data={tinTucList}
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

            <Modal show={show} size="lg">
                <Modal.Header className="py-5">
                    <label style={{ fontSize: "18px", fontWeight: 600 }}>{type} tin tức</label>
                </Modal.Header>
                {isLoading ?
                    <div className="d-flex justify-content-center" style={{ alignItems: "center", height: 500, padding: "24px" }}>
                        <InfinitySpin
                            width='200'
                            color="#4fa94d"
                        />
                    </div>
                    :
                    <Modal.Body>
                        <label className="mb-2 required" style={{ fontWeight: 600 }}>Tiêu đề</label>
                        <Form.Control
                            type="text"
                            placeholder="Nhập tiêu đề..."
                            value={titleValue ? titleValue : ""}
                            onChange={(e) => setTitleValue(e.target.value)}
                            style={{ fontWeight: 400, fontSize: "13px", height: "38px" }}
                        />

                        <label className="mt-4 mb-2 required" style={{ fontWeight: 600 }}>Nội dung</label>
                        <CKEditor
                            data={editorValue}
                            editor={ClassicEditor}
                            config={config}
                            onChange={(event, editor) => setEditorValue(editor.getData())}
                        />
                        <div className="row pt-6">
                            {isLoading ? (
                                <div className="col-12 text-center">

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
                                </div>
                            ) : (
                                <div className="col-12 text-center">

                                    <button className="btn btn-secondary btn-bottom-md mx-3" onClick={() => setShow(false)}><i className="fas fa-arrow-circle-left"></i> Quay lại</button>
                                    <button className="btn btn-primary btn-bottom-md mx-3" onClick={() => handleReset()}><i className="fas fa-undo-alt"></i> Reset</button>
                                    <button className="btn btn-success btn-bottom-md mx-3" onClick={(e) => handleSubmit(e)}><i className="fas fa-save"></i> Lưu</button>
                                </div>
                            )}
                        </div>
                    </Modal.Body>
                }
            </Modal>
        </div >
    )
}