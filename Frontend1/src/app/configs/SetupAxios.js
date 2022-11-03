export default function SetupAxios(axios, store) {
  axios.defaults.headers.Accept = "application/json";
  axios.interceptors.request.use(
    (config) => {
      const {
        auth: { access_token },
      } = store.getState();
      if (access_token) {
        config.headers.Authorization = `Bearer ${access_token}`;
      }
      return config;
    },
    (err) => Promise.reject(err)
  );
  axios.interceptors.response.use(
    (response) => response,
    (error) => {
      // if (error.response.status == 401) {
      //   localStorage.clear();
      //   window.location.href = "/connexion";
      // }
      // reject with error if response status is not 403
      return Promise.reject(error);
    }
  );
}

const responseHandler = (response) => {
  return response;
};

// const errorHandler = (error) => {
//   console.log("error", error.response);
//   let { status } = error.response;
//   switch (status) {
//     case 400:
//       const temp = errorCode?.find(
//         (elem) => elem.key === error.response.data.errorCode
//       );
//       if (temp) {
//         toast.error(temp.value, {
//           position: "top-right",
//           autoClose: 3000,
//           hideProgressBar: false,
//           closeOnClick: true,
//           pauseOnHover: true,
//           draggable: true,
//           progress: undefined,
//           toastId: "error",
//         });
//       }
//       return Promise.reject(error);
//     case 401:
//       localStorage.removeItem("persist:root");
//       authHelper.removeAuth();
//       toast.error("Token hết hạn!", {
//         position: "top-right",
//         autoClose: 3000,
//         hideProgressBar: false,
//         closeOnClick: true,
//         pauseOnHover: true,
//         draggable: true,
//         progress: undefined,
//         toastId: "error",
//       });
//       window.location.reload();
//       // navigate(0);
//       return Promise.reject(error);
//     case 500:
//       localStorage.removeItem("persist:root");
//       authHelper.removeAuth();
//       toast.error("Token hết hạn!", {
//         position: "top-right",
//         autoClose: 3000,
//         hideProgressBar: false,
//         closeOnClick: true,
//         pauseOnHover: true,
//         draggable: true,
//         progress: undefined,
//         toastId: "error",
//       });
//       window.location.reload();
//       // navigate(0);
//       return Promise.reject(error);
//     default:
//       return Promise.reject(error);
//   }
// };
