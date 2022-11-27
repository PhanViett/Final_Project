import { useEffect, useState } from "react";
import { ynOptions } from "../data";

export default function YesNo(props) {
    const [text, setText] = useState("");

    useEffect(() => {
        if (props) {
            const find = ynOptions.find((e) => e.value == props?.value)
            setText(find ? find.label : "")
        }
    }, [props])

    return (<span>{text}</span>);
}
