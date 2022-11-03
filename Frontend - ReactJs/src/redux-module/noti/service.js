import axios from "axios";
import api from "../../configs/api";

export const getListNoti = (id) => {
  return new Promise((resolve, reject) => {
    axios
      .get(api.API_GET_THONG_BAO + `?page=1&per_page=1000`)
      .then(({ data }) => {
        resolve(data);
      })
      .catch((err) => {
        reject(err);
      });
  });
};
