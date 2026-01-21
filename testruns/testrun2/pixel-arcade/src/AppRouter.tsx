import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import Home from './pages/Home'

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />,
  },
])

function AppRouter() {
  return <RouterProvider router={router} />
}

export default AppRouter