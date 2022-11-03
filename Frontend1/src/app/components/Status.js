import React from "react";

export default function Status(props) {
  return (
    <div>
      {props.status ? (
        <span className="badge badge-light-success fs-7 fw-bold">
          Đang hoạt động
        </span>
      ) : (
        <span className="badge badge-light-dark fs-7 fw-bold">
          Không hoạt động
        </span>
      )}
    </div>
  );
}
