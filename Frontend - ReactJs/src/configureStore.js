import { createStore, applyMiddleware } from "redux";
import createSagaMiddleware from "redux-saga";
import rootSagas from "./sagas";
import { composeWithDevTools } from "redux-devtools-extension";
import { persistStore, persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage";
import { encryptTransform } from 'redux-persist-transform-encrypt';

import rootReducer from './reducers';

const sagaMiddleware = createSagaMiddleware();
const middleware = [sagaMiddleware];
const persistedReducer = persistReducer({
  key: "root",
  storage,
  whitelist: ['auth'],
  transforms: [
    encryptTransform({
      secretKey: 'my-super-secret-key',
      onError: function (error) {
        console.log('encryptTransform', error)
        // Handle the error.
      },
    }),
  ],
}, rootReducer);


export default function configureStore() {
  const store = createStore(
    persistedReducer,
    composeWithDevTools(applyMiddleware(...middleware))
  );
  sagaMiddleware.run(rootSagas);

  const persistor = persistStore(store);
  return { store, persistor };
};
