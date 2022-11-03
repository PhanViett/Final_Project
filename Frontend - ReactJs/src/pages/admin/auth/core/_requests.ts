import axios from "axios";
import { AuthModel, UserModel } from "./_models";

import api from "../../../../configs/api";

const API_URL = process.env.REACT_APP_API_URL;

export const REGISTER_URL = `${API_URL}/register`;
export const REQUEST_PASSWORD_URL = `${API_URL}/forgot_password`;

// Server should return AuthModel
export function login(username: string, password: string) {
  return axios.post<AuthModel>(api.API_LOGIN, {
    username,
    password,
  });
}

// Server should return AuthModel
export function register(
  email: string,
  firstname: string,
  lastname: string,
  password: string,
  password_confirmation: string
) {
  return axios.post(REGISTER_URL, {
    email,
    first_name: firstname,
    last_name: lastname,
    password,
    password_confirmation,
  });
}

// Server should return object => { result: boolean } (Is Email in DB)
export function requestPassword(email: string) {
  return axios.post<{ result: boolean }>(REQUEST_PASSWORD_URL, {
    email,
  });
}

export function getUserByToken(token: string) {
  return axios.post<UserModel>(
    api.API_GET_USER,
    {},
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
}
