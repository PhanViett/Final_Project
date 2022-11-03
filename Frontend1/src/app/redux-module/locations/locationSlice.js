import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    loading: false,
    listTinhThanh: [],
    listQuanHuyen: [],
    listXaPhuong: [],
    listNoiCap: [],
    loai: ""
};

export const locationSlice = createSlice({
    name: "location",

    initialState,
    reducers: {
        getTinhThanh(state, action) {
            state.loading = true;
        },
        getTinhThanhSuccess(state, action) {
            state.loading = false;
            state.listTinhThanh = action.payload;
        },
        getTinhThanhFailed(state) {
            state.loading = false;
        },

        getQuanHuyen(state, action) {
            state.loading = true;
        },
        getQuanHuyenSuccess(state, action) {
            state.loading = false;
            state.listQuanHuyen = action.payload.results;
            state.loai = action.payload.loai;
        },
        getQuanHuyenFailed(state) {
            state.loading = false;
        },

        getXaPhuong(state, action) {
            state.loading = true;
        },
        getXaPhuongSuccess(state, action) {
            state.loading = false;
            state.listXaPhuong = action.payload.results;
            state.loai = action.payload.loai;
        },
        getXaPhuongFailed(state) {
            state.loading = false;
        },

        getNoiCap(state, action) {
            state.loading = true;
        },
        getNoiCapSuccess(state, action) {
            state.loading = false;
            state.listNoiCap = action.payload;
        },
        getNoiCapFailed(state) {
            state.loading = false;
        },
    }
})

export const locationActions = locationSlice.actions

const locationReducer = locationSlice.reducer;
export default locationReducer;

export const selectLoading = (state) => state.location.loading;
export const selectListTinhThanh = (state) => state.location.listTinhThanh;
export const selectListQuanHuyen = (state) => state.location.listQuanHuyen;
export const selectListXaPhuong = (state) => state.location.listXaPhuong;
export const selectListNoiCap = (state) => state.location.listNoiCap;
