/* eslint-disable import/no-anonymous-default-export */
const API_URL = process.env.REACT_APP_API_URL;
const PATH_V1 = process.env.REACT_APP_PATH_V1;
const PATH_CDN = process.env.REACT_APP_CDN_URL;

export default {
    CDN: PATH_CDN,
    API_LOGIN: API_URL + "login",
    API_REGISTER: API_URL + "register",
    API_GET_USER: API_URL + "auth/get_current_user",

    API_TINH_THANH: API_URL + PATH_V1 + "danh-muc/tinh-thanh",
    API_QUAN_HUYEN: API_URL + PATH_V1 + "danh-muc/quan-huyen",
    API_XA_PHUONG: API_URL + PATH_V1 + "danh-muc/xa-phuong",
    // PUBLIC QUAN, TINH, PHUONG
    API_TINH_THANH_PUBLIC: API_URL + PATH_V1 + "public/tinh-thanh",
    API_QUAN_HUYEN_PUBLIC: API_URL + PATH_V1 + "public/quan-huyen",
    API_XA_PHUONG_PUBLIC: API_URL + PATH_V1 + "public/xa-phuong",

    // QUAN LY NGUOI DUNG
    API_QUAN_LY_NGUOI_DUNG: API_URL + PATH_V1 + "user-get-list"

};
