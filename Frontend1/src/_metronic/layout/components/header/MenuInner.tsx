import { MenuItem } from "./MenuItem";
import { useSelector } from "react-redux";
import { useEffect, useState } from "react";
import { MenuInnerWithSub } from "./MenuInnerWithSub";
import { selectRoleUser } from "../../../../app/redux-module/auth/authSlice";

export function MenuInner() {
  const [roles, setRoles] = useState<any | undefined>();
  const roleUser = useSelector(selectRoleUser);

  useEffect(() => {
    if (roleUser) {
      setRoles(roleUser[0]?.ten_en);
    }
  }, [roleUser]);

  return (
    <>
      {/* Nộp hồ sơ */}
      {roles &&
      (roles === "duocsi" || roles === "tochuc" || roles === "admin") ? (
        <MenuItem
          to="/admin/nop-ho-so/danh-sach-ho-so"
          title="Nộp hồ sơ"
          fontIcon="fa fa-copy"
        />
      ) : null}
      {/* Chứng chỉ HN-D */}
      {roles && (roles === "duocsi" || roles === "admin") ? (
        <MenuItem
          title="Chứng chỉ HN-D"
          fontIcon="fa fa-scroll"
          to="/admin/chung-chi-hanh-nghe"
        />
      ) : null}
      {/* Giấy phép ĐKKDD */}
      {roles && (roles === "tochuc" || roles === "admin") ? (
        <MenuItem
          to="/admin/giay-phep-kinh-doanh"
          title="Giấy phép ĐKKDD"
          fontIcon="fa fa-file-alt"
        />
      ) : null}
      {/* Quản lý CCHN-D  */}
      {roles &&
      (roles === "admin" ||
        roles === "lanhdao" ||
        roles === "chuyenvien" ||
        roles === "chuyenvienhoidong" ||
        roles === "vanthu") ? (
        <MenuInnerWithSub
          to="/apps"
          fontIcon="fa fa-scroll"
          title="Quản lý CCHN-D"
          menuPlacement="bottom-start"
          menuTrigger="click"
        >
          {/* PAGES */}
          {roles === "chuyenvien" || roles === "lanhdao" ? (
            <MenuItem
              icon="/media/icons/duotune/general/gen051.svg"
              to="/admin/yeu-cau-lien-ket-duoc-si"
              title="Danh sách liên kết"
            />
          ) : null}
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/danhsach-hoso-thuly-duocsi"
            title="Danh sách hồ sơ"
          />
          {roles === "lanhdao" ? (
            <MenuItem
              icon="/media/icons/duotune/general/gen051.svg"
              to="/admin/danhsach-hoso-pheduyet-duocsi"
              title="Danh sách chờ phê duyệt"
            />
          ) : null}
          {roles === "vanthu" ? (
            <MenuItem
              icon="/media/icons/duotune/general/gen051.svg"
              to="/admin/danhsach-hoso-pheduyet-duocsi"
              title="Danh sách cấp số"
            />
          ) : null}
          {roles !== "vanthu" ? (
            <MenuItem
              icon="/media/icons/duotune/general/gen051.svg"
              to="/admin/danhsach-hoso-choin-duocsi"
              title="Danh sách chờ in"
            />
          ) : null}
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/danh-sach-chung-chi"
            title="Danh sách chứng chỉ"
          />
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/danhsach-hoidong"
            title="Danh sách hội dồng"
          />
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/loai-ma-chung-chi"
            title="Loại mã chứng chỉ"
          />
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/thong-tin-dao-tao"
            title="Thông tin đào tạo"
          />
        </MenuInnerWithSub>
      ) : null}
      {/* Quản lí giấy phép ĐKKDD */}
      {roles &&
      (roles === "admin" ||
        roles === "lanhdao" ||
        roles === "chuyenvien" ||
        roles === "chuyenvienhoidong" ||
        roles === "vanthu") ? (
        <MenuInnerWithSub
          to="/apps"
          fontIcon="fa fa-scroll"
          title="Giấy phép ĐKKDD"
          menuPlacement="bottom-start"
          menuTrigger="click"
        >
          {/* PAGES */}
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/yeu-cau-lien-ket-to-chuc"
            title="Danh sách liên kết"
          />
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/danhsach-hoso-thuly-tochuc"
            title="Danh sách hồ sơ"
          />
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/danhsach-hoso-pheduyet-tochuc"
            title="Danh sách chờ phê duyệt"
          />
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/danhsach-hoso-choin-tochuc"
            title="Danh sách hồ sơ chờ in"
          />
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/apps/user-management/users"
            title="Danh sách giấy phép"
          />
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/loai-ma-gps"
            title="Loại mã GPs"
          />
        </MenuInnerWithSub>
      ) : null}
      {/* Danh mục */}
      {roles && (roles === "admin" || roles === "lanhdao") ? (
        <MenuInnerWithSub
          title="Danh mục"
          to="/apps"
          menuPlacement="bottom-start"
          menuTrigger="click"
          fontIcon="fa fa-list-alt"
        >
          {/* PAGES */}
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/danh-muc/loai-hinh-kinh-doanh"
            title="Loại hình kinh doanh"
          />
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/danh-muc/noi-tot-nghiep"
            title="Nơi tốt nghiệp"
          />
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/danh-muc/vi-tri-hanh-nghe"
            title="Vị trí hành nghề"
          />
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/danh-muc/hoi-dong"
            title="Hội đồng"
          />
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/danh-muc/van-bang-chuyen-mon"
            title="Văn bằng chuyên môn"
          />
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/danh-muc/pham-vi-hoat-dong-kinh-doanh"
            title="Phạm vi hoạt động kinh doanh"
          />

          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/danh-muc/hoat-dong-chuyen-mon"
            title="Hoạt động chuyên môn"
          />
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/danh-muc/thanh-phan-ho-so"
            title="Thành phần hồ sơ"
          />
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/danh-muc/chung-nhan-thuc-hanh-co-so"
            title="Chứng nhận thực hành cơ sở"
          />
          <MenuItem
            icon="/media/icons/duotune/general/gen051.svg"
            to="/admin/danh-muc/thu-tuc"
            title="Thủ tục"
          />
        </MenuInnerWithSub>
      ) : null}
      {/* Thông báo */}
      <MenuItem
        to="/thong-bao"
        title="Thông báo"
        fontIcon="fa fa-bell"
        // hasBullet
      />
    </>
  );
}
