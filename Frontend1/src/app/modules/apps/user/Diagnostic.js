export function Diagnostic () {


    return (
        <div className="py-3">
            <div className="card-box" style={{ padding: "32px" }}>
                <div className="row">
                    <div className="col-12 mb-4">
                        <h4 className="fw-bold">CHẨN ĐOÁN</h4>
                    </div>
                
                    <div className="col-9 mt-4 mb-10">
                        <h5 className="fw-bold">Thông tin hiện tại</h5>

                    </div>

                    <div className="col-3 mt-4 mb-10 text-end">
                        <button className="btn btn-primary py-0" style={{ fontSize: "13px", height: "38px" }}>
                            <i className="fas fa-plus me-1" style={{ fontSize: "12px" }}></i>Cập nhật
                        </button>
                    </div>


                    <div className="row">
                        <div className="col-4">
                            <span style={{fontWeight: 500}}>Họ tên: </span>
                            <span>Phan Văn Việt</span>
                        </div>
                        <div className="col-4">
                            <span style={{ fontWeight: 500 }}>Họ tên: </span>
                            <span>Phan Văn Việt</span>
                        </div>
                        <div className="col-4">
                            <span style={{ fontWeight: 500 }}>Họ tên: </span>
                            <span>Phan Văn Việt</span>
                        </div>
                    </div>



                </div>
            </div>
        </div>
    )
}