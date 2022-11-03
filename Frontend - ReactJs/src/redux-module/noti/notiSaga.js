import { call, put, takeEvery } from "redux-saga/effects";
import { notiActions } from "./notiSlice";
import { getListNoti } from "./service";

function* handleNoti({ payload }) {
  try {
    const resultsListNoti = yield call(getListNoti, payload);

    if (resultsListNoti) {
      yield put({
        type: notiActions.getNotiSuccess.type,
        payload: resultsListNoti,
      });
    }
  } catch (e) {
    yield put({
      type: notiActions.getNotiFailed.type,
    });
  }
}

export default function* notiSaga() {
  //   yield fork(watchLoginFlow);
  yield takeEvery(notiActions.getNoti.type, handleNoti);
}
