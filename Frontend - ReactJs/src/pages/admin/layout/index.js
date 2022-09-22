import React, { useState } from "react";
import Nav from "../partials/Nav";
import { Outlet, Navigate } from "react-router-dom";
import { shallowEqual, useSelector } from "react-redux";
import Aside from "../partials/Aside";

import { Breadcrumbs } from "../partials/Breadcrumbs";

export function LayoutAdmin() {
  const [collapsed, setCollapsed] = useState(false);
  const [toggled, setToggled] = useState(false);

  const handleCollapsedChange = () => {
    setCollapsed(!collapsed);
  };

  // const handleImageChange = (checked) => {
  //   setImage(checked);
  // };

  const handleToggleSidebar = (value) => {
    setToggled(value);
  };

  const isAuthorized = useSelector(
    (state) => state.auth.isAuthorized,
    shallowEqual
  );
  // const loading = useSelector((state) => state.common.loading, shallowEqual);
  if (!isAuthorized) {
    return <Navigate to="/" />;
  }

  return (
    <>
      <div id="main-content" className="position-relative">
        <Aside
          collapsed={collapsed}
          toggled={toggled}
          handleToggleSidebar={handleToggleSidebar}
        />
        <main>
          {/* <div className="btn-toggle" onClick={() => handleToggleSidebar(true)}>
            <FaBars />
          </div> */}

          <header>
            <Nav
              collapsed={collapsed}
              handleCollapsedChange={handleCollapsedChange}
            />
          </header>
          <div className="container-fluid">
            <Breadcrumbs />
            <Outlet />
          </div>
          {/* <footer>
            <small>
              © {new Date().getFullYear()} made with <FaHeart style={{ color: 'red' }} /> by -{' '}
              <a target="_blank" rel="noopener noreferrer" href="https://azouaoui.netlify.com">
                Mohamed Azouaoui
              </a>
            </small>
            <br />
            <div className="social-bagdes">
              <a href="https://github.com/azouaoui-med" target="_blank" rel="noopener noreferrer">
                <img
                  alt="GitHub followers"
                  src="https://img.shields.io/github/followers/azouaoui-med?label=github&style=social"
                />
              </a>
              <a href="https://twitter.com/azouaoui_med" target="_blank" rel="noopener noreferrer">
                <img
                  alt="Twitter Follow"
                  src="https://img.shields.io/twitter/follow/azouaoui_med?label=twitter&style=social"
                />
              </a>
            </div>
          </footer> */}
        </main>
      </div>
    </>
  );
}
