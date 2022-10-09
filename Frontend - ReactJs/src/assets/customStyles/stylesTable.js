import axios from "axios";
import { toast } from "react-toastify";

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
  rows: {
    highlightOnHoverStyle: {
      backgroundColor: "rgb(230, 244, 244)",
      borderBottomColor: "#FFFFFF",
      outline: "1px solid #FFFFFF",
    },
  },
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

const conditionalRowStyles = [
  {
    when: (row) => row.toggleSelected,
    style: {
      backgroundColor: "#f5f5f5",
      userSelect: "none",
    },
  },
];

const handlePerRowsChange = async (api, body, newPerPage, page) => {
  axios
    .post({api} + `?page=${page}&per_page=${newPerPage}`, {})
    .then(({ data }) => {
      return data?.results;
    })
    .catch((err) => {
      toast.error("Có lỗi xảy ra vui lòng thử lại", {
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
};

export { customStyles, paginationOptions, conditionalRowStyles, handlePerRowsChange };
