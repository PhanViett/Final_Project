import { FC, Suspense } from "react";
import { useSelector } from "react-redux";
import { Navigate, Route, Routes } from "react-router-dom";
import TopBarProgress from "react-topbar-progress-indicator";
import { getCSSVariableValue } from "../../_metronic/assets/ts/_utils";
import { MasterLayout } from "../../_metronic/layout/MasterLayout";

import { selectRoleUser } from "../../app/redux-module/auth/authSlice";



import { QuanLyLichSu } from "../modules/apps/admin/quan-ly-lich-su/QuanLyLichSu";
import { QuanLyNguoiDung } from "../modules/apps/admin/quan-ly-nguoi-dung/QuanLyNguoiDung";
import { QuanLyTinTuc } from "../modules/apps/admin/quan-ly-tin-tuc/QuanLyTinTuc";
import { BlogCreate } from "../modules/apps/user/BlogCreate";
import { BlogList } from "../modules/apps/user/BlogList";
import { Diagnostic } from "../modules/apps/user/Diagnostic";
import { Homepage } from "../modules/apps/user/Homepage";
import { Info } from "../modules/apps/user/Info";
import { News } from "../modules/apps/user/News";
import { BlogDetail } from "../modules/apps/user/BlogDetail";

const PrivateRoutes = () => {
    const roleUser = useSelector(selectRoleUser);

    return (
        <Routes>
            <Route element={<MasterLayout />}>
                {/* Redirect to Dashboard after success login/registartion */}
                
                <Route path="dang-nhap/*" element={<Navigate to="/trang-chu" />}/>
                <Route path="/dang-nhap" element={<Navigate to="/trang-chu" />}/>

                {roleUser === "user" ? 
                <Route path="/" element={<Navigate to="" />}
                    />
                : null}

                <Route path="" element={<Homepage />} />
                <Route path="trang-chu" element={<Homepage />} />
                <Route path="admin/quan-ly-nguoi-dung" element={<QuanLyNguoiDung />} />
                <Route path="admin/quan-ly-lich-su" element={<QuanLyLichSu />} />
                <Route path="admin/quan-ly-tin-tuc" element={<QuanLyTinTuc />} />

                <Route path="tin-tuc/:id" element={<BlogDetail />} />
                <Route path="tin-tuc/viet-bai" element={<BlogCreate />} />
                <Route path="tin-tuc/danh-sach" element={<BlogList />} />

                <Route path="thong-tin-ca-nhan" element={<Info />} />
                <Route path="chan-doan" element={<Diagnostic />} />
                <Route path="tin-tuc" element={<News />} />


                {/* Page Not Found */}
                {/* <Route path="*" element={<Navigate to="/error/404" />} /> */}

            </Route>
        </Routes>
    );
};

const SuspensedView: FC = ({ children }) => {
    const baseColor = getCSSVariableValue("--bs-primary");
    TopBarProgress.config({
        barColors: {
            "0": baseColor,
        },
        barThickness: 1,
        shadowBlur: 5,
    });
    return <Suspense fallback={<TopBarProgress />}>{children}</Suspense>;
};

export { PrivateRoutes };

