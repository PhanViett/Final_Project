export function News() {

    return (
        <div className="py-3">
            <div className="row py-6" style={{padding: "0 14vw"}}>

                <div className="col-9">
                    <h4 className="fw-bold"> Tin tức</h4>
                </div>
                <div className="col-3">
                    <h4 className="fw-bold"> Tin nổi bật</h4>
                </div>


                {/* IMAGE RAITO 1.875 */}

                <div className="col-9" style={{ textAlign: "center"}}>
                    <div>
                        <img style={{ float: "left", marginRight: "20px" }} width={550} height={293} 
                            src="https://kenh14cdn.com/thumb_w/620/203336854389633024/2022/11/13/photo-1-16683432741632144016447.jpg" alt="" />
                    </div>
                    <p style={{ textAlign: "justify" }}> Gatsby is a black, brown, and white hound mix puppy who loves howling at fire trucks and collecting belly rubs. Although he spends most of his time sleeping he is also quick to chase any birds who enter his vision. Gatsby is a black, brown, and white hound mix puppy who loves howling at fire trucks and collecting belly rubs. Although he spends most of his time sleeping he is also quick to chase any birds who enter his vision.</p>
                </div>

                <div className="col-3 pe-10" style={{ textAlign: "center" }}>
                    <div style={{}}>
                        <img alt="" style={{ width: "100%" }}
                            src="https://kenh14cdn.com/thumb_w/620/203336854389633024/2022/11/12/photo-13-1668269617070918309706.jpg" />
                    </div>
                    <p style={{ textAlign: "justify" }}> Gatsby is a black, brown, and white hound mix puppy who loves howling at fire trucks and collecting belly rubs. Although he spends most of his time sleeping he is also quick to chase any birds who enter his vision.</p>

                </div>


                <div className="col-12 my-10" style={{ border: "1px solid red", marginLeft: "10.5px", marginRight: "10.5px" }}></div>

                <div className="col-12">
                    <div>
                        <img style={{ float: "left", marginRight: "20px" }} width={550} height={293}
                            src="https://kenh14cdn.com/thumb_w/620/203336854389633024/2022/11/13/photo-1-16683432741632144016447.jpg" alt="" />
                    </div>
                    <p style={{ textAlign: "justify" }}> Gatsby is a black, brown, and white hound mix puppy who loves howling at fire trucks and collecting belly rubs. Although he spends most of his time sleeping he is also quick to chase any birds who enter his vision. Gatsby is a black, brown, and white hound mix puppy who loves howling at fire trucks and collecting belly rubs. Although he spends most of his time sleeping he is also quick to chase any birds who enter his vision.</p>
                </div>

            </div>
        </div>
    )
}