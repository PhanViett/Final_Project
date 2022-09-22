import { createSelector } from "reselect";
export const auth = (state) => state.auth;

export const isAuthorized = createSelector(auth, (data) =>
  data.get("isAuthorized")
);

export const access_token = createSelector(auth, (data) =>
  data.get("access_token")
);

export const permissions = createSelector(auth, (data) =>
  data.get("permissions")
);


