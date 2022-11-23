import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import { CKEditor } from "@ckeditor/ckeditor5-react";
import axios from "axios";
import { useEffect, useState } from "react";
import { Form } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import api from "../../../configs/api";
import { commonActions, selectBlogDetail } from "../../../redux-module/common/commonSlice";
import UploadAdapter from "../admin/quan-ly-tin-tuc/uploadAdapter";


export function BlogCreate() {
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const blogDetail = useSelector(selectBlogDetail);

    const [currId, setCurrId] = useState("");

    const [titleValue, setTitleValue] = useState("");
    const [editorValue, setEditorValue] = useState("");


    // Upload file to MinIO API
    const URLUpload = api.API_FILE_UPLOAD

    useEffect(() => {
        if (Object.keys(blogDetail).length > 0) {
            setTitleValue(blogDetail?.title)
            setEditorValue(blogDetail?.content)
        }
        console.log(blogDetail);
    }, [blogDetail])

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

    const findFormErrors = () => {
        const newErrors = {};
        if (!titleValue || titleValue === "") {
            newErrors.title = "Tiêu đề không được bỏ trống!"
        }
        if (!editorValue || editorValue === "") {
            newErrors.content = "Nội dung không được bỏ trống!"
        }

        return newErrors;
    }

    const handleSubmit = (type) => {
        const newErrors = findFormErrors();

        if (Object.keys(newErrors).length > 0 && type === 2) {
            if (newErrors.title) {
                toast.error(newErrors?.title, {
                    position: "top-right",
                    autoClose: 1000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                    toastId: "error",
                });
            }
            if (newErrors.content) {
                toast.error(newErrors?.content, {
                    position: "top-right",
                    autoClose: 1000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                    toastId: "error",
                });
            }

        } else {
            if (type === 1 && currId === "") {
                axios
                    .post(api.API_QUAN_LY_TIN_TUC_CREATE,
                        { title: titleValue, content: editorValue })
                    .then(({ data }) => {
                        if (data) {
                            setCurrId(data?.results?.id);
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
            }
            else {
                axios
                    .put(api.API_QUAN_LY_TIN_TUC_UPDATE + "/" + currId,
                        { title: titleValue, content: editorValue, status: type })
                    .then(({ data }) => {
                        if (data) {
                            const text = type === 1 ? "Lưu bài viết thành công" : type === 2 ? "Đề nghị xuất bản bài viết thành công" : ""
                            setCurrId(data?.results?.id);
                            toast.success(text, {
                                position: "top-right",
                                autoClose: 1000,
                                hideProgressBar: false,
                                closeOnClick: true,
                                pauseOnHover: true,
                                draggable: true,
                                progress: undefined,
                                toastId: "error",
                            });
                            if (type === 2) {
                                navigate("/tin-tuc/danh-sach")
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
        }
    }


    return (
        <div className="px-4 py-4">
            <div className="row">
                <div className="col-12">
                    <Form.Control
                        type="text"
                        placeholder="Tiêu đề"
                        value={titleValue}
                        onChange={(e) => setTitleValue(e.target.value)}
                        style={{ border: "1px solid #fff", fontSize: "28px" }}
                    />
                </div>
                <div className="col-6 mt-4">
                    <CKEditor
                        config={config}
                        editor={ClassicEditor}
                        data={editorValue}
                        onChange={(event, editor) => setEditorValue(editor.getData())}
                    />
                </div>

                <div className="ck-editor5-content col-6 mt-4" dangerouslySetInnerHTML={{ __html: editorValue }}></div>

                <div className="col-12 mt-10 text-center">
                    <button className="btn btn-secondary btn-bottom-sm mx-3" onClick={(e) => { navigate(-1) }}>Quay lại</button>
                    <button className="btn btn-success btn-bottom-sm mx-3" onClick={(e) => { handleSubmit(1) }}>Lưu nháp</button>
                    <button className="btn btn-primary btn-bottom-sm mx-3" onClick={(e) => { handleSubmit(2) }}>Xuất bản</button>
                </div>
            </div>
        </div>
    )
}