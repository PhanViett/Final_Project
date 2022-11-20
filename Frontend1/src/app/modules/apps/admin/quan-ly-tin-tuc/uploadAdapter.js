import axios from "axios";
import { toast } from "react-toastify";

export default class UploadAdapter {
    constructor(loader, url) {
        this.url = url;
        this.loader = loader;
        this.loader.file.then((pic) => (this.file = pic));
        this.upload();
    }

    // Starts the upload process.
    upload() {
        if (this.file !== undefined && this.file !== "undefined") {
            const fd = new FormData();
            fd.append("dinh_kem[]", this.file);

            return new Promise((resolve, reject) => {
                axios
                    .post(this.url, fd, { headers: {"content-type": "multipart/form-data"} })
                    .then(({ data }) => {
                        if (data) {
                            resolve({
                                uploaded: true,
                                fileName: data[0]?.url,
                                url: `http://127.0.0.1:9000/${data[0]?.url}`,
                                default: `http://127.0.0.1:9000/${data[0]?.url}`,
                            });
                        }

                    })
                    .catch((error) => {
                        toast.error("Tải file thất bại", {
                            position: "top-right",
                            autoClose: 1000,
                            hideProgressBar: false,
                            closeOnClick: true,
                            pauseOnHover: true,
                            draggable: true,
                            progress: undefined,
                            toastId: "error",
                        });
                    });
            });
        }
    }
}
