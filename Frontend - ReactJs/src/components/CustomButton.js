import React, { useEffect } from "react";
import { useSelector } from "react-redux";

const Button = ({
    className,
    children,
    style,
    onClick,
    firstPath,
    secondPath
}) => {
    const permissions = useSelector(
        (state) => state.auth?.permissions);

    useEffect(() => {
    }, []);

    if (permissions?.[firstPath]?.[secondPath]) {
        return (
            <button
                onClick={onClick}
                className={className}
                style={style}
            >
                {children}
            </button>
        );
    }
}

export default Button;

