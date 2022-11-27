export default function Status(props) {

  return (
    <>
      {props.status === 0 ? (
        <span className="badge badge-light-success fs-7 fw-bold justify-content-center py-2" style={{width: 140}}>
          Bình thường
        </span>
      ) : (
          <span className="badge badge-light-dark fs-7 fw-bold justify-content-center py-2" style={{ width: 140 }}>
          Không bình thường
        </span>
      )}
    </>
  );
}
