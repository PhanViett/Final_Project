import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  loading: false,
  isLastLogin: false,
  listIdChecked: [],
  listIdCheckedPVCM: [],
  listIdCheckedVTHN: [],
  doiTuong: {},
  checkedValidate: {
    TTCN: true,
    PVCMvsVTHN: true,
  },
  DataCVHD: {},
  DataVT: {},
  validateTTCN: false,
  validatePVCMVTHN: false,
  isSubmitted: false,
};

export const commonSlice = createSlice({
  name: "common",
  initialState,
  reducers: {
    setIsLastLogin(state, action) {
      state.isLastLogin = action.payload;
    },
    setListIdChecked(state, action) {
      state.listIdChecked = action.payload;
    },
    setListIdCheckedPVCM(state, action) {
      state.listIdCheckedPVCM = action.payload;
    },
    setListIdCheckedVTHN(state, action) {
      state.listIdCheckedVTHN = action.payload;
    },
    setDoiTuongAll(state, action) {
      state.doiTuong = action.payload;
    },
    setDoiTuong(state, action) {
      state.doiTuong = {
        ...state.doiTuong,
        [action.payload.key]: action.payload.value,
      };
    },
    setDataCVHDAll(state, action) {
      state.DataCVHD = action.payload;
    },
    setDataCVHDItem(state, action) {
      state.DataCVHD = {
        ...state.DataCVHD,
        [action.payload.key]: action.payload.value,
      };
    },
    setDataVTAll(state, action) {
      state.DataVT = action.payload;
    },
    setDataVTItem(state, action) {
      state.DataVT = {
        ...state.DataVT,
        [action.payload.key]: action.payload.value,
      };
    },
    setValidateTTCN(state, action) {
      state.validateTTCN = action.payload;
    },
    setValidatePVCMVTHN(state, action) {
      state.validatePVCMVTHN = action.payload;
    },
    setIsSubmitted(state, action) {
      state.isSubmitted = action.payload;
    },
  },
});

// actions
export const commonActions = commonSlice.actions;
// reducers
const commonReducer = commonSlice.reducer;
export default commonReducer;
// selectors
export const selectIsLastLogin = (state) => state.common.isLastLogin
export const selectListIdChecked = (state) => state.common.listIdChecked;
export const selectListIdCheckedPVCM = (state) =>
  state.common.listIdCheckedPVCM;
export const selectListIdCheckedVTHN = (state) =>
  state.common.listIdCheckedVTHN;
export const doiTuong = (state) => state.common.doiTuong;
export const selectDataCVHD = (state) => state.common.DataCVHD;
export const selectDataVT = (state) => state.common.DataVT;
export const selectCheckedValidate = (state) => state.common.checkedValidate;
export const selectValidateTTCN = (state) => state.common.validateTTCN
export const selectValidatePVCMVTHN = (state) => state.common.validatePVCMVTHN
export const selectIsSubmitted = (state) => state.common.isSubmitted
