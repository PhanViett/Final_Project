import * as PropTypes from "prop-types";
import React from "react";
import { checkNoti } from "../../utils/helpers";


function ButtonPermission(props) {
    const { onClick, className, permissions, path, children, style, ...attributes } = props;
    let permissionKey = path?.split(".");

    const checkButton = (e) => {
        if (!permissions || !path) {
            onClick(e)
        }
        else if (permissions && permissions?.[permissionKey[0]]?.[permissionKey[1]]) {
            onClick(e)
        } else {
            checkNoti()
        }
    }
    return (
        <button
            style={style}
            onClick={(e) => checkButton(e)}
            className={className}
            {...attributes}
        >
            {
                children
            }
        </button>
    )
}

ButtonPermission.propTypes = {
    className: PropTypes.string,
    onClick: PropTypes.func,
    permissions: PropTypes.object,
    path: PropTypes.string,
    status: PropTypes.bool,
    style: PropTypes.object,
};

ButtonPermission.defaultProps = {
    className: "",
};

export default ButtonPermission;
