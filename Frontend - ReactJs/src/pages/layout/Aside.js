import React, { useState } from "react";
import {
  FaCog, FaUserCog
} from "react-icons/fa";
import {
  Menu,
  MenuItem, ProSidebar, SidebarContent, SidebarHeader, SubMenu
} from "react-pro-sidebar";
import { useSelector } from "react-redux";
import { NavLink } from "react-router-dom";

const Aside = ({ collapsed, toggled, handleToggleSidebar }) => {
  const permissions = useSelector((state) => state.auth?.permissions);

  const [menuName, setMenuName] = useState(false);

  return (
    <ProSidebar
      image={false}
      collapsed={collapsed}
      toggled={toggled}
      breakPoint="md"
      id="sidebar"
      onToggle={handleToggleSidebar}
    >
      <SidebarHeader>
        <div
          style={{
            padding: "12px",
            textTransform: "uppercase",
            fontSize: 14,
            letterSpacing: "1px",
            overflow: "hidden",
            height: "65px",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
          }}
        >
          <NavLink className="" to="/admin">
            <img alt="" src="/media/Trans_Logo.png" width={45} className="d-inline-block align-text-center" />
            {collapsed ? null : (
              <>
                <div
                  style={{
                    backgroundColor: "#000",
                    transition: "all .2s ease-out",
                    position: "absolute",
                    top: "1px",
                    left: "80px",
                  }}
                > </div>
              </>
            )}
          </NavLink>
        </div>
      </SidebarHeader>

      <SidebarContent>
        <Menu iconShape="circle">
          <MenuItem icon={<FaUserCog />}>
            <NavLink to="quan-ly-nguoi-dung">
              <button className="dropdown-item text-white" type="button">
                Quản lý người dùng
              </button>
            </NavLink>
          </MenuItem>

          <MenuItem icon={<FaUserCog />}>
            <NavLink to="quan-ly-tin-tuc">
              <button className="dropdown-item text-white" type="button">
                Quản lý tin tức
              </button>
            </NavLink>
          </MenuItem>

          <SubMenu
            icon={<FaCog />}
            title={"Cài đặt hệ thống"}
            open={menuName === "cai-dat-he-thong" ? true : false}
            onOpenChange={() => setMenuName("cai-dat-he-thong")}
          >
            <MenuItem icon={<FaUserCog />}>
              <NavLink to="cai-dat-he-thong/vai-tro">
                <button className="dropdown-item text-white" type="button">
                  Phân quyền
                </button>
              </NavLink>
            </MenuItem>
          </SubMenu>
        </Menu>
        <div
          style={{
            position: "absolute",
            bottom: 5,
            left: "15%",
            color: "#ffffff",
          }}
        >
        </div>
      </SidebarContent>
    </ProSidebar>
  );
};
export default Aside;
