export interface ApiClientParams<T> {
  url: string;
  method: "GET" | "POST" | "PUT" | "DELETE";
  data?: T;
}

export interface ApiResponse {
  message: string;
  status: number;
}

export interface AuthData {
  username: string;
  password: string;
}

export interface UserData {
  username: string;
}

export interface accesstoken {
  paper_token: string;
  live_token: string;
  paper_accounts: number;
  live_accounts: number;
}

export interface UpdateTokenRequest {
  paper_token?: string;
  live_token?: string;
}

export interface AcountsResponse {
  paper_accounts: string[];
  live_accounts: string[];
}

export interface TradeRequest {
  account_id: string;
  pair: string;
  units?: string;
  percentage?: string;
  take_profit: string;
  stop_loss: string;
  scheduled_time: string;
  action: "buy" | "sell";
}

export interface ScheduledTradeResponse {
  account_id: string;
  account_type: string;
  pair: string;
  units?: string;
  percentage?: string;
  take_profit: string;
  stop_loss: string;
  scheduled_time: string;
  action: string;
  id: string;
  status: string;
}
