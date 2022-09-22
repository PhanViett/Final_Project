import * as Actions from "./constants";

export function loginSuccess({ dataLogin }) {
  return {
    type: Actions.LOG_IN_SUCCESS,
    payload: dataLogin,
  };
}

export function updateUserSuccess({ dataUser }) {
  return {
    type: Actions.UPDATE_USER_SUCCESS,
    payload: dataUser,
  };
}

export function logout() {
  return {
    type: Actions.LOG_OUT,
  };
}
