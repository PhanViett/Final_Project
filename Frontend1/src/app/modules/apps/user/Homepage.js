export function Homepage() {


    return (
        <div className="row">
            <div className="col-12 ps-8 mt-4 mb-8">
                <span style={{ fontSize: "25px", fontWeight: 600 }}>Dashboard</span>
            </div>

            <div className="col-3 px-10">
                <div className="d-flex text-end bg-danger px-10 pt-7 pb-7" style={{ justifyContent: "space-between", borderRadius: "7px" }}>
                    <i class="fas fa-user text-white" style={{ fontSize: "60px" }}></i>
                    <div>
                        <label className="text-white" style={{ fontSize: "14px", fontWeight: "400" }}>Số người dùng</label> <br />
                        <label className="text-white mt-4" style={{ fontSize: "24px", fontWeight: "600" }}>1000</label>
                    </div>
                </div>
            </div>

            <div className="col-3 px-10">
                <div className="d-flex text-end bg-success px-10 pt-7 pb-7" style={{ justifyContent: "space-between", borderRadius: "7px" }}>
                    <i class="fas fa-file-image text-white" style={{ fontSize: "60px" }}></i>
                    <div>
                        <label className="text-white" style={{ fontSize: "14px", fontWeight: "400" }}>Số tin tức</label> <br />
                        <label className="text-white mt-4" style={{ fontSize: "24px", fontWeight: "600" }}>1000</label>
                    </div>
                </div>
            </div>

            <div className="col-3 px-10">
                <div className="d-flex text-end bg-warning px-10 pt-7 pb-7" style={{ justifyContent: "space-between", borderRadius: "7px" }}>
                    <i class="fas fa-stethoscope text-white" style={{ fontSize: "60px" }}></i>
                    <div>
                        <label className="text-white" style={{ fontSize: "14px", fontWeight: "400" }}>Số lượt chẩn đoán</label> <br />
                        <label className="text-white mt-4" style={{ fontSize: "24px", fontWeight: "600" }}>1000</label>
                    </div>
                </div>
            </div>

            <div className="col-3 px-10">
                <div className="d-flex text-end bg-primary px-10 pt-7 pb-7" style={{ justifyContent: "space-between", borderRadius: "7px" }}>
                    <i class="fas fa-heartbeat text-white" style={{ fontSize: "60px" }}></i>
                    <div>
                        <label className="text-white" style={{ fontSize: "14px", fontWeight: "400" }}>Tỷ lệ chẩn đoán tích cực</label> <br />
                        <label className="text-white mt-4" style={{ fontSize: "24px", fontWeight: "600" }}>1000</label>
                    </div>
                </div>
            </div>

            <div className="col-12 ps-8 mt-8 mb-8">
                <span style={{ fontSize: "25px", fontWeight: 600 }}>Tin tức</span>
            </div>


        </div>
    )
}