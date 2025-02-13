import { apiClient } from "./apiClient";
import { ApiClientParams, TradeRequest, ScheduledTradeResponse } from "./types";

const authApi = "trades/";

export const scheduledTrade = async (tradeData: TradeRequest) => {
  const options: ApiClientParams<TradeRequest> = {
    url: `${authApi}schedule/`,
    method: "POST",
    data: tradeData,
  };
  return await apiClient<TradeRequest, {}>(options);
};

export const getScheduled = async () => {
  const options: ApiClientParams<{}> = {
    url: `${authApi}get_scheduled/`,
    method: "GET",
  };
  return await apiClient<{}, { data: ScheduledTradeResponse[] }>(options);
};

export const updateScheduled = async (tradeData: ScheduledTradeResponse) => {
  const options: ApiClientParams<ScheduledTradeResponse> = {
    url: `${authApi}update_scheduled/`,
    method: "PUT",
    data: tradeData,
  };
  return await apiClient<ScheduledTradeResponse, {}>(options);
};

export const deleteScheduled = async (id: string) => {
  const options: ApiClientParams<{}> = {
    url: `${authApi}delete_scheduled/${id}/`,
    method: "DELETE",
  };
  return await apiClient<{}, {}>(options);
};
