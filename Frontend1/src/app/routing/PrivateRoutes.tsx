import { FC, Suspense } from "react";
import { useSelector } from "react-redux";
import { Navigate, Route, Routes } from "react-router-dom";
import TopBarProgress from "react-topbar-progress-indicator";
import { getCSSVariableValue } from "../../_metronic/assets/ts/_utils";
import { MasterLayout } from "../../_metronic/layout/MasterLayout";

import { selectRoleUser } from "../../app/redux-module/auth/authSlice";
import { QuanLyNguoiDung } from "../modules/apps/admin/quan-ly-nguoi-dung/QuanLyNguoiDung";

const PrivateRoutes = () => {
    const roleUser = useSelector(selectRoleUser);

    return (
        <Routes>
            <Route element={<MasterLayout />}>
                {/* Redirect to Dashboard after success login/registartion */}
                <Route path="/" element={<Navigate to="/admin/quan-ly-nguoi-dung" />} />

                <Route path="dang-nhap/*" element={<Navigate to="/dashboard" />}/>
                <Route path="/dang-nhap" element={<Navigate to="/dashboard" />}/>

                {roleUser === "user" ? 
                <Route path="/" element={<Navigate to="/admin/quan-ly-nguoi-dung" />}
                    />
                : null}

                <Route path="admin/quan-ly-nguoi-dung" element={<QuanLyNguoiDung />} />

                {/* Page Not Found */}
                <Route path="*" element={<Navigate to="/error/404" />} />

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

