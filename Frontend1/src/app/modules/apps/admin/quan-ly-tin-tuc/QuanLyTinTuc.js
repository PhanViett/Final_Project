import axios from "axios";
import { useEffect, useState } from "react";
import { Form, Modal } from "react-bootstrap";
import DataTable from "react-data-table-component";
import { Oval } from "react-loader-spinner";
import { conditionalRowStyles, customStyles, paginationOptions } from "../../../../../_metronic/assets/custom/table";
import { useDebounce } from "../../../../../_metronic/helpers";
import api from "../../../../configs/api";

import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import { CKEditor } from "@ckeditor/ckeditor5-react";
import UploadAdapter from "./uploadAdapter";

export function QuanLyTinTuc() {


    const [page, setPage] = useState(1);
    const [perPage, setPerPage] = useState(1);
    const [totalRows, setTotalRows] = useState(0);
    const [isLoading, setIsLoading] = useState(false);

    const [show, setShow] = useState(false);
    const [type, setType] = useState("Thêm mới");
    const [errors, setErrors] = useState({});
    const [searchKey, setSearchKey] = useState("");
    const [tinTucList, setTinTucList] = useState([]);

    const [titleValue, setTitleValue] = useState("");
    const [editorValue, setEditorValue] = useState("");

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

    const getList = (page_number = page, size = perPage, search_key = searchKey) => {
        axios
            .post(api.API_QUAN_LY_NGUOI_DUNG + `?page=${page_number}&per_page=${size}`, { search_key: search_key })
            .then(({ data }) => {
                if (data) {
                    setTinTucList(data?.results)
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
                    setTinTucList(data?.results);
                    setPerPage(newPerPage);
                }
            })
            .catch(() => { })
            .finally(() => {
            });
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

    const onSubmit = (id) => {
        if (type === "Thêm mới") {

        } else if (type === "Cập nhật") {

        }
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
            name: "Tên người dùng",
            selector: (row) => row.ho_ten ? <span>{row?.ho_ten}</span> : <span className="text-danger"> N/A</span>,
            grow: 8,
            style: {
                cursor: "pointer",
                color: "#202124",
            },
        },
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
            name: "Tên người dùng",
            selector: (row) => row.ho_ten ? <span>{row?.ho_ten}</span> : <span className="text-danger"> N/A</span>,
            grow: 8,
            style: {
                cursor: "pointer",
                color: "#202124",
            },
        },
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
            name: "Thao tác",
            selector: (row) => 
                <div className="text-center">
                    <button className="btn btn-link"><i className="fas fa-edit mx-2 text-primary"></i></button>
                    <button className="btn btn-link"><i className="fas fa-trash mx-2 text-danger"></i></button>
                </div>
            ,
            grow: 8,
            style: {
                cursor: "pointer",
                color: "#202124",
            },
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
                        <button className="btn btn-primary py-0" style={{ fontSize: "13px", height: "38px" }} onClick={() => { setShow(true) }}>
                            <i className="fas fa-plus me-1" style={{fontSize: "12px"}}></i>Tạo mới
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

                    <div className="col-12">
                        <div dangerouslySetInnerHTML={{ __html: editorValue }}></div>
                    </div>
                </div>
            </div>

            <Modal show={show} size="lg">
                <Modal.Header className="py-5">
                    <label style={{ fontSize: "18px", fontWeight: 600 }}>Thêm mới tin tức</label>
                </Modal.Header>
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
                        <div className="col-12 text-center">
                            <button className="btn btn-secondary btn-bottom-md mx-3" onClick={() => setShow(false)}><i className="fas fa-arrow-circle-left"></i> Quay lại</button>
                            <button className="btn btn-primary btn-bottom-md mx-3" onClick={() => handleReset()}><i className="fas fa-undo-alt"></i> Reset</button>
                            <button className="btn btn-success btn-bottom-md mx-3" onClick={(e) => handleSubmit(e)}><i className="fas fa-save"></i> Lưu</button>
                        </div>
                    </div>
                </Modal.Body>
            </Modal>
        </div>
    )
}