import axios from "axios";
import { useEffect, useState } from "react"
import api from "../../../configs/api";
import Skeleton, { SkeletonTheme } from "react-loading-skeleton";


export function News() {

    const [isLoading, setIsLoading] = useState(false)

    const [blogFirst, setBlogFirst] = useState([]);
    const [blogSecond, setBlogSecond] = useState([]);
    const [blogRemain, setBlogRemain] = useState([]);

    useEffect(() => {
        getList();
    }, [])

    const getList = () => {
        setIsLoading(true)
        axios
            .post(api.API_QUAN_LY_TIN_TUC_LIST_VIEW, {})
            .then(({ data }) => {
                if (data) {
                    let temp_most = data?.most
                    let a = temp_most?.content.split(" ")
                    let b = []
                    for (let i = 0; i < 60; i++) {
                        if (a[i]) {
                            b.push(a[i])
                        }
                    }
                    temp_most.short = b.join(" ") + "....</p>"
                    setBlogFirst(temp_most)


                    let temp_second = data?.remain[0]
                    let c = temp_second?.content.split(" ")
                    let d = []
                    for (let i = 0; i < 20; i++) {
                        if (c[i]) {
                            d.push(c[i])
                        }
                    }
                    temp_second.short = d.join(" ") + "....</p>"
                    setBlogSecond(temp_second)


                    let temp_remain_list = []
                    for (let i = 1; i < data?.remain.length; i++) {
                        let temp_remain = data?.remain[i]
                        console.log(temp_remain);
                        let a = temp_remain?.content.split(" ")
                        let b = []
                        for (let i = 0; i < 60; i++) {
                            if (a[i]) {
                                b.push(a[i])
                            }
                        }
                        temp_remain.short = b.join(" ") + "....</p>"
                        temp_remain_list.push(temp_remain)
                    }
                    setBlogRemain(temp_remain_list)

                    setIsLoading(false)
                }
            })
    }

    return (
        <div className="py-3">
            {isLoading ?
                <div className="row py-6" style={{ padding: "0 14vw" }}>
                    <div className="col-9">
                        <h2 className="fw-bold"> Tin tức</h2>
                    </div>
                    <div className="col-3">
                        <h2 className="fw-bold"> Tin nổi bật</h2>
                    </div>


                    {/* IMAGE RAITO 1.875 */}
                    <div className="col-4 pe-5">
                        <SkeletonTheme color="#5e6c77" highlightColor="#a9b7c1">
                            <Skeleton count={1} width={550} height={293} />
                        </SkeletonTheme>
                    </div>

                    <div className="col-5" style={{ paddingLeft: "160px !important" }}>
                        <SkeletonTheme color="#5e6c77" highlightColor="#a9b7c1">
                            <Skeleton count={2} height={36} />
                            <Skeleton count={1} height={36} style={{ width: "80%" }} />
                            <br />
                            <Skeleton count={2} height={20} />
                            <Skeleton count={1} height={20} style={{ width: "30%" }} />
                            <br />
                            <Skeleton count={2} height={20} />
                            <Skeleton count={1} height={20} style={{ width: "50%" }} />
                        </SkeletonTheme>

                    </div>

                    <div className="col-3 pe-10">
                        <SkeletonTheme color="#5e6c77" highlightColor="#a9b7c1">
                            <Skeleton count={1} style={{width: "100%"}} height={180} />
                        </SkeletonTheme>
                        <SkeletonTheme color="#5e6c77" highlightColor="#a9b7c1">
                            <Skeleton count={1} height={36} />
                            <Skeleton count={1} height={36} style={{ width: "80%" }} />
                            <br />
                            <Skeleton count={2} height={20} />
                            <Skeleton count={1} height={20} style={{ width: "60%" }} />
                        </SkeletonTheme>
                    </div>


                    <div className="col-12 my-10" style={{ border: "1px solid red", marginLeft: "10.5px", marginRight: "10.5px" }}></div>
                    
                    <div className="col-6 mb-4">
                        <SkeletonTheme color="#5e6c77" highlightColor="#a9b7c1">
                            <Skeleton count={1} width={550} height={293} />
                        </SkeletonTheme>
                    </div>

                    <div className="col-6 mb-4" style={{ marginLeft: "-50px" }}>
                        <SkeletonTheme color="#5e6c77" highlightColor="#a9b7c1">
                            <Skeleton count={2} height={36} style={{ width: "108%" }} />
                            <Skeleton count={1} height={36} style={{ width: "90%" }} />
                            <br />
                            <Skeleton count={3} height={20} style={{ width: "108%" }} />
                            <Skeleton count={1} height={20} style={{ width: "90%" }} />
                        </SkeletonTheme>
                    </div>

                    <div className="col-6 mb-4">
                        <SkeletonTheme color="#5e6c77" highlightColor="#a9b7c1">
                            <Skeleton count={1} width={550} height={293} />
                        </SkeletonTheme>
                    </div>

                    <div className="col-6 mb-4" style={{marginLeft: "-50px"}}>
                        <SkeletonTheme color="#5e6c77" highlightColor="#a9b7c1">
                            <Skeleton count={2} height={36} style={{ width: "108%" }} />
                            <Skeleton count={1} height={36} style={{ width: "90%" }} />
                            <br />
                            <Skeleton count={3} height={20} style={{ width: "108%" }} />
                            <Skeleton count={1} height={20} style={{ width: "90%" }} />
                        </SkeletonTheme>
                    </div>

                </div>
                :
                <div className="row py-6" style={{ padding: "0 14vw" }}>
                    <div className="col-9">
                        <h2 className="fw-bold"> Tin tức</h2>
                    </div>
                    <div className="col-3">
                        <h2 className="fw-bold"> Tin nổi bật</h2>
                    </div>


                    {/* IMAGE RAITO 1.875 */}
                    <div className="col-9 pe-5">
                        <div>
                            {blogFirst?.thumbnail ?
                                <img style={{ float: "left", marginRight: "20px" }} width={550} height={293}
                                    src="https://kenh14cdn.com/thumb_w/620/20333685438" alt="" />
                                :
                                <img style={{ float: "left", marginRight: "20px" }} width={550} height={293}
                                    src="/media/blank-image.jpg" alt="" />
                            }
                        </div>
                        <p className="font-weight-bold" style={{ fontSize: 24 }}>{blogFirst.title}</p>
                        <p style={{ textAlign: "justify" }} dangerouslySetInnerHTML={{ __html: blogFirst.short }}></p>
                    </div>

                    <div className="col-3 pe-10">
                        <div>
                            {blogFirst?.thumbnail ?
                                <img alt="" style={{ width: "100%" }}
                                    src="https://kenh14cdn.com/thumb_w/620/203336854389633024/2022/11/12/photo-13-1668269617070918309706.jpg" />
                                :
                                <img alt="" style={{ width: "100%" }} height={180}
                                    src="/media/blank-image.jpg" />
                            }
                        </div>
                        <p className="font-weight-bold" style={{ fontSize: 16 }}>{blogSecond.title}</p>
                        <p style={{ textAlign: "justify" }} dangerouslySetInnerHTML={{ __html: blogSecond.short }}></p>
                    </div>


                    <div className="col-12 my-10" style={{ border: "1px solid red", marginLeft: "10.5px", marginRight: "10.5px" }}></div>

                    {blogRemain && blogRemain.length > 0 ? blogRemain.map((e, i) => {
                        return (
                            <div className="col-12 mb-4" key={`remain_${i}`}>
                                <div>
                                    <img style={{ float: "left", marginRight: "20px" }} width={550} height={293}
                                        src="https://kenh14cdn.com/thumb_w/620/203336854389633024/2022/11/13/photo-1-16683432741632144016447.jpg" alt="" />
                                </div>
                                <p className="font-weight-bold" style={{ fontSize: 22 }}>{blogRemain[i].title}</p>
                                <p style={{ textAlign: "justify" }} dangerouslySetInnerHTML={{ __html: blogRemain[i].short }}></p>                            </div>
                        )
                    }) : null}
                </div>
            }


        </div>
    )
}