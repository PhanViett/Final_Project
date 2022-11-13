export function Homepage() {


    return (
        <div className="row">
            <div className="col-12 ps-8 mt-4 mb-8">
                <span style={{fontSize: "25px", fontWeight: 600}}>Dashboard</span>
            </div>

            <div className="col-3 px-9">
                <div className="text-end px-6 pt-7 pb-10" style={{ backgroundColor: "green" }}>
                    <span className="text-white">Số người dùng</span>
                </div>
            </div>

            <div className="col-3 px-9">
                <div className="text-end px-6 pt-7 pb-10" style={{ backgroundColor: "red" }}>
                    <span className="text-white">Số tin tức</span>
                </div>
            </div>

            <div className="col-3 px-9">
                <div className="text-end px-6 pt-7 pb-10" style={{ backgroundColor: "violet" }}>
                    <span className="text-white">Số chẩn đoán</span>
                </div>
            </div>

            <div className="col-3 px-9">
                <div className="text-end px-6 pt-7 pb-10" style={{ backgroundColor: "yellow" }}>
                    <span className="text-white">Tỷ lệ chẩn đoán tốt</span>
                </div>
            </div>

            <div className="col-12 ps-8 mt-8 mb-8">
                <span style={{ fontSize: "25px", fontWeight: 600 }}>Tin tức</span>
            </div>


        </div>
    )
}