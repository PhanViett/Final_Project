import * as PropTypes from "prop-types";
import React from "react";
import {
    AiFillLock, AiFillUnlock
} from "react-icons/ai";
import { checkNoti } from "../../utils/helpers";
function Link(props) {
    const { onClick, className, permissions, path, status, iconRight, lable, block, href } = props;
    let permissionKey = path.split(".");
    const checkButton = () => {
        if (permissionKey[1] && permissions?.[permissionKey[0]]?.[permissionKey[1]]) {
            onClick()
        } else {
            checkNoti()
        }
    }
    return (
        <a
            href={permissionKey[1] && permissions?.[permissionKey[0]]?.[permissionKey[1]] && href ? href : null}
            onClick={() => checkButton()}
            className={className}
        >
            {block && (<> {status ? <AiFillLock /> : <AiFillUnlock />} {' '}
                {status ? "Khóa" : "Mở khoá"}</>)}
            {iconRight}{' '}{lable}

        </a>


    );
}
Link.propTypes = {
    className: PropTypes.string,
    onClick: PropTypes.func,
    permissions: PropTypes.object,
    path: PropTypes.string,
    status: PropTypes.bool,
    // iconRight: PropTypes.element,
    lable: PropTypes.string,
    block: PropTypes.bool

};

Link.defaultProps = {
    className: "dropdown-item pb-2",
    block: false
};

export default Link;
