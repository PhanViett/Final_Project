import React, { useState } from "react";
import ContentLoader from "react-content-loader";

export default function Loader(props) {
  const [type, setType] = useState(props.type);

  switch (type) {
    case "new-loader": {
      return (
        <ContentLoader
          speed={2}
          width={450}
          height={400}
          viewBox="0 0 450 400"
          backgroundColor="#f3f3f3"
          foregroundColor="#ecebeb"
          {...props}
        >
          <rect x="0" y="10" rx="5" ry="5" width="170" height="100" />
          <rect x="190" y="10" rx="6" ry="6" width="250" height="9" />
          <rect x="190" y="30" rx="6" ry="6" width="200" height="9" />

          <rect x="0" y="130" rx="5" ry="5" width="170" height="100" />
          <rect x="190" y="130" rx="6" ry="6" width="250" height="9" />
          <rect x="190" y="150" rx="6" ry="6" width="200" height="9" />

          <rect x="0" y="250" rx="5" ry="5" width="170" height="100" />
          <rect x="190" y="250" rx="6" ry="6" width="250" height="9" />
          <rect x="190" y="270" rx="6" ry="6" width="200" height="9" />
        </ContentLoader>
      );
    }

    default:
      return (
        <ContentLoader
          speed={2}
          width={400}
          height={160}
          viewBox="0 0 400 160"
          backgroundColor="#f3f3f3"
          foregroundColor="#ecebeb"
          {...props}
        >
          {/* <rect x="48" y="8" rx="3" ry="3" width="88" height="6" />
          <rect x="48" y="26" rx="3" ry="3" width="52" height="6" />
          <rect x="0" y="56" rx="3" ry="3" width="410" height="6" />
          <rect x="0" y="72" rx="3" ry="3" width="380" height="6" />
          <rect x="0" y="88" rx="3" ry="3" width="178" height="6" />
          <circle cx="20" cy="20" r="20" /> */}
        </ContentLoader>
      );
  }
}
