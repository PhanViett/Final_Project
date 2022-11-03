import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  loading: false,
  listNoti: [],
  countUnreadNoti: null,
};

export const notiSlice = createSlice({
  name: "noti",
  initialState,
  reducers: {
    getNoti(state, action) {
      state.loading = true;
    },
    getNotiSuccess(state, action) {
      state.listNoti = action.payload.results;
      state.countUnreadNoti = action.payload.total_unread;
      state.loading = false;
    },
    getNotiFailed(state) {
      state.loading = false;
    },
  },
});

// actions
export const notiActions = notiSlice.actions;
// reducers
const notiReducer = notiSlice.reducer;
export default notiReducer;
// selectors
export const selectLoading = (state) => state.noti.loading;
export const selectListNoti = (state) => state.noti.listNoti;
export const selectCountUnreadNoti = (state) => state.noti.countUnreadNoti;
