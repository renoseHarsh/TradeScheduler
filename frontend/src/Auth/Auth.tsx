import Login from "./components/Login";
import Register from "./components/Register";

export default function Auth({ isLogin }: { isLogin: boolean }) {
  return (
    <div className="flex h-full items-center justify-center bg-blue-600 text-black">
      {isLogin ? <Login /> : <Register />}
    </div>
  );
}
