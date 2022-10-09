export function HomePage() {


  return (
    <div className="row justify-content-center">

      <div className="col-12 text-center mb-5">
        <img alt="" style={{ width: "calc(100vw - 17px)", height: "36vw", marginLeft: "-3rem" }} src="/media/landing1.jpg" />
      </div>

      <div className="col-12 text-center mt-3 mb-5" style={{ backgroundColor: "red", height: "160px" }}>
        <span style={{ color: "white", fontSize: "24px", fontWeight: 700 }}>LỢI ÍCH KHI SỬ DỤNG HỆ THỐNG</span><br />
      </div>

      <div style={{ display: "contents" }}>
        <div className="col-3 text-center">
          <img alt="" src="/media/Trans_Logo.png" width={45} className="d-inline-block align-text-center" /><br />
          <span>Ô 1</span>
        </div>
        <div className="col-3 text-center">
          <img alt="" src="/media/Trans_Logo.png" width={45} className="d-inline-block align-text-center" /><br />
          <span>Ô 2</span>
        </div>
        <div className="col-3 text-center">
          <img alt="" src="/media/Trans_Logo.png" width={45} className="d-inline-block align-text-center" /><br />
          <span>Ô 3</span>
        </div>
      </div>

      <div className="col-12 text-end mt-5 mb-5" style={{ backgroundColor: "#ffffff" }}>
        <img alt="" style={{ width: "calc(50vw - 8px)", height: "36vw", marginLeft: "-3rem" }} src="/media/landing2.jpg" />
      </div>

      <div className="col-12 text-center mb-5" style={{ backgroundColor: "red", height: "520px" }}>
        <span style={{ color: "white", fontSize: "18px", fontWeight: 600 }}>Theo dõi sức khỏe (Xanh)</span>
      </div>

      <div className="col-12 text-center mb-5" style={{ backgroundColor: "red", height: "520px" }}>
        <span style={{ color: "white", fontSize: "18px", fontWeight: 600 }}>Cập nhật tin tức (Trắng)</span>
      </div>

      <div className="col-12 text-center mb-5" style={{ backgroundColor: "red", height: "520px" }}>
        <span style={{ color: "white", fontSize: "18px", fontWeight: 600 }}>Thích thì đăng ký không thích cũng phải đăng ký đồ đó</span>
      </div>

      <div className="col-12 text-center mt-5" style={{ backgroundColor: "red", height: "520px" }}>
        <span style={{ color: "white", fontSize: "18px", fontWeight: 600 }}>Thông tin liên hệ các thứ đồ đó (Xanh đậm)</span>
      </div>



      {/* <div className="col-12 px-5">
        <h4>Tin tức</h4>
        <div className="col-12 mt-2 mb-4" style={{ height: "1px", margin: "0 -12px", width: "calc(100% + 24px)", backgroundColor: "blue" }}></div>

        <div className="col-12">

          <div>
            <div className="card" style={{ height: "160px" }}>
              <h2>Tin tức 1</h2>
            </div>
            <div className="col-12 my-4 border-bottom" style={{ height: "1px" }}></div>
          </div>

          <div>
            <div className="card" style={{ height: "160px" }}>
              <h2>Tin tức 2</h2>
            </div>
            <div className="col-12 my-4 border-bottom" style={{ height: "1px" }}></div>
          </div>

          <div>
            <div className="card" style={{ height: "160px" }}>
              <h2>Tin tức 3</h2>
            </div>
            <div className="col-12 my-4 border-bottom" style={{ height: "1px" }}></div>
          </div>

        </div>
      </div> */}
    </div>
  )
}