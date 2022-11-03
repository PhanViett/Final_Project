import { fork, take } from "redux-saga/effects";
import { authActions } from "./authSlice";

function* handleLogin(payload) {
  yield console.log("handleLogin", payload);
}
function* handleLogout() {
  yield console.log("handle logout");
}
function* handleLoginSuccess() { }
function* watchLoginFlow() {
  while (true) {
    const action = yield take(authActions.login.type);
    yield fork(handleLogin, action.payload);

    yield take(authActions.logout.type);
    yield fork(handleLogout);
  }
}

export default function* authSaga() {
  //   yield fork(watchLoginFlow);
  //   yield takeEvery(authActions.loginSuccess.type, handleLogin);
}
