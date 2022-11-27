/* eslint-disable import/no-anonymous-default-export */
const API_URL = process.env.REACT_APP_API_URL;
const PATH_V1 = process.env.REACT_APP_PATH_V1;
const PATH_V2 = process.env.REACT_APP_PATH_V2;
const PATH_CDN = process.env.REACT_APP_CDN_URL;
const API_LOCATION_URL = process.env.REACT_APP_LOCATION_API_URL;

export default {
    CDN: PATH_CDN,
    API_LOGIN: API_URL + "login",
    API_REGISTER: API_URL + "register",
    API_GET_USER: API_URL + "auth/get_current_user",

    API_TINH_THANH: API_URL + PATH_V1 + "danh-muc/tinh-thanh",
    API_QUAN_HUYEN: API_URL + PATH_V1 + "danh-muc/quan-huyen",
    API_XA_PHUONG: API_URL + PATH_V1 + "danh-muc/xa-phuong",
    
    // PUBLIC QUAN, TINH, PHUONG
    API_TINH_THANH_PUBLIC: API_LOCATION_URL + PATH_V2 + "danhmuc/location/tinh-thanh/get-all",
    API_QUAN_HUYEN_PUBLIC: API_LOCATION_URL + PATH_V2 + "danhmuc/location/quan-huyen/get-all/",
    API_XA_PHUONG_PUBLIC: API_LOCATION_URL + PATH_V2 + "danhmuc/location/xa-phuong/get-all/",
    API_NOI_CAP_PUBLIC: API_LOCATION_URL + PATH_V2 + "danhmuc/location/CA-tinh-thanh",
    
    // FILE UPLOAD
    API_FILE_UPLOAD: API_URL + "file/upload",

    // QUAN LY NGUOI DUNG
    API_QUAN_LY_NGUOI_DUNG: API_URL + PATH_V1 + "user-get-list",
    API_QUAN_LY_NGUOI_DUNG_CREATE: API_URL + PATH_V1 + "user-create",
    API_QUAN_LY_NGUOI_DUNG_UPDATE: API_URL + PATH_V1 + "user-update",
    API_QUAN_LY_NGUOI_DUNG_DELETE: API_URL + PATH_V1 + "user-delete",
    API_QUAN_LY_NGUOI_DUNG_INFO: API_URL + PATH_V1 + "user-info",
    API_QUAN_LY_NGUOI_DUNG_STATIC: API_URL + PATH_V1 + "user-static",

    // QUAN LY LICH SU
    API_QUAN_LY_LICH_SU: API_URL + PATH_V1 + "record-get-list",
    API_QUAN_LY_LICH_SU_CREATE: API_URL + PATH_V1 + "record-create",
    API_QUAN_LY_LICH_SU_UPDATE: API_URL + PATH_V1 + "record-update",
    API_QUAN_LY_LICH_SU_DELETE: API_URL + PATH_V1 + "record-delete",

    // QUAN LY TIN TUC
    API_QUAN_LY_TIN_TUC: API_URL + PATH_V1 + "tin-tuc-get-list",
    API_QUAN_LY_TIN_TUC_LIST_VIEW: API_URL + PATH_V1 + "tin-tuc-get-list-view",
    API_QUAN_LY_TIN_TUC_DETAIL: API_URL + PATH_V1 + "tin-tuc-detail",
    API_QUAN_LY_TIN_TUC_CREATE: API_URL + PATH_V1 + "tin-tuc-create",
    API_QUAN_LY_TIN_TUC_UPDATE: API_URL + PATH_V1 + "tin-tuc-update",
    API_QUAN_LY_TIN_TUC_DELETE: API_URL + PATH_V1 + "tin-tuc-delete",
};
