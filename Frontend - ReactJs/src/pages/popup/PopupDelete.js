import React from "react";
import { Modal, Button } from "react-bootstrap";
import api from "../../configs/api";

export function PopupDelete(props) {
  return (
    <Modal
      centered
      show={props?.show}
      onHide={() => {
        props?.onHide();
      }}
    >
      <Modal.Header className="bg-blue2">
        <Modal.Title className="text-white" style={{ fontSize: "22px" }}>
          {props?.title}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body className="d-flex" style={{ justifyContent: "center" }}>
        <img
          width={350}
          height={175}
          className="mb-2"
          src={api.CDN_IMAGES + "congsuckhoe/uploads/gif/deleteTrash.gif"}
          alt=""
        />
      </Modal.Body>
      <Modal.Footer>
        <div className="d-flex justify-content-center">
          <Button
            className="btn btn-secondary mr-3"
            onClick={() => {
              props?.onHide();
            }}
          >
            Quay lại
          </Button>
          <Button
            className="btn btn-primary"
            onClick={() => {
              props?.onDetele();
              props?.onHide();
            }}
          >
            Đồng ý
          </Button>
        </div>
      </Modal.Footer>
    </Modal>
  );
}
