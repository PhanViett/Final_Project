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

    // FILE UPLOAD
    API_FILE_UPLOAD: API_URL + "file/upload",

    // QUAN LY NGUOI DUNG
    API_QUAN_LY_NGUOI_DUNG: API_URL + PATH_V1 + "user-get-list",
    API_QUAN_LY_NGUOI_DUNG_CREATE: API_URL + PATH_V1 + "user-create",
    API_QUAN_LY_NGUOI_DUNG_UPDATE: API_URL + PATH_V1 + "user-update",
    API_QUAN_LY_NGUOI_DUNG_DELETE: API_URL + PATH_V1 + "user-delete",
    API_QUAN_LY_NGUOI_DUNG_INFO: API_URL + PATH_V1 + "user-info",


    // QUAN LY LICH SU
    API_QUAN_LY_LICH_SU: API_URL + PATH_V1 + "record-get-list",
    API_QUAN_LY_LICH_SU_CREATE: API_URL + PATH_V1 + "record-create",
    API_QUAN_LY_LICH_SU_UPDATE: API_URL + PATH_V1 + "record-update",
    API_QUAN_LY_LICH_SU_DELETE: API_URL + PATH_V1 + "record-delte",
};
