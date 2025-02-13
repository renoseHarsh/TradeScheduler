import { SubmitHandler, useForm } from "react-hook-form";
import Modal from "../../../Utils/Modal";
import { useEffect, useId, useState } from "react";
import { getAccounts } from "../../../api/authApi";
import { TradeRequest } from "../../../api/types";
import { scheduledTrade } from "../../../api/tradeApi";

export default function ScheduleModal({ onClose }: { onClose: () => void }) {
  const [isPercent, setIsPercent] = useState(false);
  const accountId = useId();
  const paidId = useId();
  const unitsId = useId();
  const takeProfitId = useId();
  const stopLossId = useId();
  const scheduledTimeId = useId();
  const [error, setError] = useState<string | null>(null);

  const instruments = [
    ["EUR_USD", "EURUSD"],
    ["AUD_USD", "AUDUSD"],
    ["USD_JPY", "USDJPY"],
    ["USD_CAD", "USDCAD"],
    ["NZD_USD", "NZDUSD"],
    ["AUD_JPY", "AUDJPY"],
    ["USD_CHF", "USDCHF"],
  ];

  const [accounts, setAccounts] = useState<{
    paper: string[];
    live: string[];
  }>({ paper: [], live: [] });

  useEffect(() => {
    const fetchAccounts = async () => {
      const response = await getAccounts();
      if (response.status === 200) {
        setAccounts({
          paper: response.data.paper_accounts,
          live: response.data.live_accounts,
        });
      }
    };
    fetchAccounts();
  }, []);

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors },
  } = useForm<TradeRequest>({ defaultValues: { action: "buy" } });
  const onSumbit: SubmitHandler<TradeRequest> = async (data) => {
    const response = await scheduledTrade(data);
    if (response.status === 201) {
      onClose();
    }
    setError(response.message);
  };

  return (
    <Modal onClose={onClose}>
      <div className="w-96 rounded-lg bg-white p-6 text-black shadow-lg">
        {/* Header */}
        <h2 className="mb-6 text-center text-3xl font-semibold text-blue-600">
          Schedule a Trade
        </h2>
        {/* Inpu area */}
        <form className="text-black" onSubmit={handleSubmit(onSumbit)}>
          {/* Account */}
          <div>
            <label
              htmlFor={accountId}
              className="block text-sm font-medium text-gray-700"
            >
              Account
            </label>
            <select
              id={accountId}
              defaultValue={"Select an account"}
              className="block w-full rounded-md border border-gray-300 bg-[#E0E0E0] px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              {...register("account_id", {
                required: "Need an account",
                validate: (value) =>
                  value !== "Select an account" || "Need an account",
              })}
            >
              <option disabled>Select an account</option>
              {accounts.paper.length > 0 && (
                <option disabled className="font-bold">
                  Paper account
                </option>
              )}
              {accounts.paper.map((data, index) => (
                <option key={index} value={data}>
                  {data}
                </option>
              ))}
              {accounts.live.length > 0 && (
                <option disabled className="font-bold">
                  Live account
                </option>
              )}
              {accounts.live.map((data, index) => (
                <option key={index} value={data}>
                  {data}
                </option>
              ))}
            </select>
            <span className="ml-1 text-sm text-red-500">
              {errors.account_id?.message}
            </span>
          </div>
          {/* Pair */}
          <div>
            <label
              htmlFor={paidId}
              className="block text-sm font-medium text-gray-700"
            >
              Pair
            </label>
            <select
              id={paidId}
              defaultValue={"Select a trading pair"}
              className="block w-full rounded-md border border-gray-300 bg-[#E0E0E0] px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              {...register("pair", {
                validate: (value) =>
                  value !== "Select a trading pair" || "Need a trading pair",
              })}
            >
              <option disabled>Select a trading pair</option>
              {instruments.map((data, index) => (
                <option key={index} value={data[0]}>
                  {data[1]}
                </option>
              ))}
            </select>
            <span className="ml-1 text-sm text-red-500">
              {errors.pair?.message}
            </span>
          </div>
          {/* Units/Percentage */}
          <div>
            <label
              htmlFor={unitsId}
              className="block text-sm font-medium text-gray-700"
            >
              {isPercent ? "Percentage" : "Units"}
            </label>
            <div className="flex items-center">
              {!isPercent && (
                <input
                  id={unitsId}
                  className="w-full rounded-md border border-gray-300 bg-[#E0E0E0] px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="units"
                  type="number"
                  {...register("units", {
                    min: { value: 1, message: "Need at least 1 unit" },
                    validate: (value) => {
                      if (isPercent) return true;
                      if (!value) return "Need units";
                    },
                  })}
                />
              )}
              {isPercent && (
                <input
                  id={unitsId}
                  className="w-full rounded-md border border-gray-300 bg-[#E0E0E0] px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="percentage"
                  type="number"
                  step={0.000000001}
                  {...register("percentage", {
                    max: { value: 100, message: "Invalid percentage" },
                    validate: (value) => {
                      if (!isPercent) return true;
                      if (!value) return "Need Percentage";
                      if (Number(value) > 0 && Number(value) <= 100)
                        return true;
                      return "Invalid Percentage";
                    },
                  })}
                />
              )}
              <div className="ml-4 flex items-center">
                <div
                  className={`relative inline-flex h-6 w-10 cursor-pointer items-center rounded-full transition-colors ${
                    isPercent ? "bg-blue-500" : "bg-gray-300"
                  }`}
                  onClick={() => {
                    setIsPercent(!isPercent);
                    setValue("units", undefined);
                    setValue("percentage", undefined);
                  }}
                >
                  <span
                    className={`absolute left-1 top-1 h-4 w-4 rounded-full bg-white shadow transition-transform ${
                      isPercent ? "translate-x-4" : ""
                    }`}
                  ></span>
                </div>
              </div>
            </div>
            <span className="ml-1 text-sm text-red-500">
              {!isPercent && errors.units?.message}
              {isPercent && errors.percentage?.message}
            </span>
          </div>
          {/* Take Profit */}
          <div>
            <label
              htmlFor={takeProfitId}
              className="block text-sm font-medium text-gray-700"
            >
              Take Profit
            </label>
            <input
              type="number"
              step={0.1}
              id={takeProfitId}
              className="block w-full rounded-md border border-gray-300 bg-[#E0E0E0] px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter take profit"
              {...register("take_profit", {
                required: "Need take profit",
                min: { value: 0.1, message: "Need at least 0.1" },
              })}
            />
            <span className="ml-1 text-sm text-red-500">
              {errors.take_profit?.message}
            </span>
          </div>
          {/* Stop Loss */}
          <div>
            <label
              htmlFor={stopLossId}
              className="block text-sm font-medium text-gray-700"
            >
              Stop Loss
            </label>
            <input
              type="number"
              step={0.1}
              id={stopLossId}
              className="block w-full rounded-md border border-gray-300 bg-[#E0E0E0] px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter stop loss"
              {...register("stop_loss", {
                required: "Need stop loss",
                min: { value: 0.1, message: "Need at least 0.1" },
              })}
            />
            <span className="ml-1 text-sm text-red-500">
              {errors.stop_loss?.message}
            </span>
          </div>
          {/* Schedule Time */}
          <div>
            <label
              htmlFor={scheduledTimeId}
              className="block text-sm font-medium text-gray-700"
            >
              Scheduled Time
            </label>
            <input
              type="datetime-local"
              id={scheduledTimeId}
              className="block w-full rounded-md border border-gray-300 bg-[#E0E0E0] px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              {...register("scheduled_time", {
                required: "Need a time",
                // validate: (value) =>
                //   new Date(value) > new Date() || "Invalid time",
              })}
            />
            <span className="ml-1 text-sm text-red-500">
              {errors.scheduled_time?.message}
            </span>
          </div>
          {/* Buy/Sell */}
          <div className="flex items-center">
            <p className="text-sm font-medium text-gray-700">Buy</p>
            <div
              className={`relative mx-2 inline-flex h-6 w-10 cursor-pointer items-center rounded-full transition-colors ${
                watch("action") === "sell" ? "bg-red-600" : "bg-green-700"
              }`}
              onClick={() =>
                setValue("action", watch("action") === "buy" ? "sell" : "buy")
              }
            >
              <span
                className={`absolute left-1 top-1 h-4 w-4 rounded-full bg-white shadow transition-transform ${
                  watch("action") === "sell" ? "translate-x-4" : ""
                }`}
              ></span>
            </div>
            <p className="text-sm font-medium text-gray-700">Sell</p>
          </div>
          {/* Buttons */}
          <div className="mt-6 flex justify-between gap-4">
            <button
              type="submit"
              className="flex-1 rounded-md bg-blue-600 py-2 text-white transition duration-200 hover:bg-blue-700 active:bg-blue-800"
            >
              Schedule
            </button>
            <button
              type="button"
              id="closeSceduleBtn"
              onClick={onClose}
              className="w-1/2 rounded-md bg-gray-500 py-2 text-center text-white transition duration-200 hover:bg-gray-600 active:bg-gray-700"
            >
              Cancel
            </button>
          </div>
          {error && <p className="text-center text-red-500">{error}</p>}
        </form>
      </div>
    </Modal>
  );
}
