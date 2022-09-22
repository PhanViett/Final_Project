import DataTable from "react-data-table-component";
import React, { useEffect, useState } from "react";
import { toast } from "react-toastify";
import BlockUi from "react-block-ui";
import { Oval, TailSpin } from "react-loader-spinner";
import axios from "axios";
import api from "../../../configs/api";
import "../../../assets/admin/sass/newsCore.scss";
import { useDispatch } from "react-redux";
import { setTitle } from "../../../saga-modules/common/actions";
import { PopupDelete } from "../../popup/PopupDelete";
import CheckboxTree from "react-checkbox-tree";
import { debounce } from "lodash";
import moment from "moment";

export function ListRoles() {
  const dispatch = useDispatch();

  const [page, setPage] = useState(1);
  const [perPage, setPerPage] = useState(10);
  const [isLoading, setIsLoading] = useState(true);
  const [pending, setPending] = useState(true);
  const [totalRows, setTotalRows] = useState(0);
  const [inputSearch, setInputSearch] = useState("");
  const [checked, setChecked] = useState([]);
  const [nodes, setNodes] = useState([]);
  const [expanded, setExpanded] = useState([]);
  const [ArrayRoles, setArrayRoles] = useState([]);
  const [ListRoles, setListRoles] = useState([]);
  const [SelectedRoles, setSelectedRoles] = useState("");
  const [sortType, setSortType] = useState("desc");
  const [sortID, setSortID] = useState("created_date");
  //open modal delete
  const [isvisibleDelete, setIsvisibleDelete] = useState(false);
  const [idDelete, setIdDelete] = useState("");
  const closeModalDelete = () => setIsvisibleDelete(false);
  const showModalDelete = () => setIsvisibleDelete(true);

  useEffect(() => {
    dispatch(setTitle({ title: "Danh sách vai trò" }));
    getDefaultPermissions();
    getRoles({});
  }, []);

  const getDefaultPermissions = () => {
    axios
      .get(api.ROLES + "/default-permission")
      .then(async ({ data }) => {
        setNodes(data?.content);
      })
      .catch((error) => { })
      .finally(() => {
        setPending(false);
        setIsLoading(false);
      });
  };

  const debounceSearch = React.useCallback(
    debounce(
      (nextValue, sort_ID, sort_type) =>
        getRoles({ search_ten: nextValue, sort_ID, sort_type }),
      1000
    ),
    []
  );

  const addRole = async () => {
    await setIsLoading(true);
    const { ten } = form;
    let jsonPostRoles = {
      ten: ten || "",
      vai_tro: JSON.stringify(ArrayRoles),
    };
    axios
      .post(api.ROLES, jsonPostRoles)
      .then(async ({ data }) => {
        await toast.success(data?.msg, {
          position: "top-right",
          autoClose: 2000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          toastId: "success",
        });
        resetState();
        getRoles({});
      })
      .catch((error) => {
        toast.error(error?.response?.data?.msg, {
          position: "top-right",
          autoClose: 2000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          toastId: "error",
        });
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  const changeArray = (array) => {
    console.log("log array", array);
    let arrayRoles = [];
    for (let i = 0; i < array.length; i++) {
      if (array[i].children && array[i].children.length) {
        for (let j = 0; j < array[i].children.length; ++j) {
          if (array[i].children[j].checked) {
            arrayRoles.push(array[i].children[j].value);
          }
        }
      }
    }
    return arrayRoles;
  };

  const changeArrayParent = (array) => {
    console.log("log array", array);
    let arrayRoles = [];
    for (let i = 0; i < array.length; i++) {
      arrayRoles.push(array[i].value);
    }
    return arrayRoles;
  };

  const getRoles = ({
    page_number = page,
    search_ten = inputSearch || "",
    size = perPage,
    sort_ID = sortID,
    sort_type = sortType,
  }) => {
    setIsLoading(true);
    setPending(true);
    axios
      .post(api.ROLES + "/get-list" + `?page=${page_number}&per_page=${size}`, {
        search_ten: search_ten || "",
        [sort_ID]: sort_type,
      })
      .then(async ({ data }) => {
        setListRoles(data?.results);
        setTotalRows(data?.total);
      })
      .catch((error) => {
        toast.error(error?.response?.data?.msg, {
          position: "top-right",
          autoClose: 2000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          toastId: "error",
        });
      })
      .finally(() => {
        setPending(false);
        setIsLoading(false);
      });
  };

  const getDetailRoles = (id) => {
    setIsLoading(true);
    axios
      .get(api.ROLES + "/" + id)
      .then(async ({ data }) => {
        let { results } = data;
        console.log("data detail", data);
        setSelectedRoles(results);
        setField("ten", results?.ten);
        setChecked(changeArray(JSON.parse(results?.vai_tro)));
        changeArrayRoles(changeArray(JSON.parse(results?.vai_tro)));
        setExpanded(changeArrayParent(JSON.parse(results?.vai_tro)));
      })
      .catch((error) => {
        toast.error(error?.response?.data?.msg, {
          position: "top-right",
          autoClose: 2000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          toastId: "error",
        });
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  const updateRoles = async () => {
    await setIsLoading(true);
    const { ten } = form;
    let jsonPutRoles = {
      ten: ten || "",
      vai_tro: JSON.stringify(ArrayRoles),
    };
    axios
      .put(api.ROLES + "/" + SelectedRoles?.id, jsonPutRoles)
      .then(async ({ data }) => {
        await toast.success(data?.msg, {
          position: "top-right",
          autoClose: 2000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          toastId: "success",
        });
        resetState();
        getRoles({});
      })
      .catch((error) => {
        toast.error(error?.response?.data?.msg, {
          position: "top-right",
          autoClose: 2000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          toastId: "error",
        });
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  const handleRowClicked = (row) => {
    const updatedData = ListRoles?.map((item) => {
      if (row.id === item.id) {
        return {
          ...item,
          toggleSelected: true,
        };
      }
      return {
        ...item,
        toggleSelected: false,
      };
    });
    setListRoles(updatedData);
  };
  const conditionalRowStyles = [
    {
      when: (row) => row.toggleSelected,
      style: {
        backgroundColor: "#f5f5f5",
        userSelect: "none",
      },
    },
  ];

  //validate thêm danh mục
  const [form, setForm] = useState({});
  const [errors, setErrors] = useState({});
  const setField = (field, value) => {
    setForm({
      ...form,
      [field]: value,
    });
    if (!!errors[field])
      setErrors({
        ...errors,
        [field]: null,
      });
  };

  const findFormErrors = () => {
    const { ten } = form;
    const newErrors = {};
    // name errors
    if (!ten || ten === "") newErrors.ten = "Tên không được bỏ trống!";
    console.log("log newErrors", newErrors);
    return newErrors;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // get our new errors
    const newErrors = findFormErrors();
    // Conditional logic:
    if (Object.keys(newErrors).length > 0) {
      // We got errors!
      setErrors(newErrors);
    } else {
      // No errors! Put any logic here for the form submission!
      if (SelectedRoles) {
        updateRoles();
      } else {
        addRole();
      }
    }
  };

  // handle api
  const deleteRoles = async () => {
    await setPending(true);
    axios
      .delete(api.ROLES + "/" + idDelete)
      .then(async ({ data }) => {
        await toast.success(data?.msg, {
          position: "top-right",
          autoClose: 2000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          toastId: "success",
        });
        resetState();
        if (page == 1) {
          getRoles({ page_number: 1 });
        } else if (ListRoles?.length == 1) {
          getRoles({ page_number: page - 1 });
        } else {
          getRoles({ page_number: page });
        }
      })
      .catch((error) => {
        console.log("error", error);
        toast.error(error?.response?.data?.msg, {
          position: "top-right",
          autoClose: 2000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          toastId: "error",
        });
      })
      .finally(() => {
        setPending(false);
      });
  };

  const resetState = () => {
    setSelectedRoles("");
    setArrayRoles([]);
    setExpanded([]);
    window.scrollTo(0, 0);
    setChecked([]);
    setField("ten", "");
    setIdDelete("");
  };

  const columns = [
    {
      name: "Tên vai trò",
      selector: (row) => <span>{row.ten}</span>,
      sortable: true,
      grow: 2,
      style: {
        color: "#1251ff",
        fontSize: "14px",
        fontWeight: 500,
        cursor: "pointer",
      },
    },
    {
      name: "Người dùng",
      selector: (row) => <span>123</span>,
      grow: 2,
      style: {
        color: "#202124",
        fontSize: "14px",
        fontWeight: 500,
      },
    },
    {
      name: "Ngày cập nhật",
      selector: (row) => (
        <span>{moment(row?.created_at).format("DD/MM/YYYY")}</span>
      ),
      grow: 2,
      sortable: true,
      style: {
        color: "#202124",
        fontSize: "14px",
        fontWeight: 500,
      },
    },
    {
      name: "Thao tác",
      // grow: 2,
      cell: (row) => (
        <button
          style={{ boxShadow: "none" }}
          className="btn btn-link text-danger w-100 float-right"
          onClick={async () => {
            await setIdDelete(row?.id);
            showModalDelete();
          }}
        >
          <i className="far fa-trash-alt"></i>
        </button>
      ),
    },
  ];

  const handleSort = async (column, sortDirection) => {
    await setSortType(sortDirection);
    await getRolesBySortID(column?.id, sortDirection);
  };

  const getRolesBySortID = (value, sortDirection) => {
    switch (value) {
      case 1:
        setSortID("order_ten");
        getRoles({ sort_ID: "order_ten", sort_type: sortDirection });
        break;
      case 3:
        setSortID("created_date");
        getRoles({ sort_ID: "created_date", sort_type: sortDirection });
        break;
      default:
        break;
    }
  };

  const changeArrayRoles = (checked) => {
    let arrayChecked = [];
    checked.filter((e, i) => {
      if (e.includes(".")) {
        arrayChecked.push(e);
      }
    });
    setArrayRoles(arrayChecked);
  };

  const customStyles = {
    headRow: {
      style: {
        borderTopStyle: "solid",
        borderTopWidth: "1px",
        borderTopColor: "#e0e0e0",
        borderBottomColor: "#e0e0e0",
      },
    },
    headCells: {
      style: {
        color: "#202124",
        fontSize: "16px",
      },
    },
    rows: {},
    pagination: {
      style: {
        border: "none",
      },
    },
  };
  const paginationOptions = {
    rowsPerPageText: "Dòng hiển thị",
    rangeSeparatorText: "trên",
  };

  const cardBox = {
    backgroundColor: "#fff",
    backgroundClip: "border-box",
    border: "1px solid #e7eaed",
    padding: "1.5rem",
    marginBottom: "24px",
    borderRadius: "0.5rem",
  };

  const handlePerRowsChange = async (newPerPage, page) => {
    await setIsLoading(true);
    axios
      .get(api.ROLES + `?page=${page}&per_page=${newPerPage}`)
      .then(({ data }) => {
        if (data?.results) {
          setListRoles(data?.results);
          setPerPage(newPerPage);
        }
      })
      .catch(() => { })
      .finally(() => {
        setIsLoading(false);
      });
  };
  const handlePageChange = (page) => {
    setPage(page);
    getRoles({ page_number: page });
  };

  return (
    <div className="page">
      <div className="container-fluid">
        <BlockUi
          tag="div"
          blocking={isLoading}
          loader={
            <TailSpin
              arialLabel="loading-indicator"
              height={60}
              width={60}
              strokeWidth={2}
              strokeWidthSecondary={1}
              color="blue"
              secondaryColor="blue"
              wrapperClass={"d-inline-flex"}
            />
          }
        >
          <div className="row">
            <div className="col-md-6">
              <div className="" style={cardBox}>
                <div className="col-12">
                  <div className="row pb-3">
                    <div className="col-md-5 pb-1 col-12">
                      <div>
                        <input
                          value={inputSearch}
                          onChange={(data) => {
                            setPending(true);
                            setInputSearch(data.target?.value);
                            debounceSearch(
                              data?.target.value,
                              sortID,
                              sortType
                            );
                          }}
                          style={{ fontSize: 14, fontWeight: 500 }}
                          placeholder="Nhập tên vai trò"
                          className="form-control"
                        />
                      </div>
                    </div>

                    <div className="col-md-3 pb-1 col-12">
                      <button
                        className="btn float-sm-right bg-blue2 text-white"
                        onClick={() => {
                          getRoles({ page_number: page });
                          resetState();
                        }}
                        style={{ fontSize: ".9rem" }}
                      >
                        Tạo mới
                      </button>
                    </div>
                  </div>
                  <DataTable
                    onSort={handleSort}
                    sortServer
                    columns={columns}
                    data={ListRoles}
                    customStyles={customStyles}
                    pagination
                    progressPending={pending}
                    highlightOnHover
                    pointerOnHover
                    noDataComponent={"Không có dữ liệu."}
                    paginationComponentOptions={paginationOptions}
                    paginationServer
                    paginationTotalRows={totalRows}
                    onChangeRowsPerPage={handlePerRowsChange}
                    onChangePage={handlePageChange}
                    paginationRowsPerPageOptions={[10, 25, 50]}
                    conditionalRowStyles={conditionalRowStyles}
                    onRowClicked={(data) => {
                      getDetailRoles(data?.id);
                      handleRowClicked(data);
                    }}
                    progressComponent={
                      <div style={{ padding: "24px" }}>
                        <Oval
                          arialLabel="loading-indicator"
                          color="#007bff"
                          height={40}
                        />
                      </div>
                    }
                  />
                </div>
              </div>
            </div>

            <div className="col-md-6">
              <div className="" style={cardBox}>
                <div className="">
                  <p className="font-weight-bold">
                    {SelectedRoles
                      ? `Cập nhật vai trò (${SelectedRoles?.ten})`
                      : " Tạo mới vai trò"}
                  </p>
                </div>

                <div className="row mt-3">
                  <div className="col-4">
                    <p className="font-weight-bold">
                      Tên vai trò<span className="text-danger">*</span>
                    </p>
                  </div>
                  <div className="col-8">
                    <input
                      style={{ fontSize: 14, fontWeight: 500 }}
                      value={form?.ten === null ? "" : form?.ten}
                      placeholder="Nhập tên vai trò"
                      className={`form-control  ${errors?.ten ? "is-invalid" : ""
                        }  `}
                      onChange={(e) => {
                        setField("ten", e.target.value);
                      }}
                    ></input>
                    <div className="invalid-feedback d-block">{errors?.ten}</div>
                  </div>
                </div>

                <div className="row mt-3">
                  <div className="col-4">
                    <p className="font-weight-bold">Danh sách quyền</p>
                  </div>
                  <div className="col-8">
                    <CheckboxTree
                      expandOnClick={false}
                      nodes={nodes}
                      checked={checked}
                      expanded={expanded}
                      onCheck={async (checked, node) => {
                        console.log("checked", checked);
                        setChecked(checked);
                        changeArrayRoles(checked);
                      }}
                      onExpand={(expanded, node) => {
                        console.log("log expanded", expanded);
                        setExpanded(expanded);
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
                <div className="row mt-3">
                  <div className="col-4">
                    {SelectedRoles ? (
                      <button
                        className="btn text-white bg-blue2"
                        style={{ fontSize: ".9rem" }}
                        onClick={() => {
                          getRoles({ page_number: page });
                          resetState();
                        }}
                      >
                        <i className="fas fa-sync-alt"></i> Làm mới
                      </button>
                    ) : null}
                  </div>

                  <div className="col-8">
                    <button
                      className="btn text-white bg-blue2 mr-3"
                      style={{ fontSize: ".9rem" }}
                      onClick={(e) => {
                        handleSubmit(e);
                      }}
                    >
                      {SelectedRoles ? (
                        <i className="fa fa-pencil-alt"></i>
                      ) : (
                        <i className="fas fa-save "></i>
                      )}{" "}
                      {SelectedRoles ? "Cập nhật" : "Lưu vai trò"}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <PopupDelete
            title="Bạn có đồng ý xóa không ?"
            show={isvisibleDelete}
            onHide={closeModalDelete}
            onDetele={() => {
              deleteRoles();
            }}
          />
        </BlockUi>
      </div>
    </div>
  );
}
