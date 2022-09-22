import React from "react";
import { Modal } from "react-bootstrap";

const PATH_IMAGE = process.env.REACT_APP_CDN_URL;

export function PopupImage(props) {
  return (
    <Modal
      size="xl"
      show={props?.show}
      onHide={() => props?.closePopupImage()}
      centered
      fullscreen={true}
    >
      <Modal.Header className="bg-blue2">
        <Modal.Title className="text-white">Hình ảnh</Modal.Title>
        <button
          className="btn text-white"
          onClick={() => props?.closePopupImage()}
        >
          <i className="fas fa-times"></i>
        </button>
      </Modal.Header>
      <Modal.Body>
        <img
          alt=""
          className="w-100"
          src={
            props?.type === "slider"
              ? props?.imageChoose?.image
              : PATH_IMAGE +
                (props?.type === "logo"
                  ? props?.imageChoose?.logo_src
                  : props?.imageChoose?.picture)
          }
        />
      </Modal.Body>
    </Modal>
  );
}
