import { Form } from "react-bootstrap";
import { CKEditor } from "@ckeditor/ckeditor5-react";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import UploadAdapter from "../admin/quan-ly-tin-tuc/uploadAdapter";
import api from "../../../configs/api";
import { useEffect, useState } from "react";


export function BlogCreate () {

    const [editorValue, setEditorValue] = useState("");


    // Upload file to MinIO API
    const URLUpload = api.API_FILE_UPLOAD

    useEffect(() => {
        console.log(editorValue);
    }, [editorValue])

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



    return (
        <div className="px-4 py-4">
            <div className="row">
                <div className="col-12">
                    <Form.Control
                        type="text"
                        placeholder="Tiêu đề"
                        style={{ border: "1px solid #fff", fontSize: "28px"}}
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
                <div className="col-6 mt-4" dangerouslySetInnerHTML={{__html: editorValue}}>
                    
                </div>
            </div>
        </div>
    )
}