import React, { useEffect, useState } from "react";
import CheckboxTree from "react-checkbox-tree";
import { useDispatch } from "react-redux";
// import { setTitle } from "../../../saga-modules/common/actions";

import Switch from "@material-ui/core/Switch";

export function AddRole() {
  const dispatch = useDispatch();

  const [checkall, setCheckAll] = useState([]);
  const [checked, setChecked] = useState([]);
  const [isCheck, setIsCheck] = useState(false);
  const [expanded, setExpanded] = useState([]);
  const [ArrayRoles, setArrayRoles] = useState([]);

  useEffect(() => {
    // dispatch(setTitle({ title: "Thêm mới vai trò" }));

    // setCheckedValue();
  }, []);

  const setCheckedValue = () => {
    let value = [];

    console.log(checked);
    for (let node of nodes) {
      value.push(node.value);
      if (node.children !== undefined) {
        for (let n of node.children) {
          value.push(n.value);
          if (n.children !== undefined) {
            for (let m of n.children) {
              value.push(m.value);
            }
          }
        }
      }
    }
    console.log("log note", nodes);
    setCheckAll(value);
  };

  const nodes = [
    {
      value: "nguoi_dung",
      label: "Người dùng",
      children: [
        {
          value: "nguoi_dung.create",
          label: "Tạo",
          checked: false,
        },
        {
          value: "nguoi_dung.update",
          label: "Cập nhật",
          checked: false,
        },
        {
          value: "nguoi_dung.get",
          label: "Xem",
          checked: false,
        },
        {
          value: "nguoi_dung.delete",
          label: "Xóa",
          checked: false,
        },
      ],
    },
    {
      value: "vai_tro",
      label: "Vai trò",
      children: [
        {
          value: "vai_tro.create",
          label: "Tạo",
          checked: false,
        },
        {
          value: "vai_tro.update",
          label: "Cập nhật",
          checked: false,
        },
        {
          value: "vai_tro.get",
          label: "Xem",
          checked: false,
        },
        {
          value: "vai_tro.delete",
          label: "Xóa",
          checked: false,
        },
        {
          value: "vai_tro.assign_role",
          label: "Bổ nhiệm chức vụ",
          checked: false,
        },
        {
          value: "vai_tro.unassign",
          label: "Tước chức vụ",
          checked: false,
        },
      ],
    },
    {
      value: "authentication",
      label: "Xác thực",
      children: [
        {
          value: "authentication.change_password",
          label: "Đổi mật khẩu",
          checked: false,
        },
        {
          value: "authentication.refresh",
          label: "Làm mới token",
          checked: false,
        },
        {
          value: "authentication.revoke_token",
          label: "Xóa token",
          checked: false,
        },
        {
          value: "authentication.revoke_refresh",
          label: "Tước quyền làm mới token",
          checked: false,
        },
      ],
    },
    {
      value: "danh_muc",
      label: "Danh mục",
      children: [
        {
          value: "danh_muc.create",
          label: "Tạo",
          checked: false,
        },
        {
          value: "danh_muc.update",
          label: "Cập nhật",
          checked: false,
        },
        {
          value: "danh_muc.get",
          label: "Xem",
          checked: false,
        },
        {
          value: "danh_muc.delete",
          label: "Xóa",
          checked: false,
        },
      ],
    },
    {
      value: "faq",
      label: "FAQ",
      children: [
        {
          value: "faq.create",
          label: "Tạo",
          checked: false,
        },
        {
          value: "faq.update",
          label: "Cập nhật",
          checked: false,
        },
        {
          value: "faq.get",
          label: "Xem",
          checked: false,
        },
        {
          value: "faq.delete",
          label: "Xóa",
          checked: false,
        },
      ],
    },
    {
      value: "don_vi",
      label: "Đơn vị",
      children: [
        {
          value: "don_vi.create",
          label: "Tạo",
          checked: false,
        },
        {
          value: "don_vi.update",
          label: "Cập nhật",
          checked: false,
        },
        {
          value: "don_vi.get",
          label: "Xem",
          checked: false,
        },
        {
          value: "don_vi.delete",
          label: "Xóa",
          checked: false,
        },
      ],
    },
  ];
  return (
    <div className="page">
      <div className="container">
        <div className="row justify-content-center mb-4">
          <div className="col-8 mb-3">
            <div className="card">
              <div className="card-body">
                <form>
                  <div className="form-group">
                    <label>
                      Tên vai trò <span className="text-danger"> (*) </span>
                    </label>
                    <input className="form-control" placeholder="Tên vai trò" />
                  </div>
                  <div className="form-group">
                    <label>
                      Ghi chú <span className="text-danger"> (*) </span>
                    </label>
                    <textarea
                      className="form-control"
                      rows={4}
                      placeholder="Ghi chú"
                    />
                  </div>
                </form>

                <Switch defaultChecked color="primary" />
              </div>
            </div>
          </div>
          <div className="col-8 mb-3">
            <div className="card">
              <div className="card-body">
                {!isCheck ? (
                  <button
                    className="btn btn-primary float-right"
                    style={{ fontSize: "14px" }}
                    onClick={() => {
                      setIsCheck(true);
                      setChecked(checkall);
                      console.log(checked);
                    }}
                  >
                    <i class="fas fa-check"></i> Check all
                  </button>
                ) : (
                  <button
                    className="btn btn-primary float-right"
                    style={{ fontSize: "14px" }}
                    onClick={() => {
                      setChecked([]);
                      setIsCheck(false);
                      console.log(checked);
                    }}
                  >
                    <i class="fas fa-times"></i> Uncheck all
                  </button>
                )}

                <CheckboxTree
                  nodes={nodes}
                  checked={checked}
                  expanded={expanded}
                  onCheck={async (checked, node) => {
                    console.log("checked", checked);
                    // console.log("node", node);
                    let arrayChecked = [];
                    await checked.filter((e, i) => {
                      if (e.includes(".")) {
                        arrayChecked.push({ value: e });
                      }
                    });
                    await console.log("arraynode", arrayChecked);
                    setArrayRoles(arrayChecked);
                    setChecked(checked);
                  }}
                  onExpand={(expanded, node) => {
                    setExpanded(expanded);
                  }}
                  onClick={(click) => {
                    console.log("click", click.path);
                  }}
                  checkModel="all"
                  iconsClass="fa5"
                  icons={{
                    check: <span className="rct-icon rct-icon-check" />,
                    uncheck: <span className="rct-icon rct-icon-uncheck" />,
                    halfCheck: (
                      <span className="rct-icon rct-icon-half-check" />
                    ),
                    expandClose: (
                      <span className="rct-icon rct-icon-expand-close" />
                    ),
                    expandOpen: (
                      <span className="rct-icon rct-icon-expand-open" />
                    ),
                    expandAll: (
                      <span className="rct-icon rct-icon-expand-all" />
                    ),
                    collapseAll: (
                      <span className="rct-icon rct-icon-collapse-close" />
                    ),
                    parentClose: <span className="" />,
                    parentOpen: <span className="" />,
                    leaf: <span className="" />,
                  }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
