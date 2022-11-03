import { all } from "redux-saga/effects";
import authSaga from "./auth/authSaga";
import locationSaga from "./locations/locationSaga";

export default function* rootSaga() {
  yield all([authSaga(), locationSaga()]);
}
