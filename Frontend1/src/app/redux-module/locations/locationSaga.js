import { call, put, takeEvery } from "redux-saga/effects";
import { locationActions, } from "./locationSlice";
import { getListQuanHuyen, getListTinhThanh, getListXaPhuong, getCATinhThanh } from "./service";

function* handleTinhThanh({ payload }) {
    try {
        const resultsTinhThanh = yield call(getListTinhThanh, payload);

        if (resultsTinhThanh) {
            yield put({
                type: locationActions.getTinhThanhSuccess.type,
                payload: resultsTinhThanh,
            });
        }
    } catch (e) {
        yield put({
            type: locationActions.getTinhThanhFailed.type,
        });
    }
}

function* handleQuanHuyen({ payload }) {
    try {
        const resultsQuanHuyen = yield call(getListQuanHuyen, payload);

        if (resultsQuanHuyen) {
            yield put({
                type: locationActions.getQuanHuyenSuccess.type,
                payload: resultsQuanHuyen,
            });
        }
    } catch (e) {
        yield put({
            type: locationActions.getQuanHuyenFailed.type,
        });
    }
}

function* handleXaPhuong({ payload }) {
    try {
        const resultsXaPhuong = yield call(getListXaPhuong, payload);

        if (resultsXaPhuong) {
            yield put({
                type: locationActions.getXaPhuongSuccess.type,
                payload: resultsXaPhuong,
            });
        }
    } catch (e) {
        yield put({
            type: locationActions.getXaPhuongFailed.type,
        });
    }
}

function* handleNoiCap({ payload }) {
    try {
        const resultsNoiCap = yield call(getCATinhThanh, payload);

        if (resultsNoiCap) {
            yield put({
                type: locationActions.getNoiCapSuccess.type,
                payload: resultsNoiCap,
            });
        }
    } catch (e) {
        yield put({
            type: locationActions.getNoiCapFailed.type,
        });
    }
}

export default function* locationSaga() {
    //   yield fork(watchLoginFlow);
    yield takeEvery(locationActions.getTinhThanh.type, handleTinhThanh);
    yield takeEvery(locationActions.getQuanHuyen.type, handleQuanHuyen);
    yield takeEvery(locationActions.getXaPhuong.type, handleXaPhuong);
    yield takeEvery(locationActions.getNoiCap.type, handleNoiCap);


}
