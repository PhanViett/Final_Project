/* eslint-disable jsx-a11y/anchor-is-valid */
import { Outlet, Route, Routes } from "react-router-dom";
import Accessdenied from "./Accessdenied";
import { Error404 } from "./components/Error404";
import PageNotFound from "./PageNotFound";

const ErrorsLayout = () => {
  return (
    <div className="d-flex flex-column flex-root">
      <div className="d-flex flex-column flex-column-fluid bgi-position-y-bottom position-x-center bgi-no-repeat bgi-size-contain bgi-attachment-fixed">
        <div className="d-flex flex-column flex-column-fluid text-center p-10 py-lg-20">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

const ErrorsPage = () => (
  <Routes>
    <Route element={<ErrorsLayout />}>
      <Route path="404" element={<PageNotFound />} />
      <Route path="403" element={<Accessdenied />} />
      <Route index element={<Error404 />} />
    </Route>
  </Routes>
);

export { ErrorsPage };

