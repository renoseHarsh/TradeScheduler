import Index from "./Home/Index";
import Auth from "./Auth/Auth";
import {
  createBrowserRouter,
  Navigate,
  RouterProvider,
} from "react-router-dom";
import { useUserContext } from "./context/userContext";

function App() {
  const { user } = useUserContext();
  const router = createBrowserRouter([
    {
      path: "/",
      element: user ? <Index /> : <Navigate to="/login" replace />,
    },
    {
      path: "/login",
      element: !user ? <Auth isLogin={true} /> : <Navigate to="/" replace />,
    },
    {
      path: "/register",
      element: !user ? <Auth isLogin={false} /> : <Navigate to="/" replace />,
    },
  ]);
  return <RouterProvider router={router} />;
}

export default App;
