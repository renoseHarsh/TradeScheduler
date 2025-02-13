import { useId, useState } from "react";
import { useForm, SubmitHandler } from "react-hook-form";
import { loginUser } from "../../api/authApi";
import { useUserContext } from "../../context/userContext";

type Inputs = {
  username: string;
  password: string;
};

export default function Login() {
  const usernameId = useId();
  const passwordId = useId();
  const [serverError, setServerError] = useState("");
  const [loading, setLoading] = useState(false);
  const { setUser } = useUserContext();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<Inputs>();
  const onSubmit: SubmitHandler<Inputs> = async (data) => {
    setLoading(true);
    const response = await loginUser(data);
    setLoading(false);
    if (response.status === 200) setUser(response.data);
    setServerError(response.message);
  };

  return (
    <div className="w-full max-w-md rounded-lg bg-white p-6 shadow-lg">
      <h1 className="mb-4 text-center text-2xl font-bold text-gray-800">
        Login
      </h1>
      <form className="flex flex-col gap-2" onSubmit={handleSubmit(onSubmit)}>
        {/* Username */}
        <div className="space-y-1">
          <label
            className="block text-sm font-medium text-gray-700"
            htmlFor={usernameId}
          >
            Username
          </label>
          <input
            className="block w-full rounded-md border border-gray-300 bg-gray-200 px-3 py-2 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            id={usernameId}
            type="text"
            {...register("username", {
              required: "Username is required",
            })}
          />
          <span className="ml-1 h-1 text-sm text-red-500">
            {errors.username?.message}
          </span>
        </div>

        {/* Password */}
        <div className="space-y-1">
          <label
            htmlFor={passwordId}
            className="block text-sm font-medium text-gray-700"
          >
            Password
          </label>
          <input
            id={passwordId}
            type="password"
            className="block w-full rounded-md border border-gray-300 bg-gray-200 px-3 py-2 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            {...register("password", {
              required: "Password is required",
            })}
          />
          <span className="ml-1 h-1 text-sm text-red-500">
            {errors.password?.message}
          </span>
        </div>
        <span className="mb-2 h-4 self-center text-sm text-red-500">
          {serverError}
        </span>
        {/* Login Button */}
        <button className="w-full rounded-lg bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
          {/* Login */}
          {loading ? (
            <span className="loading loading-spinner loading-xs"></span>
          ) : (
            "Login"
          )}
        </button>
      </form>
    </div>
  );
}
