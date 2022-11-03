import {
  FC,
  useState,
  useEffect,
  createContext,
  useContext,
  useRef,
  Dispatch,
  SetStateAction,
} from "react";
import { AuthModel, UserModel } from "./_models";
import * as authHelper from "./AuthHelpers";
import { getUserByToken } from "./_requests";

type AuthContextProps = {
  auth: AuthModel | undefined;
  saveAuth: (auth: AuthModel | undefined) => void;
  currentUser: UserModel | undefined;
  roleUser: any | undefined;
  setCurrentUser: Dispatch<SetStateAction<UserModel | undefined>>;
  setRoleUser: Dispatch<SetStateAction<any | undefined>>;
  logout: () => void;
};

const initAuthContextPropsState = {
  auth: authHelper.getAuth(),
  saveAuth: () => {},
  currentUser: undefined,
  roleUser: undefined,
  setCurrentUser: () => {},
  setRoleUser: () => {},
  logout: () => {},
};

const AuthContext = createContext<AuthContextProps>(initAuthContextPropsState);

const useAuth = () => {
  return useContext(AuthContext);
};

const AuthProvider: FC = ({ children }) => {
  const [auth, setAuth] = useState<AuthModel | undefined>(authHelper.getAuth());
  const [currentUser, setCurrentUser] = useState<UserModel | undefined>();
  const [roleUser, setRoleUser] = useState<any | undefined>();

  const saveAuth = (auth: AuthModel | undefined) => {
    setAuth(auth);
    if (auth) {
      authHelper.setAuth(auth);
    } else {
      authHelper.removeAuth();
    }
  };

  const logout = () => {
    saveAuth(undefined);
    setCurrentUser(undefined);
    setRoleUser(undefined);
  };

  return (
    <AuthContext.Provider
      value={{
        auth,
        saveAuth,
        currentUser,
        roleUser,
        setCurrentUser,
        setRoleUser,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

const AuthInit: FC = ({ children }) => {
  const { auth, logout, setCurrentUser, setRoleUser } = useAuth();
  const didRequest = useRef(false);
  // We should request user by authToken (IN OUR EXAMPLE IT'S API_TOKEN) before rendering the application
  useEffect(() => {
    const requestUser = async (apiToken: string) => {
      try {
        if (!didRequest.current) {
          const { data } = await getUserByToken(apiToken);
          if (data) {
            setCurrentUser(data);
            if (data?.assigned_role) {
              setRoleUser(data?.assigned_role);
            }
          }
        }
      } catch (error) {
        console.error(error);
        if (!didRequest.current) {
          logout();
        }
      }
      return () => (didRequest.current = true);
    };

    if (auth && auth.access_token) {
      requestUser(auth.access_token);
    } else {
      logout();
    }
    // eslint-disable-next-line
  }, []);

  return <>{children}</>;
};

export { AuthProvider, AuthInit, useAuth };
