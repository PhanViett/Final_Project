import * as Actions from "./constants";
import { fromJS } from "immutable";

export const initState = fromJS({
  isLoading: false,
  isAuthorized: false,
  user: {},
  access_token: "",
  permissions: {}
});

/**
 * Common reducer
 * @param state
 * @param action
 * @returns {*}
 */
function authReducer(state = initState, action = {}) {
  const { type, payload } = action;
  switch (type) {
    case Actions.LOG_IN:
      return {
        ...state,
        isLoading: true,
      };
    case Actions.LOG_OUT:
      return initState;
    case Actions.LOG_IN_SUCCESS:
      return {
        ...state,
        isLoading: false,
        user: payload.userInfo,
        isAuthorized: true,
        access_token: payload.access_token,
        permissions: payload.permissions
      };
    case Actions.UPDATE_USER_SUCCESS:
      return {
        ...state,
        isLoading: false,
        user: payload,
      };
    case Actions.LOG_IN_ERROR:
      return {
        ...state,
        isLoading: false,
        user: undefined,
      };
    default:
      return state;
  }
}

export default authReducer;
