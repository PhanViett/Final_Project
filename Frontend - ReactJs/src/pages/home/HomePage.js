export function HomePage() {


  return (
    <div className="row justify-content-center">
      <div className="col-12 text-center mb-5" style={{ backgroundColor: "red", height: "320px" }}>
        <span style={{ color: "white", fontSize: "18px", fontWeight: 600 }}>Carousel</span>
      </div>
      <div className="col-12 px-5">
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
      </div>
    </div>
  )
}