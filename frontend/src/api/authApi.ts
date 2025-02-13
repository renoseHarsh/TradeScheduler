import { apiClient } from "./apiClient";
import {
  accesstoken,
  ApiClientParams,
  AuthData,
  UpdateTokenRequest,
  UserData,
  AcountsResponse,
} from "./types";

const authApi = "auth/";

export const loginUser = async (loginData: AuthData) => {
  const options: ApiClientParams<AuthData> = {
    url: `${authApi}login/`,
    method: "POST",
    data: loginData,
  };
  return await apiClient<AuthData, { data: UserData }>(options);
};

export const registerUser = async (loginData: AuthData) => {
  const options: ApiClientParams<AuthData> = {
    url: `${authApi}register/`,
    method: "POST",
    data: loginData,
  };
  return await apiClient<AuthData, { data: UserData }>(options);
};

export const getUser = async () => {
  const options: ApiClientParams<null> = {
    url: `${authApi}user/`,
    method: "GET",
  };
  return await apiClient<null, { data: UserData }>(options);
};

export const logoutUser = async () => {
  const options: ApiClientParams<null> = {
    url: `${authApi}logout/`,
    method: "POST",
  };
  return await apiClient<null, {}>(options);
};

export const getTokens = async () => {
  const options: ApiClientParams<null> = {
    url: `${authApi}tokens/`,
    method: "GET",
  };
  return await apiClient<null, { data: accesstoken }>(options);
};

export const updateTokens = async (tokenData: UpdateTokenRequest) => {
  const options: ApiClientParams<UpdateTokenRequest> = {
    url: `${authApi}updatetokens/`,
    method: "PUT",
    data: tokenData,
  };
  return await apiClient<UpdateTokenRequest, { data: accesstoken }>(options);
};

export const getAccounts = async () => {
  const options: ApiClientParams<null> = {
    url: `${authApi}accounts/`,
    method: "GET",
  };
  return await apiClient<null, { data: AcountsResponse }>(options);
};
