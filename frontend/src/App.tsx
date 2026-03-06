import { Toaster } from "react-hot-toast"
import { AppRouter } from "./router/AppRouter"

export const App = () => {
  return (
    <>
      <Toaster
        position="top-center"
        toastOptions={{
          duration: 3000
        }}
      />
      <AppRouter />
    </>
  )
}

export default App