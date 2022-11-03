import { createContext, useContext, useState } from "react";
import * as notiHelper from "./NotiHelpers";

const initNotiContextPropsState = {
  noti: notiHelper.getNoti(),
  saveNoti: () => {},
  setCurrentUser: () => {},
  setRoleUser: () => {},
};

const NotiContext = createContext(initNotiContextPropsState);

const useNoti = () => {
  return useContext(NotiContext);
};

const NotiProvider: FC = ({ children }) => {
  const [noti, setNoti] = useState(notiHelper.getNoti());
  const [currentNoti, setCurrentNoti] = useState();

  return (
    <NotiContext.Provider
      value={{
        noti,
      }}
    >
      {children}
    </NotiContext.Provider>
  );
};

export { NotiProvider, useNoti };
