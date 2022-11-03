import axios from "axios";
import ReactDOM from "react-dom";
// import { Chart, registerables } from "chart.js";

import SetupAxios from "./configs/SetupAxios";
import store, { persistor } from "./redux-module/store";
import { MetronicI18nProvider } from "./_metronic/i18n/Metronici18n";
import { Provider } from "react-redux";
import { PersistGate } from "redux-persist/integration/react";
import { RootRouteObject } from "./routing/RootRouteObject";

SetupAxios(axios, store);

// Chart.register(...registerables);

ReactDOM.render(
  <MetronicI18nProvider>
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <RootRouteObject />
      </PersistGate>
    </Provider>
  </MetronicI18nProvider>,
  document.getElementById("root")
);
