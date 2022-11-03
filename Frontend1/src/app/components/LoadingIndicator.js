import React from "react";
import { Oval } from "react-loader-spinner";

export default function LoadingIndicator() {
  return (
    <div className="w-100 h-100" style={{ textAlign: "center" }}>
      <div className="spinner-border" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
    </div>
  );
}
