import React, { useState } from "react";
import { shallowEqual, useSelector } from "react-redux";
import { Outlet } from "react-router-dom";
import Aside from "./Aside";
import Nav from "./Nav";



export function LayoutAdmin() {
  const [collapsed, setCollapsed] = useState(true);
  const [toggled, setToggled] = useState(false);

  const handleCollapsedChange = () => {
    setCollapsed(!collapsed);
  };

  const handleToggleSidebar = (value) => {
    setToggled(value);
  };

  const isAuthorized = useSelector(
    (state) => state.auth.isAuthorized,
    shallowEqual
  );

  // if (!isAuthorized) {
  //   return <Navigate to="/" />;
  // }

  return (
    <>
      <div id="main-content" className="position-relative">
        {/* <Aside
          collapsed={collapsed}
          toggled={toggled}
          handleToggleSidebar={handleToggleSidebar}
        /> */}

        <main>
          <header>
            <Nav
              collapsed={collapsed}
              handleCollapsedChange={handleCollapsedChange}
            />
          </header>
          <div className="container-fluid px-0">
            {/* <Breadcrumbs /> */}
            <div className="px-5 pt-4">
                <Outlet />
            </div>
          </div>
        </main>
      </div>
    </>
  );
}
