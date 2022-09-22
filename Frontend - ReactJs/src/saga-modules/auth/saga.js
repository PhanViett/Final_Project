import { takeEvery } from "redux-saga/effects";
import * as Actions from "./constants";

/**
 * get transfer log
 * @returns {IterableIterator<*>}
 */
function* loginEffectSaga({ dataUpdate, reloadUpdate }) {}

export default function* authSaga() {
  yield takeEvery(Actions.LOG_IN, loginEffectSaga);
}
