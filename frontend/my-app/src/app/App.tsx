import MainView from "./MainView";
import Footer from "../components/Footer/Footer";
import "../styles/index.css";

export default function App() {
  return (
    <div className="app-container">
      <MainView />
      <Footer />;
    </div>
  );
}
