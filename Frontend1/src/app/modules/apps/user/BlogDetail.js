import axios from "axios";
import moment from "moment";
import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import api from "../../../configs/api";
import { selectBlogDetail } from "../../../redux-module/common/commonSlice";

export function BlogDetail() {
    const params = useParams();

    const [data, setData] = useState(useSelector(selectBlogDetail))


    useEffect(() => {
        if (data) {
            console.log(data);
        } else {
            handleDetail(params?.id)
        }
    }, [data])

    const handleDetail = (id) => {
        axios
            .post(api.API_QUAN_LY_TIN_TUC_DETAIL, { "id": id })
            .then(({ data }) => {
                if (data) {
                    setData(data?.results)
                }
            })
    }

    return (
        <div className="px-4 py-4">
            <div className="row justify-content-center">
                <div className="col-8">
                    <label style={{ fontSize: 36, fontWeight: 800 }}>{data?.title}</label>
                </div>
                <div className="col-8">
                    <label className="mt-6 font-weight-bold" style={{ fontSize: 18 }}>{data?.ref_name ? data?.ref_name : "N/A"}</label>
                    <span>&nbsp; - &nbsp;</span>
                    <label className="mt-6" style={{ fontSize: 17, color: "#9fa2ae" }}>{data?.updated_at ? moment(new Date(Number(data?.updated_at))).format("hh:mm DD/MM/YYYY") : "N/A"}</label>
                </div>
                <div className="col-7 mt-10">
                    <label style={{fontSize: 18}} dangerouslySetInnerHTML={{__html: data?.content}}></label>
                </div>
            </div>
        </div>
    )
}