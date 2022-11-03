import { combineReducers } from "redux";

import authReducer from "./auth/authSlice";
import commonReducer from "./common/commonSlice";
import locationReducer from "./locations/locationSlice";

const rootReducers = combineReducers({
  auth: authReducer,
  location: locationReducer,
  common: commonReducer,
});
export default rootReducers;
