import { useEffect, useState } from "react";
import { levelOptions } from "../data";

export default function Level(props) {
    const [text, setText] = useState("");

    useEffect(() => {
        if (props) {
            const find = levelOptions.find((e) => e.value == props?.value)
            setText(find ? find.label : "")
        }
    }, [props])

    return (<span>{text}</span>);
}
