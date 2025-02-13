import { useEffect, useId, useState } from "react";
import Modal from "../../../Utils/Modal";
import { SubmitHandler, useForm } from "react-hook-form";
import { getTokens, updateTokens } from "../../../api/authApi";
import { UpdateTokenRequest } from "../../../api/types";

type Input = {
  paper_token: string;
  live_token: string;
};

export default function TokenModal({ onClose }: { onClose: () => void }) {
  const paperLabelId = useId();
  const liveLabelId = useId();
  const [tokens, setTokens] = useState<Input>();
  const [updateError, setUpdateError] = useState("");
  const [loading, setLoading] = useState(true);
  const [accounts, setAccounts] = useState<{
    paper_accounts: number;
    live_accounts: number;
  }>();

  const { register, handleSubmit, reset } = useForm<Input>();

  useEffect(() => {
    const fetchTokens = async () => {
      const response = await getTokens();
      setTokens(response.data);
      reset(response.data);
      setAccounts(response.data);
      setLoading(false);
    };
    fetchTokens();
  }, [reset]);

  const onSubmit: SubmitHandler<Input> = async (data) => {
    if (
      data.paper_token == tokens?.paper_token &&
      data.live_token == tokens?.live_token
    )
      return;

    const options: UpdateTokenRequest = {};

    if (data.paper_token !== tokens?.paper_token)
      options.paper_token = data.paper_token;
    if (data.live_token !== tokens?.live_token)
      options.live_token = data.live_token;

    const respose = await updateTokens(options);
    setAccounts(respose.data);
    if (respose.status !== 200) setUpdateError(respose.message);
  };

  return (
    <Modal onClose={onClose}>
      <div className="w-96 rounded-lg bg-gradient-to-r from-[#4C6A92] to-[#2F4059] p-6 text-white shadow-lg">
        {/* Header */}
        <h2 className="mb-4 text-center text-2xl font-semibold">
          Manage Access Token
        </h2>
        <div className="relative inset-0 z-[100] h-full w-full bg-[#4C6A92]"></div>
        {/* Input area */}
        <form className="flex flex-col gap-6" onSubmit={handleSubmit(onSubmit)}>
          {/* Paper Token */}
          <div className="flex flex-col gap-2">
            <label htmlFor={paperLabelId} className="text-sm font-medium">
              Paper Token
              {loading && (
                <span className="loading loading-spinner loading-xs ml-2 text-black"></span>
              )}
            </label>
            <input
              className="rounded-md bg-white px-4 py-2 text-black focus:outline-none focus:ring-2 focus:ring-[#007BFF]"
              id={paperLabelId}
              {...register("paper_token")}
            />
            <span className="mt-[-4px] h-1 text-xs text-gray-300">
              {accounts &&
                `${accounts.paper_accounts} account${accounts.paper_accounts > 1 ? "s" : ""}`}
            </span>
          </div>

          {/* Live Token */}
          <div className="flex flex-col gap-2">
            <label htmlFor={liveLabelId} className="text-sm font-medium">
              Live Token
              {loading && (
                <span className="loading loading-spinner loading-xs ml-2 text-black"></span>
              )}
            </label>
            <input
              className="rounded-md bg-white px-4 py-2 text-black focus:outline-none focus:ring-2 focus:ring-[#007BFF]"
              id={liveLabelId}
              {...register("live_token")}
            />
            <span className="mt-[-4px] h-1 text-xs text-gray-300">
              {accounts &&
                `${accounts.live_accounts} account${accounts.live_accounts > 1 ? "s" : ""}`}
            </span>
          </div>

          {/* Error */}
          <span className="h-2 text-red-500">{updateError}</span>
          {/* Buttons */}
          <div className="flex h-11 w-full justify-between gap-2">
            <button
              type="submit"
              className="flex-1 rounded-md bg-[#007BFF] transition-all duration-200 hover:bg-[#0056b3] active:scale-95 active:bg-[#004085]"
            >
              Submit
            </button>
            <button
              type="button"
              id="closeAccessBtn"
              onClick={onClose}
              className="flex-1 rounded-md bg-red-600 transition-all duration-200 hover:bg-red-700 active:scale-95 active:bg-red-800"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </Modal>
  );
}
