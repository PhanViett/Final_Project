import React from "react";
import { NavLink } from "react-router-dom";
import useBreadcrumbs from "use-react-router-breadcrumbs";
import { useSelector } from "react-redux";
import { routers } from "../../../routing/RootRouteObject";
// import { titleSelector } from "../../../saga-modules/common/selectors";

function Breadcrumbs() {
  //   const titleBreadcrumbs = useSelector((state) => titleSelector(state));
  const common = useSelector((state) => state.common);
  const breadcrumbs = useBreadcrumbs(routers);
  breadcrumbs.shift();
  return (
    <div id="breadcrumbs" className="row">
      {/* {breadcrumbs.map(({ breadcrumb }) => breadcrumb)} */}
      <div className="col-12">
        <div className="page-title-box">
          <div className="page-title-right d-md-none d-lg-block">
            <ol className="breadcrumb m-0">
              {breadcrumbs.map(({ match, breadcrumb }) => {
                // console.log(match, breadcrumb);
                return (
                  <li className="breadcrumb-item" key={match.pathname}>
                    <span>
                      <NavLink to={match.pathname}>{breadcrumb}</NavLink>{" "}
                    </span>
                  </li>
                );
              })}
            </ol>
          </div>
          <h4 className="page-title">{common?.title}</h4>
        </div>
      </div>
    </div>
  );
}

export { Breadcrumbs };
