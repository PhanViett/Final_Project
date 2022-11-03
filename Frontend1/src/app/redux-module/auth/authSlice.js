import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  isLoggedIn: false,
  logging: false,
  access_token: undefined,
  currentUser: undefined,
  roleUser: undefined,
};

export const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    login(state, action) {
      state.logging = true;
    },
    loginSuccess(state, action) {
      state.logging = false;
      state.isLoggedIn = true;
      state.currentUser = action.payload?.data;
      state.access_token = action.payload?.access_token;
      state.roleUser = action.payload?.data?.assigned_role[0]?.ten_en;
    }, 
    setCurrentUser(state, action ) {
      state.currentUser = action.payload;
    },
    changeToken(state, action) {
      state.access_token = "test";
    },
    loginFailure(state) {
      state.logging = false;
    },
    logout(state) {
      state.isLoggedIn = false;
      state.currentUser = undefined;
    },
  },
});

// actions
export const authActions = authSlice.actions;
// reducers
const authReducer = authSlice.reducer;
export default authReducer;
// selectors
export const selectIsLoggedIn = (state) => state.auth.isLoggedIn;
export const selectIsLogging = (state) => state.auth.logging;
export const selectCurrentUser = (state) => state.auth.currentUser;
export const selectRoleUser = (state) => state.auth.roleUser;
export const selectAccessToken = (state) => state.auth.access_token;
