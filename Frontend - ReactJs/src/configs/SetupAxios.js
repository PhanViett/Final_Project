import { toast } from "react-toastify";
import errorCode from "./errorCode";
export default function SetupAxios(axios, store) {
  axios.defaults.headers.Accept = "application/json";
  axios.interceptors.request.use(
    (config) => {
      const {
        auth: { access_token },
      } = store.getState();
      // console.log("Auth", access_token);
      if (access_token) {
        config.headers.Authorization = `Bearer ${access_token}`;
      }
      return config;
    },
    (err) => Promise.reject(err)
  );

  axios.interceptors.response.use(
    (response) => responseHandler(response),
    (error) => errorHandler(error)
  );
}

const responseHandler = (response) => {
  return response;
};

const errorHandler = (error) => {
  console.log("errorHandler", error.response);
  if (error.response.status === 401) {
    localStorage.removeItem("persist:root");
    // window.location = "/admin/login";
  } else if (error.response.status === 400) {
    if (error.response.data) {
      const temp = errorCode?.find(
        (elem) => elem.key === error.response.data.errorCode
      );
      if (temp) {
        toast.error(temp.value, {
          position: "top-right",
          autoClose: 3000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          toastId: "error",
        });
      }
      return Promise.reject(error);
    }
  }
  return Promise.reject(error);
};
