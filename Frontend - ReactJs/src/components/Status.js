import React from "react";

export default function Status(props) {
  const cusTrangThai = {
    fontWeight: 500,
    borderRadius: "6px",
    display: "inline-block",
    padding: "5px 10px 9px 10px",
  };

  return (
    <div>
      {props?.status === true ? (
        <span className="text-white bg-success" style={cusTrangThai}>
          Đang hoạt động
        </span>
      ) : (
        <span className="text-white bg-danger" style={cusTrangThai}>
          Không hoạt động
        </span>
      )}
    </div>
  );
}
