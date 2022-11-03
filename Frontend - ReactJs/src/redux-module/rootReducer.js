import { combineReducers } from "redux";

import authReducer from "./auth/authSlice";
import notiReducer from "./noti/notiSlice";
import commonReducer from "./common/commonSlice";
import locationReducer from "./locations/locationSlice";

const rootReducers = combineReducers({
  auth: authReducer,
  noti: notiReducer,
  location: locationReducer,
  common: commonReducer,
});
export default rootReducers;
