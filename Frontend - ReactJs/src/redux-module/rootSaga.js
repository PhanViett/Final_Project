import { all } from "redux-saga/effects";
import authSaga from "./auth/authSaga";
import locationSaga from "./locations/locationSaga";
import notiSaga from "./noti/notiSaga";

export default function* rootSaga() {
  yield all([authSaga(), notiSaga(), locationSaga()]);
}
