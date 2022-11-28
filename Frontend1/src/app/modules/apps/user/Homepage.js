import axios from "axios";
import { useEffect, useState } from "react";
import Skeleton, { SkeletonTheme } from "react-loading-skeleton";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import api from "../../../configs/api";
import { commonActions } from "../../../redux-module/common/commonSlice";

export function Homepage() {
    const dispatch = useDispatch();
    const navigate = useNavigate
    ();

    const [blogFirst, setBlogFirst] = useState([]);
    const [blogRemain, setBlogRemain] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        getList();
    }, [])


    const handleDetail = (id) => {
        axios
            .post(api.API_QUAN_LY_TIN_TUC_DETAIL, { "id": id })
            .then(({ data }) => {
                if (data) {
                    console.log(data?.result);
                    dispatch(commonActions.setBlogDetail(data?.result));
                    navigate(`/tin-tuc/${id}`)
                }
            })
    }

    const getList = () => {
        setIsLoading(true);
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

                    let temp_remain_list = []
                    for (let i = 0; i < 2; i++) {
                        let temp_remain = data?.remain[i]
                        let a = temp_remain?.content.split(" ")
                        let b = []
                        for (let i = 0; i < 20; i++) {
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
        <div className="row">
            <div className="col-12 ps-8 mt-4 mb-8">
                <span style={{ fontSize: "25px", fontWeight: 600 }}>Dashboard</span>
            </div>

            <div className="col-3 px-10">
                <div className="d-flex text-end bg-danger px-10 pt-7 pb-7" style={{ justifyContent: "space-between", borderRadius: "7px" }}>
                    <i className="fas fa-user text-white" style={{ fontSize: "60px" }}></i>
                    <div>
                        <label className="text-white" style={{ fontSize: "14px", fontWeight: "400" }}>Số người dùng</label> <br />
                        <label className="text-white mt-4" style={{ fontSize: "24px", fontWeight: "600" }}>1000</label>
                    </div>
                </div>
            </div>

            <div className="col-3 px-10">
                <div className="d-flex text-end bg-success px-10 pt-7 pb-7" style={{ justifyContent: "space-between", borderRadius: "7px" }}>
                    <i className="fas fa-file-image text-white" style={{ fontSize: "60px" }}></i>
                    <div>
                        <label className="text-white" style={{ fontSize: "14px", fontWeight: "400" }}>Số tin tức</label> <br />
                        <label className="text-white mt-4" style={{ fontSize: "24px", fontWeight: "600" }}>1000</label>
                    </div>
                </div>
            </div>

            <div className="col-3 px-10">
                <div className="d-flex text-end bg-warning px-10 pt-7 pb-7" style={{ justifyContent: "space-between", borderRadius: "7px" }}>
                    <i className="fas fa-stethoscope text-white" style={{ fontSize: "60px" }}></i>
                    <div>
                        <label className="text-white" style={{ fontSize: "14px", fontWeight: "400" }}>Số lượt chẩn đoán</label> <br />
                        <label className="text-white mt-4" style={{ fontSize: "24px", fontWeight: "600" }}>1000</label>
                    </div>
                </div>
            </div>

            <div className="col-3 px-10">
                <div className="d-flex text-end bg-primary px-10 pt-7 pb-7" style={{ justifyContent: "space-between", borderRadius: "7px" }}>
                    <i className="fas fa-heartbeat text-white" style={{ fontSize: "60px" }}></i>
                    <div>
                        <label className="text-white" style={{ fontSize: "14px", fontWeight: "400" }}>Tỷ lệ chẩn đoán tích cực</label> <br />
                        <label className="text-white mt-4" style={{ fontSize: "24px", fontWeight: "600" }}>1000</label>
                    </div>
                </div>
            </div>

            <div className="col-12 ps-8 mt-8 mb-8">
                <span style={{ fontSize: "25px", fontWeight: 600 }}>Tin tức</span>
            </div>

            <div className="col-7 ps-10">
                {isLoading ?
                    <div className="row">
                        <div className="col-7">
                            <SkeletonTheme color="#5e6c77" highlightColor="#a9b7c1">
                                <Skeleton count={1} style={{ width: "100%" }} height={320} />
                            </SkeletonTheme>
                        </div>
                        <div className="col-5">
                            <SkeletonTheme color="#5e6c77" highlightColor="#a9b7c1">
                                <Skeleton count={2} height={36} />
                                <Skeleton count={1} height={36} style={{ width: "40%" }} />
                            </SkeletonTheme>
                            <br />
                            <SkeletonTheme color="#5e6c77" highlightColor="#a9b7c1">
                                <Skeleton count={2} height={20} />
                                <Skeleton count={1} height={20} style={{ width: "80%" }} />
                                <br />
                                <Skeleton count={2} height={20} />
                                <Skeleton count={1} height={20} style={{ width: "80%" }} />
                            </SkeletonTheme>
                        </div>
                    </div>
                    :
                    <div className="row" onClick={() => handleDetail(blogFirst?.id)}>
                        <div className="col-7" style={{cursor: "pointer"}}>
                            {blogFirst?.thumbnail ?
                                <img alt="" style={{ width: "100%" }} height={320} src="/media/blank-image.jpg" />
                                :
                                <img alt="" style={{ width: "100%" }} height={320} src="/media/blank-image.jpg" />
                            }
                        </div>
                        <div className="col-5">
                            <label className="font-weight-bold mb-6" style={{ fontSize: "28px", cursor: "pointer" }}>{blogFirst?.title}</label> <br />
                            <label dangerouslySetInnerHTML={{ __html: blogFirst?.short }} style={{ fontSize: 15, cursor: "pointer" }}></label>
                        </div>
                    </div>
                }
            </div>
            <div className="col-5">
                {isLoading ?
                    <>
                        <div className="row mb-4">
                            <div className="col-4">
                                <SkeletonTheme color="#5e6c77" highlightColor="#a9b7c1">
                                    <Skeleton count={1} style={{ width: "100%" }} height={144} />
                                </SkeletonTheme>
                            </div>
                            <div className="col-8">
                                <SkeletonTheme color="#5e6c77" highlightColor="#a9b7c1">
                                    <Skeleton count={1} height={30} />
                                    <Skeleton count={1} height={30} style={{ width: "60%" }} />
                                </SkeletonTheme>
                                <br />
                                <SkeletonTheme color="#5e6c77" highlightColor="#a9b7c1">
                                    <Skeleton count={1} height={18} />
                                    <Skeleton count={1} height={18} style={{ width: "80%" }} />
                                </SkeletonTheme>
                            </div>
                        </div>

                        <div className="row">
                            <div className="col-4">
                                <SkeletonTheme color="#5e6c77" highlightColor="#a9b7c1">
                                    <Skeleton count={1} style={{ width: "100%" }} height={144} />
                                </SkeletonTheme>
                            </div>
                            <div className="col-8">
                                <SkeletonTheme color="#5e6c77" highlightColor="#a9b7c1">
                                    <Skeleton count={1} height={30} />
                                    <Skeleton count={1} height={30} style={{ width: "60%" }} />

                                </SkeletonTheme>
                                <br />
                                <SkeletonTheme color="#5e6c77" highlightColor="#a9b7c1">
                                    <Skeleton count={1} height={18} />
                                    <Skeleton count={1} height={18} style={{ width: "80%" }} />
                                </SkeletonTheme>
                            </div>
                        </div>
                    </>
                    :
                    <>
                        <div className="row mb-4" style={{ cursor: "pointer" }} onClick={() => handleDetail(blogRemain[0].id)}>
                            <div className="col-4">
                                {blogRemain[0]?.thumbnail ?
                                    <img alt="" height={46} width={46} src="/media/blank-image.jpg" />
                                    :
                                    <img alt="" style={{ width: "100%" }} height={144} src="/media/blank-image.jpg" />
                                }
                            </div>
                            <div className="col-8">
                                <label className="font-weight-bold mb-4" style={{ fontSize: "20px", cursor: "pointer" }}>{blogRemain[0]?.title}</label> <br />
                                <label dangerouslySetInnerHTML={{ __html: blogRemain[0]?.short }} style={{ fontSize: 15, cursor: "pointer" }}></label>
                            </div>
                        </div>

                        <div className="row" style={{ cursor: "pointer" }}>
                            <div className="col-4">
                                {blogRemain[1]?.thumbnail ?
                                    <img alt="" height={46} width={46} src="/media/blank-image.jpg" />
                                    :
                                    <img alt="" style={{ width: "100%" }} height={144} src="/media/blank-image.jpg" />
                                }
                            </div>
                            <div className="col-8">
                                <label className="font-weight-bold mb-4" style={{ fontSize: "20px", cursor: "pointer" }}>{blogRemain[1]?.title}</label> <br />
                                <label dangerouslySetInnerHTML={{ __html: blogRemain[1]?.short }} style={{ fontSize: 15, cursor: "pointer" }}></label>
                            </div>
                        </div>
                    </>
                }
            </div>

        </div>
    )
}