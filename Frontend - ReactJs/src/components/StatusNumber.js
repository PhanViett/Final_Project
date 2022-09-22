import React from "react";

export default function StatusNumber(props) {
  const cusTrangThai = {
    fontWeight: 500,
    borderRadius: "6px",
    display: "inline-block",
    padding: "5px 10px 9px 10px",
    width: 140,
    justifyContent: "center",
    textAlign: "center",
  };

  const checkStatus = () => {
    switch (props?.status) {
      case 0:
      case 1:
        return (
          <span className="text-white bg-primary" style={cusTrangThai}>
            {props?.title}
          </span>
        );
      case 2:
        return (
          <span className="text-white bg-warning" style={cusTrangThai}>
            {props?.title}
          </span>
        );

      case 3:
        return (
          <span className="text-white bg-success" style={cusTrangThai}>
            {props?.title}
          </span>
        );
      case 4:
        return (
          <span className="text-white bg-danger" style={cusTrangThai}>
            {props?.title}
          </span>
        );
      default:
        break;
    }
  };
  return <div>{checkStatus()}</div>;
}
