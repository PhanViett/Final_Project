import { configureStore } from "@reduxjs/toolkit";
import {
  FLUSH, PAUSE,
  PERSIST, persistReducer, persistStore, PURGE,
  REGISTER, REHYDRATE
} from "redux-persist";
import { encryptTransform } from "redux-persist-transform-encrypt";
import storage from "redux-persist/lib/storage";
import createSagaMiddleware from "redux-saga";
import rootReducers from "./rootReducer";
import rootSaga from "./rootSaga";

const sagaMiddleware = createSagaMiddleware();

// const persistConfig = {
//   key: "root",
//   version: 1,
//   storage,
// };

// const persistedReducer = persistReducer(persistConfig, rootReducers);

const persistedReducer = persistReducer(
  {
    key: "root",
    storage,
    whitelist: ["auth"],
    transforms: [
      encryptTransform({
        secretKey: "abc123",
        onError: function (error) {
          console.log("encryptTransform", error);
          // Handle the error.
        },
      }),
    ],
  },
  rootReducers
);

const store = configureStore({
  reducer: persistedReducer,
  devTools: true,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    }).concat(sagaMiddleware),
});
sagaMiddleware.run(rootSaga);

export const persistor = persistStore(store);

export default store;
