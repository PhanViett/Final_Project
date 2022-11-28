export default function Status(props) {

  return (
    <>
      {props.status === 1 ? (
        <span className="badge badge-light-success fs-7 fw-bold justify-content-center py-2" style={{width: 150}}>
          Bình thường
        </span>
      ) : (
          <span className="badge badge-light-dark fs-7 fw-bold justify-content-center py-2" style={{ width: 150 }}>
          Không bình thường
        </span>
      )}
    </>
  );
}
