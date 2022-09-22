import React from "react";
import { useRoutes } from "react-router-dom";
//login
import { LoginPage } from "../pages/admin/auth/LoginPage";
//admin
import { UserInfo } from "../pages/admin/auth/UserInfo";
import { LayoutAdmin } from "../pages/admin/layout";
import { AddRole } from "../pages/admin/roles/AddRole";
//error
import { Page404 } from "../pages/admin/partials/404";

let routers = [
  {
    path: "/",
    element: <LoginPage />,
    children: [{ index: true, element: <LoginPage /> }],
  },
  {
    path: "/admin",
    breadcrumb: "Trang chủ",
    element: <LayoutAdmin />,
    children: [
      // { index: true, element: <ListRoles /> },
      {
        path: "cai-dat-he-thong",
        breadcrumb: "Cài đặt hệ thống",
        children: [
          {
            path: "vai-tro",
            children: [
              // {
              //   path: "",
              //   breadcrumb: "Vai trò",
              //   element: <ListRoles />,
              // },
              {
                path: "create",
                element: <AddRole />,
              },
            ],
          },
        ],
      },

      {
        path: "thong-tin-tai-khoan",
        children: [
          {
            path: "",
            breadcrumb: "Thông tin tài khoản",
            element: <UserInfo />,
          },
        ],
      },
      { path: "404", element: <Page404 /> },
    ],
  },
];

function RootRouteObject() {
  return useRoutes(routers);
}

export { RootRouteObject, routers };
