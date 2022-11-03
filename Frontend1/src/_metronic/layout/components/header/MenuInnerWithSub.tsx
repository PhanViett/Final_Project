import React, { useRef, useEffect } from "react";
import { useLocation } from "react-router";
import clsx from "clsx";
import { checkIsActive, KTSVG } from "../../../helpers";

type Props = {
  to: string;
  title: string;
  icon?: string;
  amountNoti?: any;
  fontIcon?: string;
  menuTrigger?: "click" | `{default:'click', lg: 'hover'}`;
  menuPlacement?: "right-start" | "bottom-start";
  hasArrow?: boolean;
  hasBullet?: boolean;
  isMega?: boolean;
};

const MenuInnerWithSub: React.FC<Props> = ({
  children,
  to,
  title,
  icon,
  amountNoti,
  fontIcon,
  menuTrigger,
  menuPlacement,
  hasArrow = false,
  hasBullet = false,
  isMega = false,
}) => {
  const menuItemRef = useRef<HTMLDivElement>(null);
  const { pathname } = useLocation();

  useEffect(() => {
    if (menuItemRef.current && menuTrigger && menuPlacement) {
      menuItemRef.current.setAttribute("data-kt-menu-trigger", menuTrigger);
      menuItemRef.current.setAttribute("data-kt-menu-placement", menuPlacement);
    }
  }, [menuTrigger, menuPlacement]);

  return (
    <div
      ref={menuItemRef}
      className="menu-item menu-inner-sub menu-lg-down-accordion me-lg-1"
    >
      <span
        className={clsx("menu-link py-3", {
          active: checkIsActive(pathname, to),
        })}
      >
        {hasBullet && (
          <span className="menu-bullet">
            <span className="bullet bullet-dot"></span>
          </span>
        )}

        {amountNoti > 0 && (
          <span
            className="menu-bullet text-center"
            style={{
              position: "absolute",
              top: 5,
              right: 2,
              backgroundColor: "red",
              width: 23,
              height: 23,
              borderRadius: 23,
              color: "#ffffff",
            }}
          >
            {amountNoti}
          </span>
        )}

        {icon && (
          <span className="menu-icon">
            <KTSVG path={icon} className="svg-icon-2" />
          </span>
        )}

        {fontIcon && (
          <span className="menu-icon">
            <i className={fontIcon}></i>
          </span>
        )}

        <span className="menu-title">{title}</span>

        {hasArrow && <span className="menu-arrow"></span>}
      </span>
      <div
        className={clsx(
          "menu-sub menu-sub-lg-down-accordion menu-sub-lg-dropdown",
          isMega
            ? "w-100 w-lg-600px p-5 p-lg-5"
            : "menu-rounded-0 py-lg-4 w-lg-225px"
        )}
        data-kt-menu-dismiss="true"
      >
        {children}
      </div>
    </div>
  );
};

export { MenuInnerWithSub };
