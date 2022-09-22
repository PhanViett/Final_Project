import * as PropTypes from "prop-types";
import React from "react";
import { toast } from "react-toastify";
import { checkNoti } from "../../utils/helpers";


function Button(props) {
    const { onClick, className, permissions, path, children, style, ...attributes } = props;
    let permissionKey = path.split(".");
    console.log('propspropsprops', props)

    const checkButton = () => {
        if (permissionKey[1] && permissions?.[permissionKey[0]]?.[permissionKey[1]]) {
            onClick()
        } else {
            checkNoti()
        }
    }
    return (
        <button
            style={style}
            onClick={() => checkButton()}
            className={className}
            {...attributes}
        >
            {
                children
            }
        </button>
    )
}

Button.propTypes = {
    className: PropTypes.string,
    onClick: PropTypes.func,
    permissions: PropTypes.object,
    path: PropTypes.string,
    status: PropTypes.bool,
    style: PropTypes.object,
};

Button.defaultProps = {
    className: "",
};

export default Button;
