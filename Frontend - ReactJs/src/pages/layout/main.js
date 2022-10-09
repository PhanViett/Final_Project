import React, { useState } from "react";
import { FaUserCircle } from "react-icons/fa";
import { MdLogout } from "react-icons/md";
import { NavLink, Outlet } from "react-router-dom";
import Nav from "./Nav";

export function LayoutMain() {
	const [collapsed, setCollapsed] = useState(true);

	const handleCollapsedChange = () => {
		setCollapsed(!collapsed);
	};

	return (
		<>
			<div id="main-content" className="position-relative">
				<main>
					<header>

						<nav
							id="nav-admin"
							className="navbar navbar-expand-lg navbar-light p-0"
						>
							<div className="container-fluid position-relative">
								<img alt="" src="/media/Trans_Logo.png" width={45} className="d-inline-block align-text-center" />

								<div className="btn-group">
									<button
										type="button"
										className="btn btn-primary dropdown-toggle"
										data-toggle="dropdown"
										aria-haspopup="true"
										aria-expanded="false"
									>
										<span className="text-white ">
											<FaUserCircle size={30} color="white" /> ND Admin
										</span>
									</button>
									<div className="dropdown-menu dropdown-menu-right">
										<NavLink style={{ textDecoration: "none" }} to="thong-tin-tai-khoan">
											<button className="dropdown-item"
												type="button"
											>
												<FaUserCircle /> Thông tin tài khoản
											</button>
										</NavLink>
										<button className="dropdown-item"
											onClick={() => {
											}}
											type="button"
										>
											<MdLogout /> Đăng xuất
										</button>
									</div>
								</div>
							</div>
						</nav>


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
	)
}