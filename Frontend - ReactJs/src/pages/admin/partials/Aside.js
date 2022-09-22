import React, { useEffect, useState } from "react";
import {
  ProSidebar,
  Menu,
  MenuItem,
  SubMenu,
  SidebarHeader,
  SidebarContent,
} from "react-pro-sidebar";
import {
  FaUserInjured,
  FaSyringe,
  FaCrutch,
  FaCog,
  FaRegFolderOpen,
  FaUserCog,
  FaHospitalUser,
  FaTags,
  FaQuestion,
  FaFileAlt,
  FaReadme,
  FaWpforms,
  FaSlidersH,
  FaUsers,
  FaInfoCircle,
  FaMagic,
} from "react-icons/fa";
import { MdAddIcCall } from "react-icons/md";
import { NavLink } from "react-router-dom";
import { BsNewspaper } from "react-icons/bs";
import { useSelector } from "react-redux";
import Version from "../../../time_version_build.json";
import moment from "moment";

const Aside = ({ collapsed, toggled, handleToggleSidebar }) => {
  const permissions = useSelector((state) => state.auth?.permissions);

  const [menuName, setMenuName] = useState(false);
  useEffect(() => {}, []);

  const checkHidden = (value) => {
    let obj = permissions?.[value];
    if (obj) {
      return Object.values(obj).includes(true);
    }
  };

  const viewTabTitle = (name, id, to, icon, type = "main") => {
    if (checkHidden(id)) {
      switch (type) {
        case "main":
          return (
            <Menu iconShape="circle">
              <MenuItem icon={icon}>
                <NavLink to={to} onClick={() => setMenuName(to)}>
                  <button className="dropdown-item text-white" type="button">
                    {name}
                  </button>
                </NavLink>
              </MenuItem>
            </Menu>
          );
        case "sub":
          return (
            <MenuItem icon={icon}>
              <NavLink to={to}>
                <button
                  className="dropdown-item text-white"
                  type="button"
                  onClick={() => setMenuName(to)}
                >
                  {name}
                </button>
              </NavLink>
            </MenuItem>
          );
        default:
          break;
      }
    }
  };
  console.log("menuNamemenuNamemenuName", menuName);
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
            <img
              src="/media/Logo_BoYTe.png"
              width={45}
              className="d-inline-block align-text-center"
            />
            {collapsed ? null : (
              <>
                <div
                  style={{
                    backgroundColor: "#025c95",
                    transition: "all .2s ease-out",
                    position: "absolute",
                    top: "1px",
                    left: "80px",
                  }}
                >
                  <p
                    style={{
                      marginBottom: 0,
                      paddingTop: "0px!important",
                    }}
                    className="text-white p-1"
                  >
                    Sở Y Tế
                  </p>
                  <p
                    style={{
                      marginBottom: 0,
                      paddingTop: "0px!important",
                      fontSize: "18px",
                    }}
                    className="text-white p-1 font-weight-bold"
                  >
                    HỒ CHÍ MINH
                  </p>
                </div>
              </>
            )}
          </NavLink>
        </div>
      </SidebarHeader>

      <SidebarContent>
        {/* {viewTabTitle("Tin tức", "tin_tuc", "tin-tuc", <BsNewspaper />)}
     
        {viewTabTitle(
          "Danh sách đơn vị",
          "don_vi",
          "don-vi",
          <FaHospitalUser />
        )}
      
        {viewTabTitle("Liên hệ", "lien_he", "lien-he", <MdAddIcCall />)}
      
        {viewTabTitle("Quản lý FAQs", "faq", "quan-ly-cau-hoi", <FaQuestion />)}
      
        {viewTabTitle(
          "Quản lý văn bản",
          "van_ban",
          "quan-ly-van-ban",
          <FaReadme />
        )}
       

        <Menu iconShape="circle">
          <MenuItem icon={<FaUsers />}>
            <NavLink
              to="quan-ly-nguoi-dung-mobile"
              onClick={() => setMenuName("quan-ly-nguoi-dung-mobile")}
            >
              <button className="dropdown-item text-white" type="button">
                Người Dùng Mobile
              </button>
            </NavLink>
          </MenuItem>
        </Menu>

        <Menu iconShape="circle">
          <SubMenu
            icon={<FaInfoCircle />}
            title={"Quản lý từ khoá"}
            open={menuName === "quan-ly-tu-khoa" ? true : false}
            onOpenChange={() => setMenuName("quan-ly-tu-khoa")}
          >
            <MenuItem icon={<FaMagic />}>
              <NavLink to="quan-ly-tu-khoa/quan-ly-tu-goi-y">
                <button className="dropdown-item text-white" type="button">
                  Quản lý từ gợi ý
                </button>
              </NavLink>
            </MenuItem>
            <MenuItem icon={<FaMagic />}>
              <NavLink to="quan-ly-tu-khoa/quan-ly-thong-tin-benh">
                <button className="dropdown-item text-white" type="button">
                  Quản lý thông tin bệnh
                </button>
              </NavLink>
            </MenuItem>
          </SubMenu>
        </Menu>
        <Menu iconShape="circle">
          <SubMenu
            icon={<FaFileAlt />}
            title={"Danh mục"}
            open={menuName === "danh-muc" ? true : false}
            onOpenChange={() => setMenuName("danh-muc")}
          >
            {viewTabTitle(
              "Tin tức",
              "danh_muc_tin_tuc",
              "danh-muc-tin-tuc",
              <FaWpforms />,
              "sub"
            )}
         
            {viewTabTitle(
              "Văn bản",
              "danh_muc_van_ban",
              "danh-muc-van-ban",
              <FaReadme />,
              "sub"
            )}
          
            {viewTabTitle(
              "Tag",
              "danh_muc_tag",
              "danh-muc-tag",
              <FaTags />,
              "sub"
            )}
            <MenuItem icon={<FaMagic />}>
              <NavLink to="danh-muc-chuyen-khoa">
                <button className="dropdown-item text-white" type="button">
                  Danh mục chuyên khoa
                </button>
              </NavLink>
            </MenuItem>
          </SubMenu>
        </Menu>
        <Menu iconShape="circle">
          <SubMenu
            icon={<FaRegFolderOpen />}
            title={"Báo cáo"}
            open={menuName === "bao-cao" ? true : false}
            onOpenChange={() => setMenuName("bao-cao")}
          >
            {viewTabTitle(
              "Điều trị",
              "ho_so_dieu_tri",
              "bao-cao/dieu-tri",
              <FaUserInjured />,
              "sub"
            )}
            {viewTabTitle(
              "Nhóm nguy cơ",
              "ho_so_nhom_nguy_co",
              "bao-cao/nhom_nguy_co",
              <FaWpforms />,
              "sub"
            )}        
            {viewTabTitle(
              "Tiêm chủng",
              "ho_so_tiem_chung",
              "bao-cao/tiem-chung",
              <FaSyringe />,
              "sub"
            )}        
            {viewTabTitle(
              "Mắc bệnh",
              "ho_so_mac_benh",
              "bao-cao/mac-benh",
              <FaCrutch />,
              "sub"
            )}         
            {viewTabTitle(
              "Cấp độ dịch",
              "ho_so_cap_do_dich",
              "bao-cao/cap-do-dich",
              <FaCrutch />,
              "sub"
            )}
          </SubMenu>
        </Menu> */}

        <Menu iconShape="circle">
          <SubMenu
            icon={<FaCog />}
            title={"Cài đặt hệ thống"}
            open={menuName === "cai-dat-he-thong" ? true : false}
            onOpenChange={() => setMenuName("cai-dat-he-thong")}
          >
            {/* {permissions?.setting?.manage_home ? (
              <MenuItem icon={<FaWpforms />}>
                <NavLink to="cai-dat-he-thong/quan-ly-trang-chu">
                  <button className="dropdown-item text-white" type="button">
                    Quản lý trang chủ
                  </button>
                </NavLink>
              </MenuItem>
            ) : null}
            {permissions?.setting?.manage_slider ? (
              <MenuItem icon={<FaSlidersH />}>
                <NavLink to="cai-dat-he-thong/quan-ly-sliders">
                  <button className="dropdown-item text-white" type="button">
                    Quản lý sliders
                  </button>
                </NavLink>
              </MenuItem>
            ) : null} */}
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
          Build: #{Version.appVersion} -{" "}
          {moment(Version.timeStamp).format("DD/MM/YYYY")}
        </div>
      </SidebarContent>

      {/* <SidebarFooter style={{ textAlign: 'center' }}>
                <div
                    className="sidebar-btn-wrapper"
                    style={{
                        padding: '20px 24px',
                    }}
                >
                    <a
                        href="https://github.com/azouaoui-med/react-pro-sidebar"
                        target="_blank"
                        className="sidebar-btn"
                        rel="noopener noreferrer"
                    >
                        <FaGithub />
                        <span style={{ whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }}>
                            00
                        </span>
                    </a>
                </div>
            </SidebarFooter> */}
    </ProSidebar>
  );
};
export default Aside;
