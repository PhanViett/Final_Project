import { FC, useEffect } from "react";
import "react-block-ui/style.css";
import { useSelector } from "react-redux";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { App } from "../App";
import { Logout } from "../modules/apps/auth";
import { ForgotPassword } from "../modules/apps/auth/components/ForgotPassword";
import { Login } from "../modules/apps/auth/Login";
import { Register } from "../modules/apps/auth/Register";
import { ErrorsPage } from "../modules/errors/ErrorsPage";
import { selectCurrentUser } from "../redux-module/auth/authSlice";
import { PrivateRoutes } from "./PrivateRoutes";

const { PUBLIC_URL } = process.env;

const AppRoutes: FC = () => {
    const currentUser = useSelector(selectCurrentUser);
    

    return (
        <BrowserRouter basename={PUBLIC_URL}>
            <Routes>
                <Route element={<App />}>

                    <Route path="dang-nhap/*" element={<Login />} />
                    <Route path="dang-nhap" element={<Login />} />
                    <Route path="dang-ky" element={<Register />} />
                    <Route path="dang-xuat" element={<Logout />} />
                    <Route path="forgot-password" element={<ForgotPassword />} />
                    <Route path="error/*" element={<ErrorsPage />} />

                    {currentUser ?
                        <>
                            <Route path="/*" element={<PrivateRoutes />} />
                        </>
                        :
                        <>
                            <Route path="dang-nhap/*" element={<Login />} />
                            <Route path="*" element={<Navigate to="/dang-nhap" />} />
                        </>
                    }
                </Route>
            </Routes>
            <ToastContainer
                hideProgressBar
                pauseOnFocusLoss
                draggable
                pauseOnHover
                limit={1}
            />
        </BrowserRouter>
    );
};

export { AppRoutes };

