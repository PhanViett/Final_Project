import { useState } from "react";
import { Form } from "react-bootstrap";

export function Diagnostic () {


    const [isUpdate, setIsUpdate] = useState(false);

    return (
        <div className="py-3">
            <div className="card-box" style={{ padding: "32px" }}>
                <div className="row">
                    <div className="col-12 mb-8">
                        <h4 className="fw-bold">CHẨN ĐOÁN TÌNH TRẠNG</h4>
                    </div>
                
                    <div className="col-9 mt-8">
                        <h5 className="fw-bold">Thông tin hiện tại</h5>
                    </div>

                    <div className="col-3 mb-10 text-end">
                        {isUpdate === false ? 
                            <button className="btn btn-primary py-0" style={{ fontSize: "13px", height: "38px" }} onClick={() => setIsUpdate(true)}>
                                <i className="fas fa-plus me-1" style={{ fontSize: "12px" }}></i>Cập nhật
                            </button>
                        :
                            <button className="btn btn-primary py-0" style={{ fontSize: "13px", height: "38px" }} onClick={() => setIsUpdate(false)}>
                                <i className="fas fa-plus me-1" style={{ fontSize: "12px" }}></i>Lưu
                            </button>
                        }

                    </div>


                    <div className="row mx-1 mb-4">
                        <div className="col-3">
                            <span className="d-block mb-1" style={{fontWeight: 500}}>Họ tên: </span>
                            {isUpdate === false ? 
                                <span>Phan Văn Việt</span>
                            :
                                <Form.Control
                                    type="text"
                                    value="Phan Văn Việt"
                                />
                            }
                        </div>
                        <div className="col-3">
                            <span className="d-block mb-1" style={{ fontWeight: 500 }}>Tuổi: </span>
                            {isUpdate === false ?
                                <span>Phan Văn Việt</span>
                                :
                                <Form.Control
                                    type="text"
                                    value="Phan Văn Việt"
                                />
                            }
                        </div>
                        <div className="col-3">
                            <span className="d-block mb-1" style={{ fontWeight: 500 }}>Giới tính: </span>
                            {isUpdate === false ?
                                <span>Phan Văn Việt</span>
                                :
                                <Form.Control
                                    type="text"
                                    value="Phan Văn Việt"
                                />
                            }
                        </div>
                        <div className="col-3">
                            <span className="d-block mb-1" style={{ fontWeight: 500 }}>Chiều cao: </span>
                            {isUpdate === false ?
                                <span>Phan Văn Việt</span>
                                :
                                <Form.Control
                                    type="text"
                                    value="Phan Văn Việt"
                                />
                            }
                        </div>
                    </div>                    
                    <div className="row mx-1 mb-4">
                        <div className="col-3">
                            <span className="d-block mb-1" style={{ fontWeight: 500 }}>Cân nặng: </span>
                            {isUpdate === false ?
                                <span>Phan Văn Việt</span>
                                :
                                <Form.Control
                                    type="text"
                                    value="Phan Văn Việt"
                                />
                            }
                        </div>
                        <div className="col-3">
                            <span className="d-block mb-1" style={{ fontWeight: 500 }}>Chiều cao: </span>
                            {isUpdate === false ?
                                <span>Phan Văn Việt</span>
                                :
                                <Form.Control
                                    type="text"
                                    value="Phan Văn Việt"
                                />
                            }
                        </div>
                        <div className="col-3">
                            <span className="d-block mb-1" style={{ fontWeight: 500 }}>Cân nặng: </span>
                            {isUpdate === false ?
                                <span>Phan Văn Việt</span>
                                :
                                <Form.Control
                                    type="text"
                                    value="Phan Văn Việt"
                                />
                            }
                        </div>
                        <div className="col-3">
                            <span className="d-block mb-1" style={{ fontWeight: 500 }}>Cholesterol: </span>
                            {isUpdate === false ?
                                <span>Phan Văn Việt</span>
                                :
                                <Form.Control
                                    type="text"
                                    value="Phan Văn Việt"
                                />
                            }
                        </div>
                    </div>
                    <div className="row mx-1 mb-4">
                        <div className="col-3">
                            <span className="d-block mb-1" style={{ fontWeight: 500 }}>Glucose: </span>
                            {isUpdate === false ?
                                <span>Phan Văn Việt</span>
                                :
                                <Form.Control
                                    type="text"
                                    value="Phan Văn Việt"
                                />
                            }
                        </div>
                        <div className="col-3">
                            <span className="d-block mb-1" style={{ fontWeight: 500 }}>Smoke: </span>
                            {isUpdate === false ?
                                <span>Phan Văn Việt</span>
                                :
                                <Form.Control
                                    type="text"
                                    value="Phan Văn Việt"
                                />
                            }
                        </div>
                        <div className="col-3">
                            <span className="d-block mb-1" style={{ fontWeight: 500 }}>Alcohol: </span>
                            {isUpdate === false ?
                                <span>Phan Văn Việt</span>
                                :
                                <Form.Control
                                    type="text"
                                    value="Phan Văn Việt"
                                />
                            }
                        </div>
                        <div className="col-3">
                            <span className="d-block mb-1" style={{ fontWeight: 500 }}>Activity: </span>
                            {isUpdate === false ?
                                <span>Phan Văn Việt</span>
                                :
                                <Form.Control
                                    type="text"
                                    value="Phan Văn Việt"
                                />
                            }
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}