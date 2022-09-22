import * as Sentry from "@sentry/react";
import { BrowserTracing } from "@sentry/tracing";
import axios from "axios";
import React from "react";
import ReactDOM from "react-dom";
import { Helmet, HelmetProvider } from "react-helmet-async";
import { Provider } from "react-redux";
import { BrowserRouter } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import { PersistGate } from "redux-persist/integration/react";

import SetupAxios from "./configs/SetupAxios";
import configureStore from "./configureStore";
import FullPageLoader from "./pages/admin/partials/FullPageLoader";
import Notifications from "./pages/admin/partials/Notifications";
import reportWebVitals from "./reportWebVitals";
import { RootRouteObject } from "./routing/RootRouteObject";

import "@fortawesome/fontawesome-free/css/all.min.css";
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.js";
import "react-block-ui/style.css";
import "react-sortable-tree/style.css";
import "react-toastify/dist/ReactToastify.css";

// This only needs to be done once; probably during your application's bootstrapping process.
import "./assets/sass/styles.scss";

import "react-checkbox-tree/lib/react-checkbox-tree.css";

const { store, persistor } = configureStore();

//Treacking
if (!process.env.NODE_ENV || process.env.NODE_ENV === "production") {
  Sentry.init({
    dsn: "https://eaf2d13e5cc54d0cb4d85fb4b3a1a629@o1115413.ingest.sentry.io/6242563",
    integrations: [new BrowserTracing()],

    // Set tracesSampleRate to 1.0 to capture 100%
    // of transactions for performance monitoring.
    // We recommend adjusting this value in production
    tracesSampleRate: 1.0,
  });
} else {
  // production code
}

const App = () => {
  return (
    <BrowserRouter>
      <Notifications />
      <RootRouteObject />
      <FullPageLoader />
      <ToastContainer
        hideProgressBar
        pauseOnFocusLoss
        draggable
        pauseOnHover
        limit={1}
      />
    </BrowserRouter>
  );
};

/**
 * Creates `axios-mock-adapter` instance for provided `axios` instance, add
 * basic Metronic mocks and returns it.
 *
 * @see https://github.com/ctimmerm/axios-mock-adapter
 */

/**
 * Inject Metronic interceptors for axios.
 *
 * @see https://github.com/axios/axios#interceptors
 */
SetupAxios(axios, store);

ReactDOM.hydrate(
  // <I18nProvider>
  <Provider store={store}>
    <PersistGate persistor={persistor}>
      <HelmetProvider>
        <Helmet />
        <App />
      </HelmetProvider>
    </PersistGate>
  </Provider>,
  // </I18nProvider>,
  document.getElementById("root")
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
