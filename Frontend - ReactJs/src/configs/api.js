/* eslint-disable import/no-anonymous-default-export */
const API_URL = process.env.REACT_APP_API_URL;
const PATH_V1 = process.env.REACT_APP_PATH_V1;
const PATH_V2 = process.env.REACT_APP_PATH_V2;
const PATH_CDN = process.env.REACT_APP_CDN_URL;

const PUBLIC = "public/";

export default {
  CDN: PATH_CDN,
  API_LOGIN: API_URL + "auth/login",
  API_TINH_THANH: API_URL + PATH_V1 + "danh-muc/tinh-thanh",
  API_QUAN_HUYEN: API_URL + PATH_V1 + "danh-muc/quan-huyen",
  API_XA_PHUONG: API_URL + PATH_V1 + "danh-muc/xa-phuong",
  // PUBLIC QUAN, TINH, PHUONG
  API_TINH_THANH_PUBLIC: API_URL + PATH_V1 + "public/tinh-thanh",
  API_QUAN_HUYEN_PUBLIC: API_URL + PATH_V1 + "public/quan-huyen",
  API_XA_PHUONG_PUBLIC: API_URL + PATH_V1 + "public/xa-phuong",
  // LIST_NEWS: API_URL + PATH_V1 + "tin-tuc",
  ADD_NEW: API_URL + PATH_V1 + "tin-tuc/create",
  NEWS: API_URL + PATH_V1 + "tin-tuc",
  NEWS_PUBLIC: API_URL + PATH_V1 + PUBLIC + "tin-tuc",
  LIST_NEWS: API_URL + PATH_V1 + "tin-tuc/list-tin-tuc",

  LIST_DON_VI: API_URL + PATH_V1 + "don-vi",
  LIST_DON_VI_PUBLIC: API_URL + PATH_V1 + PUBLIC + "don-vi",
  // LIST_NEWS: API_URL + PATH_V1 + "tin_tuc",

  LIST_USER: API_URL + PATH_V1 + "users",

  LIST_USER_UNIT: API_URL + PATH_V1 + "don-vi/get-nguoi-dung",

  // danh mục
  // LIST_CATEGORY: API_URL + PATH_V1 + "danh_muc",
  //faq
  LIST_FAQ: API_URL + PATH_V1 + "faqs",
  LIST_FAQ_PUBLIC: API_URL + PATH_V1 + "public/faq",
  //danh muc tin tuc
  LIST_CATEGORY: API_URL + PATH_V1 + "danh-muc/tin-tuc",
  //danh muc văn bản
  CATEGORY_DOCUMENT: API_URL + PATH_V1 + "danh-muc/van-ban",
  LIST_DOCUMENT: API_URL + PATH_V1 + "van-ban/list-van-ban",
  DOCUMENT: API_URL + PATH_V1 + "van-ban",
  DOCUMENT_PUBLIC: API_URL + PATH_V1 + "public/van-ban",
  //danh muc tin tuc tong hop
  LIST_ALL_CATEGORY_NEWS:
    API_URL + PATH_V1 + "danh-muc/tin-tuc/get-all-parents",
  LIST_CATEGORY_NEWS: API_URL + PATH_V1 + "danh-muc/tin-tuc/get-parents",
  //tag
  SEARCH_TAGS: API_URL + PATH_V1 + "tags/search",
  TAGS: API_URL + PATH_V1 + "tags",
  TAGS_PUBLIC: API_URL + PATH_V1 + PUBLIC + "tag",
  CDN_IMAGES: "https://cdn-dev.yte360.com/",
  //vai tro
  ROLES: API_URL + PATH_V1 + "vai-tro",
  //cai dat he thong
  MANAGE_HOME: API_URL + PATH_V1 + "quan-ly/home-page",
  DETAIL_MANAGE_HOME: API_URL + PATH_V1 + "quan-ly/home-page/getDetail",
  MAP_PUBLIC: API_URL + PATH_V1 + PUBLIC + "so-do",
  //Lien he
  CONTACT: API_URL + PATH_V1 + "lien-he/",
  CONTACT_PUBLIC: API_URL + PATH_V1 + PUBLIC + "lien-he",
  REPORT_CA_MAC_PUBLIC: API_URL + PATH_V1 + PUBLIC + "bao-cao-ca-mac",
  REPORT_DIEU_TRI_PUBLIC: API_URL + PATH_V1 + PUBLIC + "bao-cao-dieu-tri",
  REPORT_TONG_HOP_PUBLIC: API_URL + PATH_V1 + PUBLIC + "bao-cao-tong-hop",
  REPORT_TIEM_CHUNG_PUBLIC: API_URL + PATH_V1 + PUBLIC + "bao-cao-mui-tiem",
  REPORT_NGUY_CO_PUBLIC: API_URL + PATH_V1 + PUBLIC + "bao-cao-nguy-co",
  LIST_CONTACT: API_URL + PATH_V1 + "lien-he/get-list",


  //danh sach import
  IMPORT_DIEU_TRI: API_URL + PATH_V2 + "ho-so-dieu-tri/import",
  IMPORT_MAC_BENH: API_URL + PATH_V2 + "ho-so-mac-benh/import",
  IMPORT_NHOM_NGUY_CO: API_URL + PATH_V2 + "ho-so-nhom-nguy-co/import",
  IMPORT_TIEM_CHUNG: API_URL + PATH_V2 + "ho-so-tiem-chung/import",
  IMPORT_CAP_DO_DICH: API_URL + PATH_V2 + "ho-so-cap-do-dich/import",
  IMPORT_DON_VI: API_URL + PATH_V1 + "don-vi/import",

  //ho so nang luc theo don vi
  HSNLTDV: API_URL + PATH_V1 + "public/ho-so-nang-luc-theo-don-vi",
  //lich su import
  HISTORY_IMPORT_DON_VI: API_URL + PATH_V2 + "lich-su-import/don-vi",
  HISTORY_IMPORT_NHOM_CO_NGUY_CO: API_URL + PATH_V2 + "lich-su-import/ho-so-nhom-nguy-co",
  HISTORY_IMPORT_HO_SO_DIEU_TRI: API_URL + PATH_V2 + "lich-su-import/ho-so-dieu-tri",
  HISTORY_IMPORT_HO_SO_MAC_BENH: API_URL + PATH_V2 + "lich-su-import/ho-so-mac-benh",
  HISTORY_IMPORT_HO_SO_TIEM_CHUNG: API_URL + PATH_V2 + "lich-su-import/ho-so-tiem-chung",
  HISTORY_IMPORT_HO_SO_CAP_DO_DICH: API_URL + PATH_V2 + "lich-su-import/ho-so-cap-do-dich",
  //lich su import highlight
  HIGHLIGHT_IMPORT_NHOM_CO_NGUY_CO: API_URL + PATH_V2 + "lich-su-import/ho-so-nhom-nguy-co/highlight",
  HIGHLIGHT_IMPORT_HO_SO_DIEU_TRI: API_URL + PATH_V2 + "lich-su-import/ho-so-dieu-tri/highlight",
  HIGHLIGHT_IMPORT_HO_SO_MAC_BENH: API_URL + PATH_V2 + "lich-su-import/ho-so-mac-benh/highlight",
  HIGHLIGHT_IMPORT_HO_SO_TIEM_CHUNG: API_URL + PATH_V2 + "lich-su-import/ho-so-tiem-chung/highlight",
  HIGHLIGHT_IMPORT_HO_SO_CAP_DO_DICH: API_URL + PATH_V2 + "lich-su-import/ho-so-cap-do-dich/highlight",

  //Cap nhat file mau
  CAP_NHAT_FILE_MAU: API_URL + PATH_V1 + "quan-ly/set-excel-mac-dinh",
  //Sliders
  SLIDER_MAIN: API_URL + PATH_V1 + "slider/main",
  SLIDER_ITEM: API_URL + PATH_V1 + "slider/item",
  PUBLIC_SLIDER_HOME: API_URL + PATH_V1 + PUBLIC + "slider"

};
