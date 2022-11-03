import ReactDOM from "react-dom";
// Axios
import axios from "axios";
import { Chart, registerables } from "chart.js";

// Apps
import { PersistGate } from "redux-persist/integration/react";
import { MetronicI18nProvider } from "./_metronic/i18n/Metronici18n";
import { Provider } from "react-redux";
import store, { persistor } from "./app/redux-module/store";
import { AppRoutes } from "./app/routing/AppRoutes";
import "./_metronic/assets/sass/style.react.scss";
import "./_metronic/assets/sass/style.scss";
import SetupAxios from "./app/configs/SetupAxios";

SetupAxios(axios, store);

Chart.register(...registerables);

ReactDOM.render(
  <MetronicI18nProvider>
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <AppRoutes />
      </PersistGate>
    </Provider>
  </MetronicI18nProvider>,
  document.getElementById("root")
);
