import { ApiClientParams, ApiResponse } from "./types";
export const BASE_URL = "https://renoseharsh.pythonanywhere.com/api/";

const getCsrfTokenFromCookie = () => {
  const csrfToken = document.cookie
    .split(";")
    .find((cookie) => cookie.trim().startsWith("csrftoken="));
  return csrfToken ? csrfToken.split("=")[1] : "";
};

export const apiClient = async <T, R>({
  url,
  method,
  data,
}: ApiClientParams<T>): Promise<R & ApiResponse> => {
  try {
    const response = await fetch(`${BASE_URL}${url}`, {
      method,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCsrfTokenFromCookie(),
      },
      body: data ? JSON.stringify(data) : undefined,
      credentials: "include",
    });
    const responseData: R & { message: string } = await response.json();
    return { ...responseData, status: response.status };
  } catch (error) {
    console.error("apiClient error", error);
    throw error;
  }
};
