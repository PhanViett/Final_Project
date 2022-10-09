import React, { useState } from "react";
import { Outlet } from "react-router-dom";
import Aside from "../layout/Aside";
import Nav from "../layout/Nav";


export function LayoutAdmin() {
  const [collapsed, setCollapsed] = useState(false);
  const [toggled, setToggled] = useState(false);

  const handleCollapsedChange = () => {
    setCollapsed(!collapsed);
  };

  const handleToggleSidebar = (value) => {
    setToggled(value);
  };

  // const isAuthorized = useSelector(
  //   (state) => state.auth.isAuthorized,
  //   shallowEqual
  // );

  // if (!isAuthorized) {
  //   return <Navigate to="/" />;
  // }

  return (
    <>
      <div id="main-content" className="position-relative">
        <Aside
          collapsed={collapsed}
          toggled={toggled}
          handleToggleSidebar={handleToggleSidebar}
        />
        <main>
          <header>
            <Nav
              collapsed={collapsed}
              handleCollapsedChange={handleCollapsedChange}
            />
          </header>
          <div className="container-fluid">
            {/* <Breadcrumbs /> */}
            <Outlet />
          </div>
        </main>
      </div>
    </>
  );
}
