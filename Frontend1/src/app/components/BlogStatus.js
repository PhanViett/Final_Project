import { useEffect, useState } from "react"
import { statusOpstions } from "../data"

export function BlogStatus(props) {
    const [text, setText] = useState("")
    const [finder, setFinder] = useState()

    useEffect(() => {
        setFinder(statusOpstions.find((e) => e.value == props?.status))
        if (finder) {
            setText(finder?.label)
        }
    }, [props])


    return (<>
        {finder?.value == 0 ?
            <span className="text-secondary">{text}</span>
            : finder?.value == 1 ?
            <span className="text-primary">{text}</span>
            : finder?.value == 2 ?
            <span className="text-success">{text}</span>
            : finder?.value == 3 ?
            <span className="text-danger">{text}</span>
            : null
        }
    </>

    )
}